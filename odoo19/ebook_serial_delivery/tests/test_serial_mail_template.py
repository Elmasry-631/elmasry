# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSerialMailTemplate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.default_template = cls.env.ref('ebook_serial_delivery.mail_template_ebook_serial')
        warehouse = cls.env['stock.warehouse'].search([('company_id', '=', cls.company.id)], limit=1)
        cls.ebook = cls.env['product.product'].create({
            'name': 'Mail eBook',
            'type': 'consu',
            'is_storable': True,
            'tracking': 'serial',
            'is_ebook_with_codes': True,
        })
        for serial in ('MAIL-001', 'MAIL-002'):
            lot = cls.env['stock.lot'].create({'name': serial, 'product_id': cls.ebook.id})
            cls.env['stock.quant'].with_context(inventory_mode=True).create({
                'product_id': cls.ebook.id,
                'location_id': warehouse.lot_stock_id.id,
                'lot_id': lot.id,
                'inventory_quantity': 1,
            }).action_apply_inventory()
        cls.partner = cls.env['res.partner'].create({'name': 'Mail Customer', 'email': 'mail.customer@example.com'})

    def _confirm_ebook_order(self):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {'product_id': self.ebook.id, 'product_uom_qty': 1})],
        })
        order.action_confirm()
        return order

    def _order_mails(self, order):
        return self.env['mail.mail'].search([('model', '=', 'sale.order'), ('res_id', '=', order.id)])

    def test_default_template(self):
        self.assertEqual(self.company.ebook_serial_mail_template_id, self.default_template)
        order = self._confirm_ebook_order()
        self.assertEqual(order.picking_ids.state, 'done')
        self.assertTrue(order.picking_ids.ebook_email_sent)
        self.assertTrue(self._order_mails(order))

    def test_template_chosen_in_settings_is_sent(self):
        custom = self.default_template.copy({
            'name': 'Custom eBook email',
            'subject': 'Custom {{ object.name }}',
            'body_html': '<p>Your codes:</p><t t-out="object.ebook_serial_numbers_html"/>',
        })
        self.env['res.config.settings'].create({'ebook_serial_mail_template_id': custom.id}).execute()
        self.assertEqual(self.company.ebook_serial_mail_template_id, custom)

        order = self._confirm_ebook_order()
        serial = order.picking_ids.move_line_ids.lot_id.name
        mail = self._order_mails(order)
        self.assertEqual(mail.subject, 'Custom %s' % order.name)
        self.assertIn(serial, mail.body_html)

    def test_serial_numbers_placeholder(self):
        order = self._confirm_ebook_order()
        serial = order.picking_ids.move_line_ids.lot_id.name
        self.assertIn(serial, order.ebook_serial_numbers_html)
        self.assertIn(self.ebook.display_name, order.ebook_serial_numbers_html)

    def test_empty_setting_falls_back_to_default(self):
        self.company.ebook_serial_mail_template_id = False
        self.assertEqual(self.company._get_ebook_serial_mail_template(), self.default_template)
        action = self.env['res.config.settings'].create({}).action_open_ebook_serial_mail_template()
        self.assertEqual(action['res_id'], self.default_template.id)
