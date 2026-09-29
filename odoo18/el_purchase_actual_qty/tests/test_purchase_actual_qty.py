from odoo.tests.common import TransactionCase


class TestPurchaseActualQty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vendor = cls.env["res.partner"].create({"name": "Actual Qty Vendor"})
        cls.product = cls.env["product.product"].create({
            "name": "Tomato",
            "is_storable": True,
            "purchase_method": "purchase",
        })

    def _line(self, ordered=100.0, actual=90.0, price=50.0):
        po = self.env["purchase.order"].create({"partner_id": self.vendor.id})
        line = self.env["purchase.order.line"].create({
            "order_id": po.id,
            "product_id": self.product.id,
            "product_qty": ordered,
            "actual_qty": actual,
            "price_unit": price,
        })
        return po, line

    def test_effective_cost_preserves_value(self):
        po, line = self._line()
        self.assertAlmostEqual(line.effective_price_unit, 5000.0 / 90.0, places=4)
        self.assertAlmostEqual(line.effective_price_unit * line.actual_qty, 5000.0, places=4)

    def test_variance(self):
        po, line = self._line()
        self.assertEqual(line.variance_qty, 10.0)
        self.assertAlmostEqual(line.variance_percent, 10.0, places=4)

    def test_bill_line_quantity_and_value(self):
        po, line = self._line()
        po.button_confirm()
        vals = line._prepare_account_move_line()
        self.assertAlmostEqual(vals["quantity"], 90.0, places=4)
        self.assertAlmostEqual(vals["quantity"] * vals["price_unit"], 5000.0, places=4)

    def test_receipt_quantity_and_value(self):
        po, line = self._line()
        po.button_confirm()
        move = po.picking_ids.move_ids.filtered(lambda m: m.product_id == self.product)[:1]
        self.assertTrue(move)
        self.assertAlmostEqual(move.product_uom_qty, 90.0, places=4)
        self.assertAlmostEqual(move.price_unit, 5000.0 / 90.0, places=4)
