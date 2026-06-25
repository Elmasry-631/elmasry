# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDirectPrintMixin(TransactionCase):
    """Unit tests for the direct.print.mixin API and the per-model
    implementations of _get_direct_print_report_ref and
    _should_direct_print_auto.
    """

    def setUp(self):
        super().setUp()
        self.ICP = self.env["ir.config_parameter"].sudo()

    # ------------------------------------------------------------------
    # Report ref resolution
    # ------------------------------------------------------------------
    def test_01_sale_order_report_ref(self):
        so = self.env["sale.order"].create({"partner_id": self.env.ref("base.res_partner_2").id})
        self.assertEqual(so._get_direct_print_report_ref(), "sale.action_report_saleorder")

    def test_02_account_move_report_ref(self):
        move = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.env.ref("base.res_partner_2").id,
        })
        self.assertEqual(move._get_direct_print_report_ref(), "account.account_invoices")

    def test_03_stock_picking_report_ref(self):
        picking = self.env["stock.picking"].create({
            "partner_id": self.env.ref("base.res_partner_2").id,
            "picking_type_id": self.env.ref("stock.picking_type_out").id,
        })
        self.assertEqual(picking._get_direct_print_report_ref(), "stock.action_report_delivery")

    def test_04_purchase_order_report_ref(self):
        po = self.env["purchase.order"].create({"partner_id": self.env.ref("base.res_partner_1").id})
        self.assertEqual(po._get_direct_print_report_ref(), "purchase.action_report_purchase_order")

    # ------------------------------------------------------------------
    # Auto-print gating
    # ------------------------------------------------------------------
    def test_10_so_auto_print_disabled_by_default(self):
        self.ICP.set_param("direct_print_auto.so_auto", "False")
        so = self.env["sale.order"].create({"partner_id": self.env.ref("base.res_partner_2").id})
        self.assertFalse(so._should_direct_print_auto())

    def test_11_so_auto_print_enabled(self):
        self.ICP.set_param("direct_print_auto.so_auto", "true")
        so = self.env["sale.order"].create({"partner_id": self.env.ref("base.res_partner_2").id})
        self.assertTrue(so._should_direct_print_auto())

    def test_12_invoice_auto_print_customer_only(self):
        """Vendor bills must never auto-print even if the toggle is on."""
        self.ICP.set_param("direct_print_auto.invoice_auto", "true")
        customer_move = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.env.ref("base.res_partner_2").id,
        })
        vendor_move = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": self.env.ref("base.res_partner_1").id,
        })
        self.assertTrue(customer_move._should_direct_print_auto())
        self.assertFalse(vendor_move._should_direct_print_auto())

    def test_13_picking_auto_print_outgoing_only(self):
        """Only outgoing (delivery) pickings should auto-print."""
        self.ICP.set_param("direct_print_auto.picking_auto", "true")
        outgoing = self.env["stock.picking"].create({
            "partner_id": self.env.ref("base.res_partner_2").id,
            "picking_type_id": self.env.ref("stock.picking_type_out").id,
        })
        incoming = self.env["stock.picking"].create({
            "partner_id": self.env.ref("base.res_partner_1").id,
            "picking_type_id": self.env.ref("stock.picking_type_in").id,
        })
        self.assertTrue(outgoing._should_direct_print_auto())
        self.assertFalse(incoming._should_direct_print_auto())

    # ------------------------------------------------------------------
    # Manual button — action_direct_print returns a client action
    # ------------------------------------------------------------------
    def test_20_action_direct_print_returns_client_action(self):
        so = self.env["sale.order"].create({"partner_id": self.env.ref("base.res_partner_2").id})
        action = so.action_direct_print()
        self.assertEqual(action.get("type"), "ir.actions.client")
        self.assertEqual(action.get("tag"), "direct_print_auto")
        params = action.get("params", {})
        self.assertEqual(params.get("report_ref"), "sale.action_report_saleorder")
        self.assertEqual(params.get("res_model"), "sale.order")
        self.assertEqual(params.get("res_ids"), [so.id])
