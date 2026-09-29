# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.tests import new_test_user


@tagged('post_install', '-at_install')
class TestSaleOrderConfirmationUser(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_a = new_test_user(
            cls.env, login='confirm_user_a', groups='sales_team.group_sale_salesman')
        cls.user_b = new_test_user(
            cls.env, login='confirm_user_b', groups='sales_team.group_sale_salesman')
        cls.user_c = new_test_user(
            cls.env, login='confirm_user_c', groups='sales_team.group_sale_manager')

        cls.partner = cls.env['res.partner'].create({'name': 'Confirmation Test Partner'})
        cls.product = cls.env['product.product'].create({
            'name': 'Confirmation Test Product',
            'list_price': 100.0,
        })

    def _create_order(self, user):
        return self.env['sale.order'].with_user(user).create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
            })],
        })

    def test_01_confirmed_by_set_to_confirming_user(self):
        """1-3: create as User A, confirm as User B -> confirmed_by_id == User B."""
        order = self._create_order(self.user_a)
        order.with_user(self.user_b).action_confirm()
        self.assertEqual(order.confirmed_by_id, self.user_b)
        self.assertNotEqual(order.confirmed_by_id, order.create_uid)

    def test_02_group_by_and_filter_confirmed_by(self):
        """4-6: second quotation confirmed by User C; verify group by and filter."""
        order_b = self._create_order(self.user_a)
        order_b.with_user(self.user_b).action_confirm()
        order_c = self._create_order(self.user_a)
        order_c.with_user(self.user_c).action_confirm()

        groups = self.env['sale.order'].read_group(
            [('id', 'in', (order_b | order_c).ids)],
            ['confirmed_by_id'], ['confirmed_by_id'],
        )
        grouped_user_ids = {g['confirmed_by_id'][0] for g in groups if g['confirmed_by_id']}
        self.assertEqual(grouped_user_ids, {self.user_b.id, self.user_c.id})

        filtered = self.env['sale.order'].search([('confirmed_by_id', '=', self.user_b.id)])
        self.assertIn(order_b, filtered)
        self.assertNotIn(order_c, filtered)

    def test_03_confirmed_by_readonly_via_write(self):
        """7: confirmed_by_id cannot be changed through a normal write()."""
        order = self._create_order(self.user_a)
        order.with_user(self.user_b).action_confirm()
        original = order.confirmed_by_id
        order.write({'confirmed_by_id': self.user_a.id, 'client_order_ref': 'no-op'})
        self.assertEqual(order.confirmed_by_id, original)

    def test_04_confirmed_by_not_copied(self):
        """8: copying a confirmed order must not copy confirmed_by_id."""
        order = self._create_order(self.user_a)
        order.with_user(self.user_b).action_confirm()
        duplicate = order.copy()
        self.assertFalse(duplicate.confirmed_by_id)

    def test_05_batch_confirmation(self):
        """9: confirming several quotations at once stamps them all."""
        order_1 = self._create_order(self.user_a)
        order_2 = self._create_order(self.user_a)
        (order_1 | order_2).with_user(self.user_c).action_confirm()
        self.assertEqual(order_1.confirmed_by_id, self.user_c)
        self.assertEqual(order_2.confirmed_by_id, self.user_c)

    def test_06_programmatic_confirmation(self):
        """10: calling action_confirm() directly from code (not the UI button)."""
        order = self._create_order(self.user_a)
        order.with_user(self.user_b).action_confirm()
        self.assertEqual(order.confirmed_by_id, self.user_b)

    def test_07_reconfirmation_after_cancel(self):
        """11: cancel -> reset to draft -> reconfirm by a different user."""
        order = self._create_order(self.user_a)
        order.with_user(self.user_b).action_confirm()
        order.with_user(self.user_b).action_cancel()
        order.with_user(self.user_b).action_draft()
        order.with_user(self.user_c).action_confirm()
        self.assertEqual(order.confirmed_by_id, self.user_c)

    def test_08_idempotent_confirm_does_not_overwrite(self):
        """Calling action_confirm() again on an already-'sale' order must not
        reset confirmed_by_id to the new caller."""
        order = self._create_order(self.user_a)
        order.with_user(self.user_b).action_confirm()
        order.with_user(self.user_c).action_confirm()
        self.assertEqual(order.confirmed_by_id, self.user_b)

    def test_09_pre_existing_order_not_backfilled(self):
        """12: an order confirmed before this module existed (state forced to
        'sale' without going through action_confirm) must keep confirmed_by_id
        empty rather than being backfilled from create_uid/write_uid."""
        order = self._create_order(self.user_a)
        order.sudo().write({'state': 'sale'})
        self.assertFalse(order.confirmed_by_id)
