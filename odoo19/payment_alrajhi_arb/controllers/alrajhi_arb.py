# -*- coding: utf-8 -*-

import json
import logging
from html import escape
from urllib.parse import parse_qs, urlencode

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from ..services.arb_client import ARBClient


_logger = logging.getLogger(__name__)


class AlRajhiARBController(http.Controller):
    """Handle ARB return callback (bank hosted redirect)."""

    @staticmethod
    def _get_callback_params(route_params):
        """Collect callback data from query string, form POST, JSON POST, or raw form body.

        Some ARB hosted pages return a browser POST where the useful data is only in
        ``trandata`` and not in a standalone ``paymentId`` parameter. Be deliberately
        defensive here because Odoo must not reject the request before reading the
        encrypted gateway payload.
        """

        params = {}
        params.update(route_params or {})

        httprequest = request.httprequest

        # Query string values.
        try:
            params.update(httprequest.args.to_dict(flat=True))
        except Exception:
            pass

        # Standard form POST values.
        try:
            params.update(httprequest.form.to_dict(flat=True))
        except Exception:
            pass

        # Odoo's merged params, useful for type='http' routes.
        try:
            params.update(dict(request.params))
        except Exception:
            pass

        # JSON or raw x-www-form-urlencoded fallback.
        if httprequest.method == "POST":
            try:
                raw_body = httprequest.get_data(cache=True, as_text=True) or ""
            except Exception:
                raw_body = ""

            if raw_body:
                content_type = (httprequest.content_type or "").lower()
                if "json" in content_type:
                    try:
                        body = json.loads(raw_body)
                        if isinstance(body, dict):
                            params.update(body)
                    except Exception:
                        pass
                elif "=" in raw_body:
                    try:
                        parsed = parse_qs(raw_body, keep_blank_values=True)
                        params.update({key: values[-1] for key, values in parsed.items() if values})
                    except Exception:
                        pass

        return params

    @staticmethod
    def _get_param(params, *names):
        """Read a value from params using case-insensitive key matching."""

        for name in names:
            if name in params and params[name] not in (None, ""):
                return params[name]

        lowered = {str(key).lower(): value for key, value in (params or {}).items()}
        for name in names:
            value = lowered.get(str(name).lower())
            if value not in (None, ""):
                return value
        return None


    @classmethod
    def _get_any_param(cls, *sources_and_names):
        """Read the first non-empty value from dictionaries using case-insensitive keys.

        Usage: ``_get_any_param(params, plain, ("result", "Result"))``.
        The last argument must be an iterable of field names; all previous arguments
        are dictionaries to search in order.
        """

        if not sources_and_names:
            return None
        *sources, names = sources_and_names
        for source in sources:
            if not isinstance(source, dict):
                continue
            value = cls._get_param(source, *names)
            if value not in (None, ""):
                return value
        return None

    @staticmethod
    def _to_dict(decrypted_payload):
        """Normalize decrypted ARB trandata to a dictionary."""

        if isinstance(decrypted_payload, list) and decrypted_payload:
            decrypted_payload = decrypted_payload[0]
        if isinstance(decrypted_payload, dict):
            return decrypted_payload
        return {}

    def _decrypt_trandata_with_known_providers(self, encrypted_trandata):
        """Try decrypting return trandata using configured ARB provider keys.

        ARB return callbacks can omit the standalone paymentId. In that case, the
        transaction cannot be located first. We therefore try the configured ARB
        resource keys until one decrypts the payload successfully, then use the
        decrypted paymentId/trackId to locate the transaction.
        """

        providers = request.env["payment.provider"].sudo().search(
            [
                ("code", "=", "alrajhi_arb"),
                ("arb_resource_key", "!=", False),
            ]
        )
        last_error = None
        for provider in providers:
            try:
                plain = ARBClient.decrypt_trandata(
                    resource_key=provider.arb_resource_key,
                    encrypted_hex=encrypted_trandata,
                )
                plain_dict = self._to_dict(plain)
                if plain_dict:
                    return provider, plain_dict
            except Exception as exc:
                last_error = exc

        _logger.warning(
            "Al Rajhi ARB: failed to decrypt callback trandata with configured providers: %s",
            last_error,
        )
        return request.env["payment.provider"], {}

    def _find_transaction(self, payment_id=None, track_id=None, provider=None):
        """Find the matching ARB transaction by gateway paymentId or stored trackId."""

        tx_model = request.env["payment.transaction"].sudo()
        domain = [("provider_code", "=", "alrajhi_arb")]
        if provider:
            domain.append(("provider_id", "=", provider.id))

        if payment_id:
            tx = tx_model.search(domain + [("provider_reference", "=", str(payment_id))], limit=1)
            if tx:
                return tx

        if track_id:
            tx = tx_model.search(domain + [("arb_track_id", "=", str(track_id))], limit=1)
            if tx:
                return tx

        return tx_model.browse()


    @staticmethod
    def _normalize_gateway_value(value):
        """Normalize ARB callback values; treat empty/blank markers as missing."""

        if value in (None, False):
            return ""
        value = str(value).strip()
        if value.upper() in {"", "NULL", "NONE", "N/A", "NA", "MISSING"}:
            return ""
        return value

    @classmethod
    def _notification_data_from_sources(
        cls,
        *,
        plain,
        params,
        tx,
        payment_id=None,
        track_id=None,
        error=None,
        error_text=None,
    ):
        """Build Odoo payment notification data from ARB plain/encrypted payloads."""

        payment_id = payment_id or cls._get_any_param(
            plain,
            params,
            ("paymentId", "PaymentID", "PaymentId", "payment_id", "paymentid", "payId", "PayId", "payid", "PayID"),
        )
        track_id = cls._get_any_param(
            plain,
            params,
            ("trackId", "TrackID", "track_id", "trackid", "trackID"),
        ) or track_id or tx.arb_track_id

        return {
            "payment_id": str(payment_id or tx.provider_reference or ""),
            "provider_reference": str(payment_id or tx.provider_reference or ""),
            "track_id": str(track_id or ""),
            "result": cls._get_any_param(
                plain,
                params,
                ("result", "Result", "paymentResult", "PaymentResult"),
            ),
            "error": error or cls._get_any_param(plain, params, ("error", "Error")),
            "error_text": error_text or cls._get_any_param(
                plain, params, ("errorText", "ErrorText", "error_text")
            ),
            "trans_id": cls._get_any_param(
                plain, params, ("transId", "TransID", "transactionId", "tranid", "tranId")
            ),
            "auth_resp_code": cls._get_any_param(
                plain,
                params,
                ("authRespCode", "AuthRespCode", "auth_resp_code", "responseCode", "ResponseCode"),
            ),
            "auth_code": cls._get_any_param(
                plain, params, ("authCode", "AuthCode", "auth_code", "auth", "Auth")
            ),
            "card_type": cls._get_any_param(
                plain, params, ("cardType", "CardType", "card_type")
            ),
            "amount": cls._get_any_param(
                plain, params, ("amt", "amount", "Amount", "amount_paid")
            ),
            "currency_code": cls._get_any_param(
                plain, params, ("currencyCode", "CurrencyCode", "currency_code", "currency")
            ),
        }

    @classmethod
    def _merge_final_values(cls, base_data, extra_data):
        """Copy meaningful values from extra_data into base_data."""

        if not extra_data:
            return base_data
        for key, value in extra_data.items():
            if cls._normalize_gateway_value(value):
                base_data[key] = value
        return base_data

    @classmethod
    def _has_final_payment_result(cls, notification_data):
        """Return True only when ARB sent a final success/failure signal.

        ARB can post a browser callback containing identifiers and 3DS metadata
        before sending a final authorization result. That intermediate callback must
        not validate the website order.
        """

        result = cls._normalize_gateway_value(notification_data.get("result")).upper()
        auth_resp_code = cls._normalize_gateway_value(notification_data.get("auth_resp_code")).upper()
        error = cls._normalize_gateway_value(notification_data.get("error"))
        error_text = cls._normalize_gateway_value(notification_data.get("error_text"))

        if error or error_text or auth_resp_code:
            return True

        final_results = {
            "CAPTURED",
            "APPROVED",
            "SUCCESS",
            "SUCCESSFUL",
            "PAID",
            "COMPLETED",
            "NOT CAPTURED",
            "NOT_CAPTURED",
            "DECLINED",
            "FAILED",
            "FAILURE",
            "CANCELED",
            "CANCELLED",
            "DENIED",
            "VOID",
            "VOIDED",
            "TIMEOUT",
            "EXPIRED",
        }
        return result in final_results

    @staticmethod
    def _get_non_success_landing_route(tx):
        """Return a safe route that does not validate/confirm the website order."""

        landing_route = tx.landing_route or ""
        if landing_route.startswith("/shop/"):
            return "/shop/payment"
        return "/payment/status"

    @staticmethod
    def _get_success_landing_route(tx):
        """Return Odoo's normal success route only after the transaction is done."""

        return tx.landing_route or "/payment/status"

    @classmethod
    def _get_processing_status_route(cls, tx, attempt=0):
        """Build the protected public route used while ARB status is not final."""

        query = urlencode({
            "token": tx.arb_return_token or "",
            "attempt": int(attempt or 0),
        })
        return f"/payment/alrajhi_arb/status/{tx.id}?{query}"

    @classmethod
    def _render_processing_page(cls, tx, attempt=0, delay=3):
        """Render a lightweight processing page that polls ARB inquiry safely."""

        status_route = cls._get_processing_status_route(tx, attempt=attempt + 1)
        title = "Payment is being verified"
        body = (
            "We are verifying your Al Rajhi payment. "
            "Please do not close this page or go back."
        )
        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta http-equiv="refresh" content="{int(delay)};url={escape(status_route)}"/>
  <title>{escape(title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f7f7f7; color: #222; }}
    .card {{ max-width: 520px; background: #fff; border-radius: 14px; padding: 28px; box-shadow: 0 8px 24px rgba(0,0,0,.08); text-align: center; }}
    .spinner {{ width: 36px; height: 36px; border: 4px solid #ddd; border-top-color: #555; border-radius: 50%; margin: 0 auto 18px; animation: spin 1s linear infinite; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    a {{ color: #0066cc; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="spinner"></div>
    <h2>{escape(title)}</h2>
    <p>{escape(body)}</p>
    <p>Reference: <strong>{escape(tx.reference or '')}</strong></p>
    <p>If this page does not continue automatically, <a href="{escape(status_route)}">click here</a>.</p>
  </div>
</body>
</html>"""
        return request.make_response(html, headers=[("Content-Type", "text/html; charset=utf-8")])

    def _verify_by_inquiry(self, tx, notification_data=None):
        """Call ARB inquiry and merge any final result into notification_data."""

        notification_data = dict(notification_data or {})
        inquiry_plain = ARBClient.inquire_transaction(
            provider=tx.provider_id,
            amount=tx.amount,
            payment_id=notification_data.get("payment_id") or tx.provider_reference,
            track_id=notification_data.get("track_id") or tx.arb_track_id,
            trans_id=notification_data.get("trans_id"),
        )
        inquiry_data = self._notification_data_from_sources(
            plain=inquiry_plain if isinstance(inquiry_plain, dict) else {},
            params={},
            tx=tx,
            payment_id=notification_data.get("payment_id") or tx.provider_reference,
            track_id=notification_data.get("track_id") or tx.arb_track_id,
            error=inquiry_plain.get("error") if isinstance(inquiry_plain, dict) else None,
            error_text=inquiry_plain.get("errorText") if isinstance(inquiry_plain, dict) else None,
        )
        self._merge_final_values(notification_data, inquiry_data)
        _logger.info(
            "Al Rajhi ARB: inquiry verification tx=%s result=%s auth_resp_code=%s error=%s error_text=%s",
            tx.reference,
            notification_data.get("result") or "missing",
            notification_data.get("auth_resp_code") or "missing",
            notification_data.get("error") or "missing",
            notification_data.get("error_text") or "missing",
        )
        return notification_data

    def _process_final_or_wait(self, tx, notification_data, attempt=0):
        """Process final ARB data or keep the customer on a safe processing page."""

        if self._has_final_payment_result(notification_data):
            tx._process("alrajhi_arb", notification_data)
            if tx.state == "done":
                return request.redirect(self._get_success_landing_route(tx))
            return request.redirect(self._get_non_success_landing_route(tx))

        # Not final yet: never validate the website order. Give ARB a short window
        # to finish authorization, then send the customer back to payment safely.
        attempt = int(attempt or 0)
        if attempt >= 5:
            _logger.warning(
                "Al Rajhi ARB: payment still non-final after inquiry retries tx=%s payment_id=%s track_id=%s",
                tx.reference,
                notification_data.get("payment_id") or tx.provider_reference or "missing",
                notification_data.get("track_id") or tx.arb_track_id or "missing",
            )
            return request.redirect(self._get_non_success_landing_route(tx))
        return self._render_processing_page(tx, attempt=attempt)

    @http.route(
        "/payment/alrajhi_arb/return",
        type="http",
        auth="public",
        methods=["GET", "POST"],
        csrf=False,
        sitemap=False,
    )
    def alrajhi_arb_return(self, **route_params):
        # ARB can return by browser GET or by form POST depending on the payment flow.
        params = self._get_callback_params(route_params)

        payment_id = self._get_param(
            params,
            "paymentId", "PaymentID", "PaymentId", "payment_id", "paymentid", "payId", "PayId", "payid", "PayID",
        )
        encrypted_trandata = self._get_param(params, "trandata", "Trandata", "tranData", "trandata[]")
        error = self._get_param(params, "error", "Error")
        error_text = self._get_param(params, "errorText", "ErrorText", "error_text")

        plain = {}
        provider = request.env["payment.provider"]

        if encrypted_trandata:
            if payment_id:
                tx_for_key = self._find_transaction(payment_id=payment_id)
                if tx_for_key:
                    provider = tx_for_key.provider_id
                    try:
                        plain = self._to_dict(
                            ARBClient.decrypt_trandata(
                                resource_key=provider.arb_resource_key,
                                encrypted_hex=encrypted_trandata,
                            )
                        )
                    except Exception as exc:
                        _logger.warning(
                            "Al Rajhi ARB: failed to decrypt callback trandata for paymentId=%s: %s",
                            payment_id,
                            exc,
                        )
                else:
                    provider, plain = self._decrypt_trandata_with_known_providers(encrypted_trandata)
            else:
                provider, plain = self._decrypt_trandata_with_known_providers(encrypted_trandata)

        # Some ARB responses carry identifiers inside the encrypted trandata only.
        payment_id = payment_id or self._get_param(
            plain,
            "paymentId", "PaymentID", "PaymentId", "payment_id", "paymentid", "payId", "PayId", "payid", "PayID",
        )
        track_id = self._get_any_param(
            plain,
            params,
            ("trackId", "TrackID", "track_id", "trackid", "trackID"),
        )

        tx = self._find_transaction(payment_id=payment_id, track_id=track_id, provider=provider if provider else None)
        if not tx and provider:
            tx = self._find_transaction(payment_id=payment_id, track_id=track_id)

        if not tx:
            raise ValidationError(
                "Al Rajhi ARB: no transaction found for return callback. "
                "Received keys=%s, paymentId=%s, trackId=%s."
                % (", ".join(sorted(str(key) for key in params.keys())) or "none", payment_id or "missing", track_id or "missing")
            )

        # ARB can either return a standalone plain form payload or an encrypted
        # trandata payload. Do not rely on trandata only; some hosted-page flows
        # post fields directly to responseURL/errorURL.
        notification_data = self._notification_data_from_sources(
            plain=plain,
            params=params,
            tx=tx,
            payment_id=payment_id,
            track_id=track_id,
            error=error,
            error_text=error_text,
        )

        _logger.info(
            "Al Rajhi ARB: return callback tx=%s payment_id=%s track_id=%s result=%s auth_resp_code=%s error=%s error_text=%s raw_keys=%s decrypted=%s",
            tx.reference,
            notification_data.get("payment_id") or "missing",
            notification_data.get("track_id") or "missing",
            notification_data.get("result") or "missing",
            notification_data.get("auth_resp_code") or "missing",
            error or "missing",
            error_text or "missing",
            sorted(str(key) for key in params.keys()),
            bool(plain),
        )

        if not self._has_final_payment_result(notification_data):
            # ARB can post intermediate 3DS/browser data first. Verify by inquiry
            # before deciding whether to finish or keep waiting.
            try:
                notification_data = self._verify_by_inquiry(tx, notification_data)
            except Exception as exc:
                _logger.warning(
                    "Al Rajhi ARB: inquiry verification failed for tx=%s payment_id=%s track_id=%s: %s",
                    tx.reference,
                    notification_data.get("payment_id") or "missing",
                    notification_data.get("track_id") or "missing",
                    exc,
                )

        return self._process_final_or_wait(tx, notification_data, attempt=0)

    @http.route(
        "/payment/alrajhi_arb/status/<int:tx_id>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
        sitemap=False,
    )
    def alrajhi_arb_status(self, tx_id, token=None, attempt=0, **_kwargs):
        """Protected status page used after non-final ARB browser callbacks."""

        tx = request.env["payment.transaction"].sudo().browse(int(tx_id)).exists()
        if not tx or tx.provider_code != "alrajhi_arb" or not token or token != tx.arb_return_token:
            return request.not_found()

        if tx.state == "done":
            return request.redirect(self._get_success_landing_route(tx))
        if tx.state in {"error", "cancel"}:
            return request.redirect(self._get_non_success_landing_route(tx))

        notification_data = {
            "payment_id": tx.provider_reference or "",
            "provider_reference": tx.provider_reference or "",
            "track_id": tx.arb_track_id or "",
        }
        try:
            notification_data = self._verify_by_inquiry(tx, notification_data)
        except Exception as exc:
            _logger.warning(
                "Al Rajhi ARB: status inquiry failed for tx=%s payment_id=%s track_id=%s: %s",
                tx.reference,
                tx.provider_reference or "missing",
                tx.arb_track_id or "missing",
                exc,
            )

        return self._process_final_or_wait(tx, notification_data, attempt=int(attempt or 0))
