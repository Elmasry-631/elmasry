# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "direct.print.mixin"]

    # ------------------------------------------------------------------
    # DirectPrintMixin implementation
    # ------------------------------------------------------------------
    def _get_direct_print_report_ref(self):
        return "sale.action_report_saleorder"

    def _should_direct_print_auto(self):
        """Auto-print fires when the SO toggle is enabled in settings."""
        return bool(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("direct_print_auto.so_auto", "False")
            .lower() == "true"
        )

    # ------------------------------------------------------------------
    # Confirm override — wrap super().action_confirm() with auto-print
    # ------------------------------------------------------------------
    def action_confirm(self):
        action = super().action_confirm()
        return self._trigger_direct_print_after(action)
