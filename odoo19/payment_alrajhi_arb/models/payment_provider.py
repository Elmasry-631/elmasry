# -*- coding: utf-8 -*-

import uuid

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("alrajhi_arb", "Al Rajhi Bank (ARB) - KSA")],
        ondelete={"alrajhi_arb": "set default"},
    )

    arb_tranportal_id = fields.Char(
        string="Tranportal ID",
        required_if_provider="alrajhi_arb",
    )
    arb_tranportal_password = fields.Char(
        string="Tranportal Password",
        required_if_provider="alrajhi_arb",
    )
    arb_resource_key = fields.Char(
        string="Resource Key",
        required_if_provider="alrajhi_arb",
    )

    arb_endpoint_url_test = fields.Char(
        string="Token Generation Endpoint (Test/UAT)",
        default="https://securepayments.alrajhibank.com.sa/pg/payment/tranportal.htm",
    )
    arb_endpoint_url_prod = fields.Char(
        string="Token Generation Endpoint (Production)",
        default="https://digitalpayments.alrajhibank.com.sa/pg/payment/tranportal.htm",
    )

    @api.model
    def _get_default_payment_method_codes(self):
        # ARB supports card payments through its bank-hosted flow.
        return {"card"}

    def _get_redirect_form_view(self, is_validation=False):
        """Resolve the redirect template dynamically instead of storing a DB FK.

        This avoids upgrade issues when Odoo refreshes QWeb views and keeps the
        provider independent from a hard ``redirect_form_view_id`` relation.
        """
        self.ensure_one()
        if self.code != "alrajhi_arb":
            return super()._get_redirect_form_view(is_validation=is_validation)
        return self.env.ref("payment_alrajhi_arb.arb_redirect_form_view")

    def _get_removal_values(self):
        """Clear provider-specific fields cleanly when the module is removed."""
        values = super()._get_removal_values()
        if self.code == "alrajhi_arb":
            values.update(
                {
                    "redirect_form_view_id": False,
                    "arb_tranportal_id": False,
                    "arb_tranportal_password": False,
                    "arb_resource_key": False,
                }
            )
        return values

    def _should_build_inline_form(self, is_validation=False):
        # Bank-hosted ARB integration relies on redirects (payment page), not inline/direct payments.
        return False

    def action_test_alrajhi_connection(self):
        """Safely test ARB token generation from THIS server. No Sale Order is created.

        Runs the exact token-generation request used at checkout with a 1.00 SAR amount.
        On success the bank returns an unused PaymentID (nobody is charged); on failure
        the bank's error code/message is shown. Credentials themselves are never displayed
        — only whether each one is configured.
        """
        self.ensure_one()
        if self.code != "alrajhi_arb":
            raise UserError(_("This test is only available for the Al Rajhi Bank (ARB) provider."))

        from ..services.arb_client import ARBClient

        base = self.env["ir.config_parameter"].sudo().get_param("web.base.url", default="").rstrip("/")
        callback = "%s/payment/alrajhi_arb/return" % (base or "https://example.com")
        track_id = str(uuid.uuid4().int % 10 ** 16).zfill(16)
        env_label = "Test/UAT" if self.state == "test" else "Production"
        endpoint = self.arb_endpoint_url_test if self.state == "test" else self.arb_endpoint_url_prod

        try:
            payment_id, _action_url, _params, _page = ARBClient.create_payment_token(
                provider=self,
                track_id=track_id,
                amount=1.00,
                response_url=callback,
                error_url=callback,
                action_code="1",
                langid="en",
            )
        except UserError as exc:
            return self._alrajhi_notify(
                title=_("Al Rajhi ARB test failed"),
                message=_("Environment: %(env)s\nEndpoint: %(url)s\n\n%(err)s")
                % {"env": env_label, "url": endpoint or "-", "err": str(exc)},
                success=False,
            )
        return self._alrajhi_notify(
            title=_("Al Rajhi ARB test succeeded"),
            message=_(
                "Environment: %(env)s\nEndpoint: %(url)s\n\n"
                "Token generated successfully — connection, credentials and terminal are working, "
                "so the customer redirect will work. Nothing was charged (PaymentID length: %(plen)s)."
            )
            % {"env": env_label, "url": endpoint or "-", "plen": len(str(payment_id))},
            success=True,
        )

    @staticmethod
    def _alrajhi_notify(title, message, success):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": title,
                "message": message,
                "type": "success" if success else "danger",
                "sticky": True,
            },
        }

