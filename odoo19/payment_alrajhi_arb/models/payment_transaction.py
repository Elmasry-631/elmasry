# -*- coding: utf-8 -*-

import uuid

from odoo import fields, models
from odoo.exceptions import ValidationError

from ..services.arb_client import ARBClient


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    arb_track_id = fields.Char(
        string="Al Rajhi ARB Track ID",
        copy=False,
        readonly=True,
        index=True,
        help="Merchant-side trackId sent to Al Rajhi. Used to match callbacks that do not return paymentId separately.",
    )
    arb_return_token = fields.Char(
        string="Al Rajhi ARB Return Token",
        copy=False,
        readonly=True,
        index=True,
        help="Private token used to protect the public ARB processing/status route.",
    )

    def _get_specific_processing_values(self, processing_values):
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != "alrajhi_arb":
            return res

        if self.operation != "online_redirect":
            # For now, implement only bank-hosted redirect payments.
            return res

        # Mark transaction as pending before redirecting customer.
        if self.state == "draft":
            self._set_pending()

        base_url = self._get_base_url()
        callback_url = f"{base_url}/payment/alrajhi_arb/return"

        # ARB documents trackId as numeric. Keep it numeric and unique enough for
        # bank-side duplicate checks while avoiding card-data collection in Odoo.
        track_id = str(uuid.uuid4().int % 10**16).zfill(16)
        return_token = uuid.uuid4().hex

        payment_id, payment_action_url, payment_params, payment_page_base = ARBClient.create_payment_token(
            provider=self.provider_id,
            track_id=track_id,
            amount=self.amount,
            response_url=callback_url,
            error_url=callback_url,
            action_code="1",  # Purchase
            langid="ar",
        )

        # Save gateway payment id to reliably locate the transaction on return.
        # Use write() so it is persisted before the user is redirected.
        self.write({
            "provider_reference": str(payment_id),
            "arb_track_id": str(track_id),
            "arb_return_token": return_token,
        })

        import logging
        _logger = logging.getLogger("payment_alrajhi_arb")
        _tid = str(self.provider_id.arb_tranportal_id or "")
        _tid_masked = ("%s***%s" % (_tid[:2], _tid[-2:])) if len(_tid) > 4 else ("set" if _tid else "unset")
        _logger.info(
            "ARB DEBUG: payment_id=%s payment_page_base=%s payment_action_url=%s payment_param_names=%s track_id=%s callback_url=%s tranportal_id=%s",
            payment_id,
            payment_page_base,
            payment_action_url,
            [param.get("name") for param in payment_params],
            track_id,
            callback_url,
            _tid_masked,
        )

        return {
            **res,
            "arb_payment_action_url": payment_action_url,
            "arb_payment_params": payment_params,
            "arb_payment_page_url": payment_page_base,
            "arb_payment_id": payment_id,
        }

    def _get_specific_rendering_values(self, processing_values):
        rendering_values = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != "alrajhi_arb":
            return rendering_values

        return {
            **rendering_values,
            "payment_action_url": processing_values.get("arb_payment_action_url"),
            "payment_params": processing_values.get("arb_payment_params") or [],
            "payment_id": str(processing_values.get("arb_payment_id") or "").strip(),
            "tranportal_id": str(self.provider_id.arb_tranportal_id or "").strip(),
        }

    def _search_by_reference(self, provider_code, payment_data):
        if provider_code != "alrajhi_arb":
            return super()._search_by_reference(provider_code, payment_data)

        payment_id = payment_data.get("payment_id") or payment_data.get("provider_reference")
        track_id = payment_data.get("track_id")

        if payment_id:
            tx = self.search(
                [
                    ("provider_code", "=", "alrajhi_arb"),
                    ("provider_reference", "=", str(payment_id)),
                ],
                limit=1,
            )
            if tx:
                return tx

        if track_id:
            tx = self.search(
                [
                    ("provider_code", "=", "alrajhi_arb"),
                    ("arb_track_id", "=", str(track_id)),
                ],
                limit=1,
            )
            if tx:
                return tx

        raise ValidationError(
            "Al Rajhi ARB: transaction not found for payment_id=%s track_id=%s"
            % (payment_id or "missing", track_id or "missing")
        )

    def _extract_amount_data(self, payment_data):
        if self.provider_code != "alrajhi_arb":
            return super()._extract_amount_data(payment_data)

        amount = payment_data.get("amount")
        currency_code = payment_data.get("currency_code")
        if not amount or not currency_code:
            # ARB return payloads do not always include the amount/currency. In that
            # case, skip Odoo's amount validation instead of raising a KeyError.
            return None

        currency_map = {
            "682": "SAR",
        }
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return None

        return {
            "amount": amount,
            "currency_code": currency_map.get(str(currency_code), str(currency_code)),
        }

    def _apply_updates(self, payment_data):
        if self.provider_code != "alrajhi_arb":
            return super()._apply_updates(payment_data)

        result = str(payment_data.get("result") or "").strip().upper()
        auth_resp_code = str(payment_data.get("auth_resp_code") or "").strip().upper()
        error = str(payment_data.get("error") or "").strip()
        error_text = str(payment_data.get("error_text") or "").strip()

        # ARB can include empty-looking markers in browser callbacks. Normalize
        # them so intermediate returns do not become false failures/successes.
        empty_markers = {"", "NULL", "NONE", "N/A", "NA", "MISSING"}
        if result in empty_markers:
            result = ""
        if auth_resp_code in empty_markers:
            auth_resp_code = ""
        if error.upper() in empty_markers:
            error = ""
        if error_text.upper() in empty_markers:
            error_text = ""

        failure_message = error_text or error

        if payment_data.get("payment_id"):
            self.provider_reference = str(payment_data["payment_id"])
        if payment_data.get("track_id") and not self.arb_track_id:
            self.arb_track_id = str(payment_data["track_id"])

        success_results = {
            "CAPTURED",
            "APPROVED",
            "SUCCESS",
            "SUCCESSFUL",
            "PAID",
            "COMPLETED",
        }
        failure_results = {
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
        success_auth_codes = {"0", "00", "000"}

        if result in success_results or (auth_resp_code in success_auth_codes and not failure_message):
            message = "ARB result=%s" % (result or auth_resp_code or "success")
            self._set_done(state_message=message)
            return

        if result in failure_results or failure_message:
            self._set_error(
                state_message=failure_message or "ARB payment failed (result=%s)." % result
            )
            return

        if auth_resp_code and auth_resp_code not in success_auth_codes:
            self._set_error(
                state_message="ARB payment authorization failed (authRespCode=%s)." % auth_resp_code
            )
            return

        # Do not mark a transaction as failed just because ARB returned without a
        # final status. Some hosted-page responses post only identifiers first. Keep
        # the transaction pending so it can be completed by a later callback/manual
        # verification instead of showing a false payment failure to the customer.
        self._set_pending(
            state_message=(
                "ARB returned without a final payment result. "
                "Waiting for payment confirmation."
            )
        )

    def _get_base_url(self):
        """Compute absolute base URL (web base url preferred)."""
        icp = self.env["ir.config_parameter"].sudo()
        return icp.get_param("web.base.url", default="").rstrip("/")

