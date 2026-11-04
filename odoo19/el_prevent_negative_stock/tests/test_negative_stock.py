"""Tests for el_prevent_negative_stock module."""
from odoo.tests import TransactionCase, tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestPreventNegativeStock(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env.ref('product.product_product_4')
        cls.location = cls.env.ref('stock.stock_location_stock')
        cls.dest_location = cls.env.ref('stock.stock_location_customers')
        cls.picking_type = cls.env.ref('stock.picking_type_out')
        existing = cls.env['stock.quant'].search([
            ('product_id', '=', cls.product.id),
            ('location_id', '=', cls.location.id),
        ])
        existing.unlink()

    def _add_stock(self, qty):
        self.env['stock.quant'].create({
            'product_id': self.product.id,
            'location_id': self.location.id,
            'quantity': qty,
        })

    def _create_picking(self, qty):
        picking = self.env['stock.picking'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
            'picking_type_id': self.picking_type.id,
            'location_id': self.location.id,
            'location_dest_id': self.dest_location.id,
        })
        self.env['stock.move'].create({
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'picking_id': picking.id,
            'location_id': self.location.id,
            'location_dest_id': self.dest_location.id,
            'picking_type_id': self.picking_type.id,
            'product_uom_qty': qty,
        })
        return picking

    def test_01_sufficient_stock(self):
        """Picking should confirm+assign when enough stock."""
        self._add_stock(100)
        picking = self._create_picking(50)
        picking.action_confirm()
        self.assertEqual(picking.state, 'assigned')

    def test_02_insufficient_stock_rejected(self):
        """Picking should be rejected when not enough stock."""
        self._add_stock(10)
        picking = self._create_picking(50)
        with self.assertRaises(UserError):
            picking.action_confirm()

    def test_03_zero_stock_rejected(self):
        """Picking should be rejected when no stock at all."""
        picking = self._create_picking(10)
        with self.assertRaises(UserError):
            picking.action_confirm()

    def test_04_exact_quantity(self):
        """Exact available quantity should pass."""
        self._add_stock(50)
        picking = self._create_picking(50)
        picking.action_confirm()
        self.assertEqual(picking.state, 'assigned')

    def test_05_multiple_products_mixed(self):
        """Mixed picking: one product sufficient, one insufficient → rejected."""
        self._add_stock(100)
        product2 = self.env.ref('product.product_product_5')
        existing2 = self.env['stock.quant'].search([
            ('product_id', '=', product2.id),
            ('location_id', '=', self.location.id),
        ])
        existing2.unlink()

        picking = self.env['stock.picking'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
            'picking_type_id': self.picking_type.id,
            'location_id': self.location.id,
            'location_dest_id': self.dest_location.id,
        })
        # Move 1: sufficient stock
        self.env['stock.move'].create({
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'picking_id': picking.id,
            'location_id': self.location.id,
            'location_dest_id': self.dest_location.id,
            'picking_type_id': self.picking_type.id,
            'product_uom_qty': 50,
        })
        # Move 2: insufficient stock (product2 has 0)
        self.env['stock.move'].create({
            'product_id': product2.id,
            'product_uom': product2.uom_id.id,
            'picking_id': picking.id,
            'location_id': self.location.id,
            'location_dest_id': self.dest_location.id,
            'picking_type_id': self.picking_type.id,
            'product_uom_qty': 50,
        })
        with self.assertRaises(UserError):
            picking.action_confirm()


@tagged('post_install', '-at_install')
class TestPreventNegativeStockSale(TransactionCase):
    """Tests for sale order blocking."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env.ref('product.product_product_4')
        cls.location = cls.env.ref('stock.stock_location_stock')
        # Clear existing stock
        existing = cls.env['stock.quant'].search([
            ('product_id', '=', cls.product.id),
            ('location_id', '=', cls.location.id),
        ])
        existing.unlink()

    def _add_stock(self, qty):
        self.env['stock.quant'].create({
            'product_id': self.product.id,
            'location_id': self.location.id,
            'quantity': qty,
        })

    def _create_sale_order(self, qty):
        """Create a sale order with one line."""
        order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
        })
        self.env['sale.order.line'].create({
            'order_id': order.id,
            'product_id': self.product.id,
            'product_uom_qty': qty,
            'price_unit': 100.0,
        })
        return order

    def test_10_sale_with_sufficient_stock(self):
        """Sale should confirm when enough stock."""
        self._add_stock(100)
        order = self._create_sale_order(50)
        order.action_confirm()
        self.assertEqual(order.state, 'sale')

    def test_11_sale_with_insufficient_stock_blocked(self):
        """Sale should be blocked when not enough stock."""
        self._add_stock(10)
        order = self._create_sale_order(50)
        with self.assertRaises(UserError):
            order.action_confirm()

    def test_12_sale_with_zero_stock_blocked(self):
        """Sale should be blocked when no stock at all."""
        order = self._create_sale_order(10)
        with self.assertRaises(UserError):
            order.action_confirm()

    def test_13_sale_exact_quantity_allowed(self):
        """Sale with exact available quantity should pass."""
        self._add_stock(50)
        order = self._create_sale_order(50)
        order.action_confirm()
        self.assertEqual(order.state, 'sale')

    def test_14_sale_blocked_with_clear_message(self):
        """Sale block should produce clear error."""
        self._add_stock(5)
        order = self._create_sale_order(20)
        try:
            order.action_confirm()
            self.fail('Should have raised UserError')
        except UserError as e:
            # Verify the error message contains key info
            msg = str(e)
            self.assertIn('Negative Stock', msg)
            self.assertIn(self.product.display_name, msg)
