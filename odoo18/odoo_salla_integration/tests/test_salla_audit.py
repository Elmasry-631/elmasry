from unittest.mock import patch

from odoo.addons.odoo_multi_channel_sale.tests.common import (
    TestMultiChannelCommon,
)
from odoo.tests import tagged


class FakeSallaApi:
    import_url = 'https://salla.test/'

    def __init__(self, pages):
        self.pages = pages
        self.calls = []

    def salla_response(self, endpoint, method='GET', data=None, params=None, headers=None):
        """Pages of the given rows restricted to the requested date window, like Salla."""
        params = params or {}
        self.calls.append(dict(params))
        window = [[r for r in page if params['from_date'] <= r['date']['date'][:10] <= params['to_date']]
                  for page in self.pages]
        window = [p for p in window if p]
        page = params.get('page', 1)
        rows = window[page - 1] if page <= len(window) else []
        return {'data': rows, 'pagination': {'links': {'next': 'x'} if page < len(window) else {}}}


CURRENCY = {'name': 'SAR'}


def row(store_id, ref, status, total, currency=None, date='2026-01-05 10:00:00', method='mada'):
    currency = currency or CURRENCY['name']
    return {'id': store_id, 'reference_id': ref, 'status': {'slug': status, 'name': status},
            'total': {'amount': total, 'currency': currency}, 'date': {'date': date}, 'payment_method': method}


@tagged('post_install', '-at_install')
class TestSallaAudit(TestMultiChannelCommon):

    def setUp(self):
        super().setUp()
        self.channel.channel = 'salla'
        self.channel.state = 'validate'
        self.company = self.channel.company_id

        self.env['channel.order.states'].create([
            {'channel_id': self.channel.id, 'channel_state': 'delivered', 'odoo_order_state': 'done',
             'odoo_create_invoice': True, 'odoo_set_invoice_state': 'paid'},
            {'channel_id': self.channel.id, 'channel_state': 'restored', 'odoo_order_state': 'sale'},
            {'channel_id': self.channel.id, 'channel_state': 'canceled', 'odoo_order_state': 'cancelled'},
        ])
        self.sale_journal = self.env['account.journal'].create({
            'name': 'Salla audit sales', 'code': 'SLAS', 'type': 'sale', 'company_id': self.company.id})
        # no ZATCA checks in tests: the invoices of the connector flow go to the default sale journal
        if 'edi_format_ids' in self.sale_journal._fields:
            self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', self.company.id)]).write(
                {'edi_format_ids': [(5, 0, 0)]})
        self.bank_journal = self.env['account.journal'].create({
            'name': 'Salla audit bank', 'code': 'SLAB', 'type': 'bank', 'company_id': self.company.id})
        self.partner = self.env['res.partner'].create({'name': 'Salla audit customer'})
        # rows use the currency a new order of this partner gets (pricelist currency)
        CURRENCY['name'] = self.env['sale.order'].new({
            'partner_id': self.partner.id, 'company_id': self.company.id}).currency_id.name
        self.product = self.env['product.product'].create({
            'name': 'Salla audit service', 'type': 'service', 'invoice_policy': 'order',
            'list_price': 100, 'taxes_id': [(5, 0, 0)]})

    def _order(self, ref, store_id=None, status='delivered', price=100):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id, 'client_order_ref': ref, 'company_id': self.company.id,
            'order_line': [(0, 0, {'product_id': self.product.id, 'product_uom_qty': 1, 'price_unit': price})],
        })
        order.action_confirm()
        if store_id:
            self.channel.create_order_mapping(order, store_id, None, status)
        return order

    def _invoice(self, order, pay=False):
        invoice = order._create_invoices()
        invoice.write({'journal_id': self.sale_journal.id})
        invoice.action_post()
        if pay:
            self.env['account.payment.register'].with_context(
                active_model='account.move', active_ids=invoice.ids,
            ).create({'journal_id': self.bank_journal.id}).action_create_payments()
        return invoice

    def _run(self, pages):
        audit = self.env['salla.order.audit'].create({
            'channel_id': self.channel.id, 'date_from': '2026-01-01', 'date_to': '2026-01-31'})
        audit.action_start()
        api = FakeSallaApi(pages)
        with patch.object(type(self.channel), 'getAccessToken', lambda *a, **k: True), \
                patch.object(type(self.channel), 'get_sallaApi', lambda *a, **k: api):
            audit._process(600)
        return audit, api

    def test_list_and_compare(self):
        ok = self._order('A-OK', 'S-OK')
        self._invoice(ok, pay=True)
        unpaid = self._order('A-UNPAID', 'S-UNPAID')
        self._invoice(unpaid)
        self._order('A-NOINV', 'S-NOINV')
        returned = self._order('A-RET', 'S-RET', status='restored')
        self._invoice(returned, pay=True)
        self._order('A-DUP', 'S-DUP')
        self._order('A-DUP')
        self._order('A-UNMAPPED')
        amount = self._order('A-AMT', 'S-AMT', price=90)
        self._invoice(amount, pay=True)
        pages = [
            [row('S-OK', 'A-OK', 'delivered', 100), row('S-UNPAID', 'A-UNPAID', 'delivered', 100),
             row('S-NOINV', 'A-NOINV', 'delivered', 100)],
            [row('S-RET', 'A-RET', 'restored', 100), row('S-DUP', 'A-DUP', 'delivered', 100),
             row('S-UNMAPPED', 'A-UNMAPPED', 'delivered', 100)],
            [row('S-AMT', 'A-AMT', 'delivered', 100, date='2026-01-20 09:00:00'),
             row('S-MISSING', 'A-MISSING', 'delivered', 50, date='2026-01-29 09:00:00'),
             row('S-OK', 'A-OK', 'delivered', 100)],   # repeated row across pages is listed once
        ]
        audit, api = self._run(pages)
        self.assertEqual(audit.state, 'done')
        # one query per page of each week of January (5 weeks), the first week has 3 pages
        self.assertEqual([c['from_date'] for c in api.calls],
                         ['2026-01-01'] * 3 + ['2026-01-08', '2026-01-15', '2026-01-22', '2026-01-29'])
        self.assertEqual(api.calls[-1]['to_date'], '2026-01-31')
        cat = {l.reference: l.category for l in audit.line_ids}
        self.assertEqual(len(audit.line_ids), 8)
        self.assertEqual(cat, {
            'A-OK': 'ok', 'A-UNPAID': 'not_paid', 'A-NOINV': 'not_invoiced', 'A-RET': 'should_refund',
            'A-DUP': 'duplicate', 'A-UNMAPPED': 'unmapped', 'A-AMT': 'amount_diff', 'A-MISSING': 'missing',
        })
        self.assertIn('OK: 1 order(s)', audit.summary)
        # the importer gets everything it can fix, not the duplicate or the amount difference
        audit.action_import_problems()
        import json
        ids = json.loads(audit.backfill_id.order_ids_json)
        self.assertEqual(sorted(ids), sorted(['S-RET', 'S-UNMAPPED', 'S-MISSING']))
        self.assertEqual(audit.backfill_id.state, 'running')

    def test_compare_again_after_a_fix(self):
        unpaid = self._order('B-1', 'SB-1')
        invoice = self._invoice(unpaid)
        audit, _api = self._run([[row('SB-1', 'B-1', 'delivered', 100)]])
        self.assertEqual(audit.line_ids.category, 'not_paid')
        self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=invoice.ids,
        ).create({'journal_id': self.bank_journal.id}).action_create_payments()
        audit.action_compare_again()
        audit._process(600)
        self.assertEqual(audit.line_ids.category, 'ok')
        self.assertEqual(audit.line_ids.invoice_state, 'paid')

    def test_invoice_and_pay(self):
        mapping_model = self.env['channel.account.journal.mappings']
        mapping_model.create({'channel_id': self.channel.id, 'store_journal_name': 'mada', 'odoo_journal': self.bank_journal.id,
                              'odoo_journal_id': self.bank_journal.id})
        noinv = self._order('C-1', 'SC-1')
        unpaid = self._order('C-2', 'SC-2')
        invoice = self._invoice(unpaid)
        for ref, store in (('C-1', 'SC-1'), ('C-2', 'SC-2')):
            self.env['order.feed'].create({'channel_id': self.channel.id, 'store_id': store, 'name': ref,
                                           'order_state': 'delivered', 'payment_method': 'mada'})
        audit, _api = self._run([[row('SC-1', 'C-1', 'delivered', 100), row('SC-2', 'C-2', 'delivered', 100)]])
        self.assertEqual(sorted(audit.line_ids.mapped('category')), ['not_invoiced', 'not_paid'])
        audit.action_fix_invoices()
        self.assertEqual(audit.state, 'fixing')
        audit._process(600)
        self.assertEqual(audit.state, 'done')
        self.assertEqual(audit.line_ids.mapped('category'), ['ok', 'ok'], audit.line_ids.mapped('fix_error'))
        self.assertIn(invoice.payment_state, ('paid', 'in_payment'))
        new_invoice = noinv.invoice_ids.filtered(lambda m: m.move_type == 'out_invoice')
        self.assertEqual(new_invoice.state, 'posted')
        self.assertEqual(new_invoice.invoice_date, noinv.date_order.date())
        payment = new_invoice._get_reconciled_payments()
        self.assertEqual(payment.journal_id, self.bank_journal)
        self.assertEqual(payment.date, new_invoice.invoice_date)

    def test_cancelled_in_both_is_ok(self):
        order = self._order('E-1', 'SE-1', status='canceled')
        order.with_context(disable_cancel_warning=True, from_webhook=True).action_cancel()
        still_missing = self._order('E-2', status='delivered')
        still_missing.with_context(disable_cancel_warning=True, from_webhook=True).action_cancel()
        audit, _api = self._run([[row('SE-1', 'E-1', 'canceled', 100), row('SE-2', 'E-2', 'delivered', 100)]])
        cat = {l.reference: l.category for l in audit.line_ids}
        self.assertEqual(cat, {'E-1': 'ok', 'E-2': 'missing'})

    def _fix_setup(self, ref, store):
        if not self.env['channel.account.journal.mappings'].search([('channel_id', '=', self.channel.id)]):
            self.env['channel.account.journal.mappings'].create({
                'channel_id': self.channel.id, 'store_journal_name': 'mada',
                'odoo_journal': self.bank_journal.id, 'odoo_journal_id': self.bank_journal.id})
        self.env['order.feed'].create({'channel_id': self.channel.id, 'store_id': store, 'name': ref,
                                       'order_state': 'delivered', 'payment_method': 'mada'})

    def test_untaxed_order_is_invoiced_with_the_zero_tax(self):
        zero = self.env['account.tax'].create({'name': 'Audit 0%', 'amount': 0, 'amount_type': 'percent',
                                               'type_tax_use': 'sale', 'company_id': self.company.id})
        self.channel.salla_zero_tax_id = zero
        order = self._order('F-1', 'SF-1')
        tax_field = 'tax_ids' if 'tax_ids' in order.order_line._fields else 'tax_id'
        self.assertFalse(order.order_line[tax_field])
        self._fix_setup('F-1', 'SF-1')
        audit, _api = self._run([[row('SF-1', 'F-1', 'delivered', 100)]])
        audit.action_fix_invoices()
        audit._process(600)
        self.assertEqual(audit.line_ids.category, 'ok', audit.line_ids.fix_error)
        invoice = order.invoice_ids.filtered(lambda m: m.move_type == 'out_invoice')
        self.assertEqual(invoice.state, 'posted')
        self.assertEqual(invoice.invoice_line_ids.tax_ids, zero)
        self.assertEqual(order.order_line[tax_field], zero)

    def test_numbered_draft_is_replaced_by_a_new_invoice(self):
        order = self._order('F-2', 'SF-2')
        old = self._invoice(order)
        old.button_draft()
        self.assertTrue(old.name and old.name != '/')
        self._fix_setup('F-2', 'SF-2')
        audit, _api = self._run([[row('SF-2', 'F-2', 'delivered', 100)]])
        self.assertEqual(audit.line_ids.category, 'not_invoiced')
        audit.action_fix_invoices()
        audit._process(600)
        self.assertEqual(audit.line_ids.category, 'ok', audit.line_ids.fix_error)
        self.assertEqual(old.state, 'cancel')
        new = order.invoice_ids.filtered(lambda m: m.move_type == 'out_invoice' and m.state == 'posted')
        self.assertEqual(len(new), 1)
        self.assertNotEqual(new, old)
        self.assertIn(new.payment_state, ('paid', 'in_payment'))
        self.assertEqual(new.invoice_date, order.date_order.date())

    def test_invoice_date_is_the_local_day_of_the_order(self):
        self.channel.wk_time_zone = 'Asia/Riyadh'
        order = self._order('G-1', 'SG-1')
        order.date_order = '2026-02-07 23:34:45'   # 02:34 on 8 February in Riyadh
        self._fix_setup('G-1', 'SG-1')
        audit, _api = self._run([[row('SG-1', 'G-1', 'delivered', 100)]])
        audit.action_fix_invoices()
        audit._process(600)
        invoice = order.invoice_ids.filtered(lambda m: m.move_type == 'out_invoice')
        self.assertEqual(str(invoice.invoice_date), '2026-02-08')
        self.assertEqual(str(invoice._get_reconciled_payments().date), '2026-02-08')

    def test_currency_rounding_and_credited_returns_are_ok(self):
        foreign = self.env['res.currency'].with_context(active_test=False).search([('name', '=', 'QAR')], limit=1)
        foreign.active = True
        pricelist = self.env['product.pricelist'].create({'name': 'Audit QAR', 'currency_id': foreign.id})
        rounded = self.env['sale.order'].create({
            'partner_id': self.partner.id, 'client_order_ref': 'R-QAR', 'company_id': self.company.id,
            'pricelist_id': pricelist.id,
            'order_line': [(0, 0, {'product_id': self.product.id, 'product_uom_qty': 1, 'price_unit': 100})],
        })
        rounded.action_confirm()
        self.channel.create_order_mapping(rounded, 'SR-QAR', None, 'delivered')
        self.assertEqual(rounded.currency_id, foreign)
        self._invoice(rounded, pay=True)
        returned = self._order('R-RET', 'SR-RET', status='restored', price=120)
        invoice = self._invoice(returned)
        self.channel._salla_refund_order(returned)
        self.assertEqual(invoice.payment_state, 'reversed')
        audit, _api = self._run([[row('SR-QAR', 'R-QAR', 'delivered', 100.3, currency='QAR'),
                                  row('SR-RET', 'R-RET', 'restored', 100)]])
        cat = {l.reference: l.category for l in audit.line_ids}
        self.assertEqual(cat, {'R-QAR': 'ok', 'R-RET': 'ok'}, audit.line_ids.mapped('issues'))

    def test_status_mismatch_is_imported_again(self):
        order = self._order('I-1', 'SI-1', status='restored')
        audit, _api = self._run([[row('SI-1', 'I-1', 'delivered', 100)]])
        self.assertEqual(audit.line_ids.category, 'not_invoiced')
        self.assertIn('Odoo status restored', audit.line_ids.issues)
        audit.action_import_problems()
        import json
        self.assertEqual(json.loads(audit.backfill_id.order_ids_json), ['SI-1'])
        self.assertTrue(order)

    def test_zero_residual_invoice_counts_as_paid(self):
        order = self._order('Z-1', 'SZ-1')
        invoice = self._invoice(order, pay=True)
        # what Odoo leaves on some KWD/OMR invoices: nothing left to pay, state still partial
        invoice.write({'payment_state': 'partial'})
        self.assertTrue(invoice.currency_id.is_zero(invoice.amount_residual))
        self.assertTrue(self.channel._salla_invoice_settled(invoice))
        audit, _api = self._run([[row('SZ-1', 'Z-1', 'delivered', 100)]])
        self.assertEqual(audit.line_ids.category, 'ok', audit.line_ids.issues)
        res = self.env['multi.channel.skeleton']._salla_set_order_paid(order, self.bank_journal.id, order.date_order,
                                                                       channel=self.channel)
        self.assertTrue(res['status'], res)
        self.assertEqual(len(order.invoice_ids), 1)

    def test_invoiced_net_is_compared_and_returned_totals_ignored(self):
        order = self._order('N-1', 'SN-1', price=90)
        invoice = order._create_invoices()
        invoice.write({'journal_id': self.sale_journal.id})
        invoice.invoice_line_ids.write({'price_unit': 100})
        invoice.action_post()
        self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=invoice.ids,
        ).create({'journal_id': self.bank_journal.id}).action_create_payments()
        self._order('N-2', 'SN-2', status='restored', price=120)
        audit, _api = self._run([[row('SN-1', 'N-1', 'delivered', 100), row('SN-2', 'N-2', 'restored', 150)]])
        cat = {l.reference: l.category for l in audit.line_ids}
        self.assertEqual(cat, {'N-1': 'ok', 'N-2': 'ok'}, audit.line_ids.mapped('issues'))
        self.assertEqual(audit.line_ids.filtered(lambda l: l.reference == 'N-1').odoo_total, 100)

    def test_order_emptied_by_a_grouped_reversal_is_invoiced_again(self):
        self.env['channel.account.journal.mappings'].create({
            'channel_id': self.channel.id, 'store_journal_name': 'mada', 'odoo_journal': self.bank_journal.id,
            'odoo_journal_id': self.bank_journal.id})
        returned = self._order('W-1', 'SW-1', status='restored', price=100)
        kept = self._order('W-2', 'SW-2', price=60)
        invoice = (returned | kept)._create_invoices()
        invoice.write({'journal_id': self.sale_journal.id})
        invoice.action_post()
        self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=invoice.ids,
        ).create({'journal_id': self.bank_journal.id}).action_create_payments()
        # an older refund credited the whole grouped invoice
        note = invoice._reverse_moves(default_values_list=[{'ref': 'old full refund'}], cancel=False)
        note.action_post()
        for ref, store, status in (('W-1', 'SW-1', 'restored'), ('W-2', 'SW-2', 'delivered')):
            self.env['order.feed'].create({'channel_id': self.channel.id, 'store_id': store, 'name': ref,
                                           'order_state': status, 'payment_method': 'mada'})
        audit, _api = self._run([[row('SW-1', 'W-1', 'restored', 100), row('SW-2', 'W-2', 'delivered', 60)]])
        cat = {l.reference: l.category for l in audit.line_ids}
        self.assertEqual(cat, {'W-1': 'ok', 'W-2': 'not_invoiced'}, audit.line_ids.mapped('issues'))
        audit.action_fix_invoices()
        audit._process(600)
        cat = {l.reference: l.category for l in audit.line_ids}
        self.assertEqual(cat, {'W-1': 'ok', 'W-2': 'ok'}, audit.line_ids.mapped('fix_error'))
        new = kept.invoice_ids.filtered(lambda m: m.move_type == 'out_invoice' and m != invoice)
        self.assertEqual(len(new), 1)
        self.assertEqual(new.amount_total, 60)
        self.assertEqual(new.invoice_line_ids.sale_line_ids.order_id, kept)
        self.assertIn(new.payment_state, ('paid', 'in_payment'))
        self.assertEqual(self.channel._salla_order_net(kept), 60)
        self.assertEqual(self.channel._salla_order_net(returned), 0)

    def test_free_order_is_ok(self):
        free = self._order('F-1', 'SF-1', price=0)
        self._invoice(free, pay=False)
        audit, _api = self._run([[row('SF-1', 'F-1', 'delivered', 0)]])
        self.assertEqual(audit.line_ids.category, 'ok', audit.line_ids.issues)
