# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAutoPrintFlow(TransactionCase):
    """Integration tests for the auto-print-on-confirm flow.

    These tests verify that when a sales order is confirmed and the
    SO auto-print toggle is on, ``action_confirm`` returns a direct
    print client action wrapping the original confirm action.
    """

    def setUp(self):
        super().setUp()
        self.ICP = self.env["ir.config_parameter"].sudo()

    def test_30_so_confirm_wraps_action_when_auto_print_on(self):
        self.ICP.set_param("direct_print_auto.so_auto", "true")
        so = self.env["sale.order"].create({
            "partner_id": self.env.ref("base.res_partner_2").id,
            "order_line": [(0, 0, {
                "product_id": self.env.ref("product.product_product_1").id,
                "product_uom_qty": 1.0,
                "price_unit": 100.0,
            })],
        })
        action = so.action_confirm()
        self.assertEqual(action.get("type"), "ir.actions.client")
        self.assertEqual(action.get("tag"), "direct_print_auto")
        params = action.get("params", {})
        self.assertEqual(params.get("report_ref"), "sale.action_report_saleorder")
        self.assertEqual(params.get("res_model"), "sale.order")
        # next_action must be set so the user is returned to the form view
        # after the print dialog closes
        self.assertTrue(params.get("next_action"))

    def test_31_so_confirm_no_wrap_when_auto_print_off(self):
        self.ICP.set_param("direct_print_auto.so_auto", "False")
        so = self.env["sale.order"].create({
            "partner_id": self.env.ref("base.res_partner_2").id,
            "order_line": [(0, 0, {
                "product_id": self.env.ref("product.product_product_1").id,
                "product_uom_qty": 1.0,
                "price_unit": 100.0,
            })],
        })
        action = so.action_confirm()
        # The standard sale confirm returns True or a dict — never the
        # direct_print_auto client action when the toggle is off.
        if isinstance(action, dict):
            self.assertNotEqual(action.get("tag"), "direct_print_auto")
