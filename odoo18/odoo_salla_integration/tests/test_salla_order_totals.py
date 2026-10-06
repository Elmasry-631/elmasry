# -*- coding: utf-8 -*-
from datetime import timedelta
from unittest.mock import patch

from odoo import fields
from odoo.addons.odoo_multi_channel_sale.tests.common import (
    TestMultiChannelCommon,
)
from odoo.tests import tagged

VAT15 = "[{'included_in_price': False, 'rate': 15.0, 'tax_type': 'percent'}]"


class FakeSweepApi:
    import_url = 'https://salla.test/'

    def __init__(self, rows, per_page):
        self.rows, self.per_page, self.pages, self.params = rows, per_page, [], []

    def salla_response(self, endpoint, method='GET', data=None, params=None, headers=None):
        """The order list of the requested creation dates, as Salla pages it."""
        page = (params or {}).get('page', 1)
        self.pages.append(page)
        self.params.append(dict(params or {}))
        rows = self.rows[(page - 1) * self.per_page:page * self.per_page]
        more = page * self.per_page < len(self.rows)
        return {'data': rows, 'pagination': {'links': {'next': 'x'} if more else {}}}


@tagged('post_install', '-at_install')
class TestSallaOrderTotals(TestMultiChannelCommon):

    def setUp(self):
        super().setUp()
        self.channel.channel = 'salla'
        self.channel.state = 'validate'
        self.company = self.channel.company_id
        # no ZATCA checks in tests: the invoices of the connector flow go to the default sale journal
        if 'edi_format_ids' in self.env['account.journal']._fields:
            self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', self.company.id)]).write(
                {'edi_format_ids': [(5, 0, 0)]})
        self.bank_journal = self.env['account.journal'].create({
            'name': 'Salla totals bank', 'code': 'SLTB', 'type': 'bank', 'company_id': self.company.id})
        self.partner = self.env['res.partner'].create({'name': 'Salla totals customer'})
        self.vat = self.env['account.tax'].create({
            'name': 'Salla totals VAT 15%', 'amount': 15, 'amount_type': 'percent', 'type_tax_use': 'sale',
            'company_id': self.company.id})
        self.zero = self.env['account.tax'].create({
            'name': 'Salla totals 0%', 'amount': 0, 'amount_type': 'percent', 'type_tax_use': 'sale',
            'company_id': self.company.id})
        self.channel.salla_zero_tax_id = self.zero
        self.product = self.env['product.product'].create({
            'name': 'Salla totals item', 'type': 'service', 'invoice_policy': 'order', 'list_price': 100,
            'taxes_id': [(5, 0, 0)]})
        # the items sell on their own income account, not the one an adjustment line would take
        Account = self.env['account.account']
        company_field = ('company_ids', [(6, 0, self.company.ids)]) if 'company_ids' in Account._fields \
            else ('company_id', self.company.id)
        self.sales_account = Account.create({'name': 'Salla totals sales', 'code': '700991',
                                             'account_type': 'income', company_field[0]: company_field[1]})
        self.product.with_company(self.company).property_account_income_id = self.sales_account
        self.tax_field = 'tax_ids' if 'tax_ids' in self.env['sale.order.line']._fields else 'tax_id'
        self.currency = self.env['sale.order'].new({
            'partner_id': self.partner.id, 'company_id': self.company.id}).currency_id.name
        self.skeleton = self.env['multi.channel.skeleton']

    def _order(self, ref, lines):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id, 'client_order_ref': ref, 'company_id': self.company.id,
            'order_line': [(0, 0, {'product_id': self.product.id, 'name': name, 'product_uom_qty': 1,
                                   'price_unit': price, self.tax_field: [(6, 0, taxes.ids)]})
                           for name, price, taxes in lines],
        })
        order.action_confirm()
        return order

    def _feed(self, ref, lines):
        """Order feed holding Salla's lines as the connector stores them (discounts positive)."""
        return self.env['order.feed'].create({
            'channel_id': self.channel.id, 'store_id': 'S-' + ref, 'name': ref,
            'line_ids': [(0, 0, {
                'line_name': name, 'line_price_unit': str(price), 'line_product_uom_qty': '1',
                'line_source': source, 'line_taxes': taxes,
                'line_product_id': 'P-1' if source == 'product' else False,
                'line_variant_ids': 'No Variants' if source == 'product' else False,
            }) for name, price, source, taxes in lines],
        })

    def _row(self, store_id, ref, status, total, created=None):
        row = {'id': store_id, 'reference_id': ref, 'status': {'slug': status},
               'total': {'amount': total, 'currency': self.currency}}
        if created:
            row['date'] = {'date': '%s 10:00:00' % created}
        return row

    def _invoice(self, order):
        res = self.skeleton._salla_set_order_paid(order, self.bank_journal.id, fields.Date.today(), channel=self.channel)
        self.assertTrue(res.get('status'), res)
        return order.invoice_ids.filtered(lambda m: m.state == 'posted')

    def _adjust_lines(self, order):
        return order.order_line.filtered(lambda l: l.product_id.default_code == 'SALLA-ADJUST')

    def test_feed_total(self):
        feed = self._feed('OT-0', [('item', 444.35, 'product', VAT15), ('KSA', 100, 'discount', VAT15),
                                   ('Delivery', 41, 'delivery', VAT15), ('export item', 10, 'product', False)])
        self.assertAlmostEqual(self.channel._salla_feed_total(feed), 453.15)

    def test_coupon_added_after_the_import_is_on_the_first_invoice(self):
        # imported at 511 (444.35 + VAT); the coupon KSA (-100 before VAT) came later in Salla: 396
        order = self._order('OT-1', [('item', 444.35, self.vat)])
        self._feed('OT-1', [('item', 444.35, 'product', VAT15), ('KSA', 100, 'discount', VAT15)])
        invoice = self._invoice(order)
        self.assertEqual(len(invoice), 1)
        self.assertAlmostEqual(invoice.amount_total, 396.0)
        self.assertAlmostEqual(invoice.amount_tax, 51.65)
        line = self._adjust_lines(order)
        self.assertEqual(len(line), 1)
        self.assertEqual(line[self.tax_field], self.vat)
        self.assertAlmostEqual(line.price_total, -115.0)
        self.assertIn(invoice.payment_state, ('paid', 'in_payment'))
        # one income account for the whole sale, the adjustment included
        sold = invoice.invoice_line_ids.filtered(lambda l: l.display_type == 'product')
        self.assertEqual(len(sold), 2)
        self.assertEqual(sold.account_id, self.sales_account)

    def test_coupon_removed_after_the_import_raises_the_first_invoice(self):
        order = self._order('OT-2', [('item', 444.35, self.vat), ('KSA', -100, self.vat)])
        self.assertAlmostEqual(order.amount_total, 396.0)
        self._feed('OT-2', [('item', 444.35, 'product', VAT15)])
        self.assertAlmostEqual(self._invoice(order).amount_total, 511.0)

    def test_order_like_its_feed_is_not_touched(self):
        order = self._order('OT-3', [('item', 444.35, self.vat)])
        self._feed('OT-3', [('item', 444.35, 'product', VAT15)])
        self.assertAlmostEqual(self._invoice(order).amount_total, 511.0)
        self.assertFalse(self._adjust_lines(order))

    def test_total_read_by_the_sweep_wins(self):
        order = self._order('OT-4', [('item', 444.35, self.vat)])
        self._feed('OT-4', [('item', 444.35, 'product', VAT15)])
        self.skeleton = self.skeleton.with_context(salla_order_totals={'OT-4': (400.0, self.currency)})
        self.assertAlmostEqual(self._invoice(order).amount_total, 400.0)

    def test_mixed_vat_order_is_left_to_the_daily_check(self):
        order = self._order('OT-5', [('item', 444.35, self.vat), ('export item', 50, self.zero)])
        self._feed('OT-5', [('item', 444.35, 'product', VAT15), ('KSA', 100, 'discount', VAT15),
                            ('export item', 50, 'product', False)])
        self.assertAlmostEqual(self._invoice(order).amount_total, 561.0)
        self.assertFalse(self._adjust_lines(order))

    def test_adjustment_follows_salla_until_the_invoice(self):
        order = self._order('OT-6', [('item', 444.35, self.vat)])
        self.channel._salla_bring_order_to_total(order, 396.0)
        self.assertAlmostEqual(order.amount_total, 396.0)
        self.channel._salla_bring_order_to_total(order, 443.15)   # changed again in Salla
        self.assertAlmostEqual(order.amount_total, 443.15)
        self.assertEqual(len(self._adjust_lines(order)), 1)
        self.channel._salla_bring_order_to_total(order, 511.0)    # back to the imported total
        self.assertAlmostEqual(order.amount_total, 511.0)

    def test_sweep_reimports_status_and_total_changes_of_the_last_days(self):
        today = fields.Date.context_today(self.channel)
        rows = []
        # orders in sync fill the first pages (2 orders a page in this test)
        for index in range(12):
            ref = 'SW-%02d' % index
            order = self._order(ref, [('item', 100, self.vat)])
            self.channel.create_order_mapping(order, 'S' + ref, None, 'under_review')
            rows.append(self._row('S' + ref, ref, 'under_review', 115.0))
        status = self._order('SW-STATUS', [('item', 100, self.vat)])
        self.channel.create_order_mapping(status, 'S-STATUS', None, 'under_review')
        rows.append(self._row('S-STATUS', 'SW-STATUS', 'completed', 115.0))
        coupon = self._order('SW-COUPON', [('item', 444.35, self.vat)])
        self.channel.create_order_mapping(coupon, 'S-COUPON', None, 'under_review')
        rows.append(self._row('S-COUPON', 'SW-COUPON', 'under_review', 396.0))
        invoiced = self._order('SW-INV', [('item', 444.35, self.vat)])
        invoiced._create_invoices().action_post()
        self.channel.create_order_mapping(invoiced, 'S-INV', None, 'completed')
        rows.append(self._row('S-INV', 'SW-INV', 'completed', 396.0))
        rows.append(self._row('S-NEW', 'SW-NEW', 'under_review', 50.0, created=today))
        # never imported and older than two days: left to the order import and the daily check
        rows.append(self._row('S-OLD', 'SW-OLD', 'completed', 50.0, created=today - timedelta(days=5)))
        api = FakeSweepApi(rows, 2)
        imported = []

        def fake_import(operation, **kw):
            imported.extend(kw['object_id'].split(','))
            self.assertEqual(operation.env.context['salla_order_totals']['SW-COUPON'], (396.0, self.currency))

        Channel = type(self.channel)
        with patch('odoo.addons.odoo_salla_integration.models.multi_channel_sale.SALLA_UPDATED_SWEEP_PER_PAGE', 2), \
                patch.object(Channel, 'getAccessToken', lambda *a, **k: True), \
                patch.object(Channel, 'get_sallaApi', lambda *a, **k: api), \
                patch.object(type(self.env['import.operation']), 'import_with_filter', fake_import), \
                patch.object(self.env.cr, 'commit', lambda *a, **k: None):   # the sweep commits per chunk
            self.channel.salla_sweep_updated_orders()
        self.assertEqual(set(imported), {'S-STATUS', 'S-COUPON', 'S-NEW'})
        self.assertEqual(api.pages, list(range(1, 10)))   # every page: the coupon change sits on page 7
        self.assertEqual(api.params[0]['from_date'], str(today - timedelta(days=14)))
        self.assertEqual(api.params[0]['sort_by'], 'created_at-desc')
        self.assertAlmostEqual(coupon.amount_total, 396.0)
        self.assertAlmostEqual(invoiced.amount_total, 511.0)
