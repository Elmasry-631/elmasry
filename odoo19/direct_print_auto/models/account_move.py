# -*- coding: utf-8 -*-
from odoo import models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ["account.move", "direct.print.mixin"]

    # ------------------------------------------------------------------
    # DirectPrintMixin implementation
    # ------------------------------------------------------------------
    def _get_direct_print_report_ref(self):
        return "account.account_invoices"

    def _should_direct_print_auto(self):
        """Auto-print only for customer invoices and refunds (not vendor bills).

        Decision: per STEP 0 confirmation, customer-only.
        """
        # Vendor bills and entries never auto-print
        if self.move_type not in ("out_invoice", "out_refund"):
            return False
        return bool(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("direct_print_auto.invoice_auto", "False")
            .lower() == "true"
        )

    # ------------------------------------------------------------------
    # Post override — wrap super().action_post() with auto-print
    # ------------------------------------------------------------------
    def action_post(self):
        action = super().action_post()
        return self._trigger_direct_print_after(action)
