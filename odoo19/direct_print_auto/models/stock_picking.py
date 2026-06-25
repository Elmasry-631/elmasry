# -*- coding: utf-8 -*-
from odoo import models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "direct.print.mixin"]

    # ------------------------------------------------------------------
    # DirectPrintMixin implementation
    # ------------------------------------------------------------------
    def _get_direct_print_report_ref(self):
        return "stock.action_report_delivery"

    def _should_direct_print_auto(self):
        """Auto-print only for outgoing (delivery) pickings.

        Decision: per STEP 0 confirmation, outgoing-only.
        """
        if self.picking_type_id.code != "outgoing":
            return False
        return bool(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("direct_print_auto.picking_auto", "False")
            .lower() == "true"
        )

    # ------------------------------------------------------------------
    # Validate override — wrap super().button_validate() with auto-print
    # ------------------------------------------------------------------
    def button_validate(self):
        action = super().button_validate()
        return self._trigger_direct_print_after(action)
