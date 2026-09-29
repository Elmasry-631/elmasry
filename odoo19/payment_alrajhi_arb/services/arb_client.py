# -*- coding: utf-8 -*-

import json
import logging
from urllib.parse import parse_qsl, quote_plus, urlencode, unquote_plus, urlsplit, urlunsplit

import requests
from odoo import _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ARBClient:
    """Minimal ARB REST client + trandata AES encrypt/decrypt utilities.

    Encryption/Decryption rules extracted from:
    "Sample Encryption and Decryption Code For JAVA/JAVASCRIPT" in the provided ARB PDF.
    """

    AES_IV = "PGKEYENCDECIVSPC"
    CURRENCY_CODE_SAR = "682"

    @staticmethod
    def _require_crypto():
        try:
            from Crypto.Cipher import AES  # noqa: F401
            from Crypto.Util.Padding import pad, unpad  # noqa: F401

            return AES, pad, unpad
        except Exception as e:
            raise UserError(
                "Al Rajhi ARB: missing crypto dependency. "
                "Please ensure PyCryptodome is installed in the Odoo environment (%s)." % e
            )

    @classmethod
    def encrypt_trandata(cls, resource_key: str, plain_text: str) -> str:
        """Encrypt plain JSON (URL-encoded before encryption) into ARB encryptedHex."""

        AES, pad, _unpad = cls._require_crypto()
        key_bytes = (resource_key or "").encode("utf-8")
        iv_bytes = cls.AES_IV.encode("utf-8")

        # ARB requires URL Encoder before encrypting.
        encoded = quote_plus(plain_text, safe="")
        data = encoded.encode("utf-8")
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        # ARB sample (Java) returns HEX string uppercase.
        return ciphertext.hex().upper()

    @classmethod
    def decrypt_trandata(cls, resource_key: str, encrypted_hex: str):
        """Decrypt ARB encryptedHex and return decoded JSON (object/list)."""

        AES, _pad, unpad = cls._require_crypto()
        encrypted_hex = unquote_plus(str(encrypted_hex or "").strip())
        ciphertext = bytes.fromhex(encrypted_hex)

        key_bytes = (resource_key or "").encode("utf-8")
        iv_bytes = cls.AES_IV.encode("utf-8")
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        padded = cipher.decrypt(ciphertext)
        plain_encoded = unpad(padded, AES.block_size).decode("utf-8")

        # ARB requires URL Decoder after decryption.
        plain_json = unquote_plus(plain_encoded)
        try:
            return json.loads(plain_json)
        except Exception:
            # Some ARB flows might return a non-JSON string; keep raw.
            return plain_json

    @classmethod
    def get_customer_ip_header(cls) -> str:
        """Return an X-FORWARDED-FOR compatible value for ARB risk checks."""

        # NOTE: This helper assumes it is executed inside an HTTP request context.
        # For background jobs, we fall back to empty string.
        try:
            from odoo.http import request as odoo_request

            headers = odoo_request.httprequest.headers
            xff = headers.get("X-FORWARDED-FOR")
            if xff:
                # ARB needs the customer's IP first.
                return xff.split(",")[0].strip()
            return odoo_request.httprequest.remote_addr or ""
        except Exception:
            return ""

    @classmethod
    def _choose_endpoint(cls, provider) -> str:
        """Pick sandbox/live endpoint based on payment.provider.state."""

        if getattr(provider, "state", None) == "test":
            return provider.arb_endpoint_url_test or ""
        return provider.arb_endpoint_url_prod or ""

    @classmethod
    def _choose_inquiry_endpoint(cls, provider) -> str:
        """Inquiry/verification (action 8) always uses the Tranportal API path.

        The token-generation field could later be pointed at a different page name;
        supporting transactions are served from ``.../pg/payment/tranportal.htm`` on
        the SAME host. This keeps inquiry working regardless of the token field value.
        """

        endpoint = str(cls._choose_endpoint(provider) or "").strip()
        split_url = urlsplit(endpoint)
        if split_url.path.lower().rsplit("/", 1)[-1] not in ("tranportal.htm", ""):
            parts = split_url.path.rsplit("/", 1)
            new_path = (parts[0] + "/tranportal.htm") if len(parts) == 2 else "/pg/payment/tranportal.htm"
            endpoint = urlunsplit((split_url.scheme, split_url.netloc, new_path, split_url.query, split_url.fragment))
        return endpoint

    @classmethod
    def _get_credentials(cls, provider):
        """Return stripped ARB credentials and fail early with a clear message."""

        tranportal_id = str(provider.arb_tranportal_id or "").strip()
        tranportal_password = str(provider.arb_tranportal_password or "").strip()
        resource_key = str(provider.arb_resource_key or "").strip()
        missing_fields = []
        if not tranportal_id:
            missing_fields.append("Tranportal ID")
        if not tranportal_password:
            missing_fields.append("Tranportal Password")
        if not resource_key:
            missing_fields.append("Resource Key")
        if missing_fields:
            raise UserError(
                "Al Rajhi ARB: the selected payment provider is missing: %s."
                % ", ".join(missing_fields)
            )
        return tranportal_id, tranportal_password, resource_key

    @classmethod
    def _build_headers(cls):
        """Build request headers required by ARB."""

        return {
            "Content-Type": "application/json",
            # Mandatory in ARB v1.31 for risk checks; the customer's IP must be first.
            "X-FORWARDED-FOR": cls.get_customer_ip_header(),
        }

    @classmethod
    def _post_gateway(cls, endpoint, payload):
        """POST a JSON payload to ARB and return the first response object."""

        _logger.info("Al Rajhi ARB: sending request to %s", endpoint)
        resp = requests.post(endpoint, json=payload, headers=cls._build_headers(), timeout=30)
        resp.raise_for_status()

        data = resp.json()
        if not isinstance(data, list) or not data:
            raise UserError("Al Rajhi ARB: unexpected gateway response format.")
        if not isinstance(data[0], dict):
            raise UserError("Al Rajhi ARB: unexpected gateway response item format.")
        return data[0]

    @classmethod
    def _normalize_bank_hosted_payment_url(cls, payment_page_url):
        """Return the user-facing bank-hosted payment page URL.

        This module does not collect card data in Odoo, so it must use ARB's
        Bank Hosted page where the customer enters the card/Mada details.  Some
        terminals return ``TranportalVbv.htm`` in the token response, which is a
        processing/3DS hand-off page used by merchant-hosted style flows. Opening
        that page directly can immediately post an intermediate callback to Odoo
        without displaying the card-entry page.

        For the standard bank-hosted Odoo redirect flow, normalize that returned
        path to ``paymentpage.htm`` and submit only ``PaymentID`` as documented
        by ARB for Bank Hosted Integration.
        """

        split_url = urlsplit(str(payment_page_url or "").strip())
        path = split_url.path or ""
        if "tranportalvbv.htm" not in path.lower():
            return str(payment_page_url or "").strip()

        parts = path.rsplit("/", 1)
        normalized_path = "%s/paymentpage.htm" % parts[0] if len(parts) == 2 else "/pg/paymentpage.htm"
        normalized_url = urlunsplit(
            (
                split_url.scheme,
                split_url.netloc,
                normalized_path,
                "",
                split_url.fragment,
            )
        )
        _logger.info(
            "Al Rajhi ARB: normalized returned processing URL to bank-hosted payment page: %s -> %s",
            payment_page_url,
            normalized_url,
        )
        return normalized_url

    @classmethod
    def _get_payment_url_shape(cls, payment_page_url):
        """Return the ARB hosted page shape for parameter casing decisions."""

        path_lower = (urlsplit(str(payment_page_url or "")).path or "").lower()
        if "tranportalvbv" in path_lower:
            return "tranportal_vbv"
        return "payment_page"

    @classmethod
    def frame_payment_page_url(cls, payment_page_url, payment_id, tranportal_id):
        """Return a fully framed ARB hosted payment URL for logs/debugging."""

        action_url, form_params = cls.prepare_redirect_form_values(
            payment_page_url, payment_id, tranportal_id
        )
        return urlunsplit(
            (
                urlsplit(action_url).scheme,
                urlsplit(action_url).netloc,
                urlsplit(action_url).path,
                urlencode([(param["name"], param["value"]) for param in form_params]),
                urlsplit(action_url).fragment,
            )
        )

    @classmethod
    def prepare_redirect_form_values(cls, payment_page_url, payment_id, tranportal_id):
        """Prepare the GET form action and hidden fields for the ARB hosted page.

        The ARB guide shows two URL shapes:
        * paymentpage.htm -> PaymentID=<payment_id>
        * TranportalVbv.htm -> paymentId=<payment_id>&id=<tranportal_id>

        Odoo renders redirect providers as auto-submitted forms. A browser GET form
        submission can discard the query string already present in the action URL.
        Therefore, this method removes the action query and sends all required ARB
        query parameters as hidden form inputs.
        """

        raw_payment_page_url = str(payment_page_url or "").strip()
        payment_page_url = cls._normalize_bank_hosted_payment_url(raw_payment_page_url)
        payment_id = str(payment_id or "").strip()
        tranportal_id = str(tranportal_id or "").strip()
        if not payment_page_url:
            raise UserError("Al Rajhi ARB: missing payment page URL in token generation response.")
        if not payment_id:
            raise UserError("Al Rajhi ARB: missing payment ID in token generation response.")

        split_url = urlsplit(payment_page_url)
        existing_pairs = parse_qsl(split_url.query, keep_blank_values=True)
        shape = cls._get_payment_url_shape(payment_page_url)

        # Preserve non-ARB extra parameters returned by the gateway, but normalize
        # the mandatory names/casing expected by each hosted page.
        form_values = {}
        for key, value in existing_pairs:
            if str(key).lower() in {"paymentid", "id"}:
                continue
            form_values[key] = value

        if shape == "tranportal_vbv":
            if not tranportal_id:
                raise UserError("Al Rajhi ARB: missing Tranportal ID for TranportalVbv payment URL.")
            mandatory_pairs = [("paymentId", payment_id), ("id", tranportal_id)]
        else:
            mandatory_pairs = [("PaymentID", payment_id)]

        # Mandatory ARB identifiers first, then any gateway-supplied extras.
        form_params = [{"name": key, "value": value} for key, value in mandatory_pairs]
        form_params.extend(
            {"name": key, "value": value}
            for key, value in form_values.items()
            if key not in {param["name"] for param in form_params}
        )

        action_url = urlunsplit(
            (
                split_url.scheme,
                split_url.netloc,
                split_url.path,
                "",
                split_url.fragment,
            )
        )
        return action_url, form_params

    @classmethod
    def create_payment_token(
        cls,
        *,
        provider,
        track_id: str,
        amount: float,
        response_url: str,
        error_url: str,
        action_code: str = "1",
        langid: str = "ar",
    ):
        """Call ARB Payment Token Generation API and return (payment_id, payment_page_url)."""

        endpoint = str(cls._choose_endpoint(provider) or "").strip()
        if not endpoint:
            raise UserError("Al Rajhi ARB: missing endpoint URL configuration on the provider.")

        tranportal_id, tranportal_password, resource_key = cls._get_credentials(provider)

        plain_trandata = json.dumps(
            [
                {
                    "amt": f"{amount:.2f}",
                    "action": str(action_code),
                    "password": tranportal_password,
                    "id": tranportal_id,
                    "currencyCode": cls.CURRENCY_CODE_SAR,
                    "trackId": str(track_id),
                    "responseURL": response_url,
                    "errorURL": error_url,
                    "langid": langid,
                }
            ],
            separators=(",", ":"),
        )
        encrypted_trandata = cls.encrypt_trandata(resource_key, plain_trandata)

        payload = [
            {
                "id": tranportal_id,
                "trandata": encrypted_trandata,
                "responseURL": response_url,
                "errorURL": error_url,
            }
        ]

        # Safe diagnostic log: environment + endpoint + WHICH credentials are set (never the values).
        _logger.info(
            "Al Rajhi ARB: token request env=%s endpoint=%s tranportal_id_set=%s password_set=%s "
            "resource_key_set=%s track_id=%s amount=%.2f currency=%s response_url=%s error_url=%s",
            getattr(provider, "state", None), endpoint,
            bool(tranportal_id), bool(tranportal_password), bool(resource_key),
            track_id, amount, cls.CURRENCY_CODE_SAR, response_url, error_url,
        )

        first = cls._post_gateway(endpoint, payload)
        status = str(first.get("status") or "")
        err = first.get("error") or ""
        err_txt = first.get("errorText") or first.get("error_text") or ""
        _logger.info(
            "Al Rajhi ARB: token response env=%s endpoint=%s arb_status=%s arb_error=%s track_id=%s",
            getattr(provider, "state", None), endpoint, status or "-", err or "-", track_id,
        )
        if status != "1":
            # Technical details stay in the server log; the Tranportal ID is masked, secrets are never logged.
            _logger.warning(
                "Al Rajhi ARB: token generation FAILED env=%s endpoint=%s tranportal_id=%s***%s(len=%s) "
                "track_id=%s arb_error=%s arb_error_text=%s",
                getattr(provider, "state", None), endpoint,
                tranportal_id[:2], tranportal_id[-2:], len(tranportal_id),
                track_id, err or "-", err_txt or "-",
            )
            user_msg = _(
                "Al Rajhi Bank rejected the payment token request, so the customer could not be "
                "redirected to the payment page.\n\n"
                "The bank could not complete the request with the current terminal configuration. "
                "Please verify with Al Rajhi Bank that the Tranportal ID, password, Resource Key and "
                "environment (Test/Production) are correct, that the terminal is active for online "
                "payments, and whether this server's outbound IP address must be whitelisted for the "
                "terminal.\n\n"
                "ARB error: %(code)s - %(text)s"
            ) % {"code": err or "IPAY", "text": err_txt or "unknown"}
            raise UserError(user_msg)

        # result = "<paymentId>:<paymentPageBaseUrl>"
        result = first.get("result")
        if not result:
            raise UserError("Al Rajhi ARB: token generation succeeded but result is missing.")

        payment_id, payment_page_base = str(result).split(":", 1)
        payment_page_url = cls.frame_payment_page_url(payment_page_base, payment_id, tranportal_id)
        payment_action_url, payment_params = cls.prepare_redirect_form_values(
            payment_page_url, payment_id, tranportal_id
        )
        return payment_id, payment_action_url, payment_params, payment_page_url

    @classmethod
    def inquire_transaction(
        cls,
        *,
        provider,
        amount: float,
        payment_id: str = None,
        track_id: str = None,
        trans_id: str = None,
    ):
        """Call ARB Inquiry transaction API and return decrypted payment data.

        ARB's guide requires merchants to verify the transaction status after the
        gateway response. Inquiry action code is 8 and can be performed by
        PaymentID, TRANID, or TrackID.
        """

        endpoint = cls._choose_inquiry_endpoint(provider)
        if not endpoint:
            raise UserError("Al Rajhi ARB: missing endpoint URL configuration on the provider.")

        tranportal_id, tranportal_password, resource_key = cls._get_credentials(provider)

        lookup_type = None
        lookup_value = None
        if payment_id:
            lookup_type = "PaymentID"
            lookup_value = str(payment_id)
        elif trans_id:
            lookup_type = "TRANID"
            lookup_value = str(trans_id)
        elif track_id:
            lookup_type = "TrackID"
            lookup_value = str(track_id)

        if not lookup_value:
            return {}

        plain_trandata = json.dumps(
            [
                {
                    "id": tranportal_id,
                    "password": tranportal_password,
                    "action": "8",
                    "amt": f"{amount:.2f}",
                    "currencyCode": cls.CURRENCY_CODE_SAR,
                    "trackId": str(track_id or ""),
                    "udf5": lookup_type,
                    # ARB uses the transId field to carry the lookup value when
                    # udf5 specifies PaymentID / TRANID / TrackID.
                    "transId": lookup_value,
                }
            ],
            separators=(",", ":"),
        )
        encrypted_trandata = cls.encrypt_trandata(resource_key, plain_trandata)
        payload = [{"id": tranportal_id, "trandata": encrypted_trandata}]

        _logger.info(
            "Al Rajhi ARB: sending inquiry request by %s=%s",
            lookup_type,
            lookup_value,
        )
        first = cls._post_gateway(endpoint, payload)
        response_data = {
            "status": first.get("status"),
            "error": first.get("error") or first.get("Error"),
            "errorText": first.get("errorText") or first.get("ErrorText"),
        }

        encrypted_response = first.get("trandata") or first.get("Trandata") or first.get("tranData")
        if encrypted_response:
            plain = cls.decrypt_trandata(resource_key, encrypted_response)
            if isinstance(plain, list) and plain:
                plain = plain[0]
            if isinstance(plain, dict):
                response_data.update(plain)

        return response_data
