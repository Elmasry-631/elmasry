# -*- coding: utf-8 -*-
from odoo import models


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = ["purchase.order", "direct.print.mixin"]

    # ------------------------------------------------------------------
    # DirectPrintMixin implementation
    # ------------------------------------------------------------------
    def _get_direct_print_report_ref(self):
        return "purchase.action_report_purchase_order"

    def _should_direct_print_auto(self):
        """Auto-print fires when the PO toggle is enabled in settings."""
        return bool(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("direct_print_auto.po_auto", "False")
            .lower() == "true"
        )

    # ------------------------------------------------------------------
    # Approve override — wrap super().button_approve() with auto-print
    # ------------------------------------------------------------------
    def button_approve(self):
        action = super().button_approve()
        return self._trigger_direct_print_after(action)
