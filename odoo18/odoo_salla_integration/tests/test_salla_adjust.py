# -*- coding: utf-8 -*-
from odoo.addons.odoo_multi_channel_sale.tests.common import (
    TestMultiChannelCommon,
)
from unittest.mock import patch

from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestSallaAdjust(TestMultiChannelCommon):

    def setUp(self):
        super().setUp()
        self.channel.channel = 'salla'
        self.company = self.channel.company_id
        self.sale_journal = self.env['account.journal'].create({
            'name': 'Salla adjust sales', 'code': 'SLAJ', 'type': 'sale', 'company_id': self.company.id})
        # no ZATCA checks in tests: the invoices of the connector flow go to the default sale journal
        if 'edi_format_ids' in self.sale_journal._fields:
            self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', self.company.id)]).write(
                {'edi_format_ids': [(5, 0, 0)]})
        self.bank_journal = self.env['account.journal'].create({
            'name': 'Salla adjust bank', 'code': 'SLJB', 'type': 'bank', 'company_id': self.company.id})
        self.partner = self.env['res.partner'].create({'name': 'Salla adjust customer'})
        self.vat = self.env['account.tax'].create({
            'name': 'Salla adjust VAT 15%', 'amount': 15, 'amount_type': 'percent', 'type_tax_use': 'sale',
            'company_id': self.company.id})
        self.zero = self.env['account.tax'].create({
            'name': 'Salla adjust 0%', 'amount': 0, 'amount_type': 'percent', 'type_tax_use': 'sale',
            'company_id': self.company.id})
        self.channel.salla_zero_tax_id = self.zero
        self.product = self.env['product.product'].create({
            'name': 'Salla adjust item', 'type': 'service', 'invoice_policy': 'order', 'list_price': 100,
            'taxes_id': [(5, 0, 0)]})
        self.tax_field = 'tax_ids' if 'tax_ids' in self.env['sale.order.line']._fields else 'tax_id'

    def _order(self, ref, lines):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id, 'client_order_ref': ref, 'company_id': self.company.id,
            'order_line': [(0, 0, {'product_id': self.product.id, 'name': name, 'product_uom_qty': 1,
                                   'price_unit': price, self.tax_field: [(6, 0, taxes.ids)]})
                           for name, price, taxes in lines],
        })
        order.action_confirm()
        invoice = order._create_invoices()
        invoice.write({'journal_id': self.sale_journal.id})
        invoice.action_post()
        self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=invoice.ids,
        ).create({'journal_id': self.bank_journal.id}).action_create_payments()
        return order, invoice

    def _net(self, order):
        return self.channel._salla_order_net(order)

    def test_lower_salla_total_gives_a_refunded_credit_note(self):
        # Salla: coupon went from 50 to 60 -> (380 - 60) * 1.15 = 368; Odoo invoiced 379.50
        order, invoice = self._order('ADJ-1', [('item', 380, self.vat), ('coupon', -50, self.vat)])
        self.assertAlmostEqual(self._net(order), 379.5)
        note = self.channel._salla_adjust_order_total(order, 368.0)
        self.assertEqual(note.move_type, 'out_refund')
        self.assertEqual(note.state, 'posted')
        self.assertAlmostEqual(note.amount_total, 11.5)
        self.assertEqual(note.reversed_entry_id, invoice)
        self.assertEqual(note.invoice_date, invoice.invoice_date)
        self.assertEqual(note.invoice_line_ids.tax_ids, self.vat)
        self.assertAlmostEqual(self._net(order), 368.0)
        self.assertAlmostEqual(order.amount_total, 368.0)
        refund = note._get_reconciled_payments()
        self.assertEqual(refund.payment_type, 'outbound')
        self.assertEqual(refund.journal_id, self.bank_journal)
        self.assertAlmostEqual(refund.amount, 11.5)
        self.assertEqual(order.invoice_status, 'invoiced')
        # nothing left to do
        self.assertFalse(self.channel._salla_adjust_order_total(order, 368.0))

    def test_higher_salla_total_gives_a_paid_invoice(self):
        order, invoice = self._order('ADJ-2', [('item', 380, self.vat)])
        move = self.channel._salla_adjust_order_total(order, 496.31)   # + shipping 51.57 with VAT
        self.assertEqual(move.move_type, 'out_invoice')
        self.assertAlmostEqual(move.amount_total, 59.31)
        self.assertIn(move.payment_state, ('paid', 'in_payment'))
        self.assertAlmostEqual(self._net(order), 496.31)
        if 'debit_origin_id' in move._fields:
            self.assertEqual(move.debit_origin_id, invoice)

    def test_every_cent_is_reached(self):
        # 0.01 cannot be the total of a base plus 15% of it: the base moves until the line fits
        for index, target in enumerate((437.01, 436.99, 1000.07, 3066.02)):
            order, _invoice = self._order('ADJ-C%d' % index, [('item', 380, self.vat)])
            self.channel._salla_adjust_order_total(order, target)
            self.assertAlmostEqual(self._net(order), target, places=2)

    def test_zero_rated_order_is_adjusted_without_vat(self):
        order, _invoice = self._order('ADJ-3', [('item', 435.44, self.zero), ('shipping', 181.41, self.zero)])
        note = self.channel._salla_adjust_order_total(order, 468.44)
        self.assertEqual(note.invoice_line_ids.tax_ids, self.zero)
        self.assertAlmostEqual(note.amount_total, 148.41)
        self.assertAlmostEqual(self._net(order), 468.44)

    def test_mixed_vat_invoice_is_rebuilt(self):
        # old import: product line without VAT, coupon and shipping with VAT -> total 2.31, Salla 59.31
        order, invoice = self._order('ADJ-4', [('item', 380, self.env['account.tax']), ('coupon', -380, self.vat),
                                                ('shipping', 51.57, self.vat)])
        self.assertAlmostEqual(invoice.amount_total, 2.31)
        new = self.channel._salla_adjust_order_total(order, 59.31)
        self.assertEqual(invoice.payment_state, 'reversed')
        self.assertEqual(new.move_type, 'out_invoice')
        self.assertAlmostEqual(new.amount_total, 59.31)
        self.assertAlmostEqual(new.amount_tax, 7.74)
        self.assertIn(new.payment_state, ('paid', 'in_payment'))
        self.assertAlmostEqual(self._net(order), 59.31)
        self.assertTrue(all(line[self.tax_field] == self.vat for line in order.order_line))

    def test_locked_order_is_adjusted_and_locked_again(self):
        order, _invoice = self._order('ADJ-5', [('item', 380, self.vat)])
        order.action_lock()
        self.channel._salla_adjust_order_total(order, 400.0)
        self.assertTrue(order.locked)
        self.assertAlmostEqual(self._net(order), 400.0)

    def test_audit_brings_totals_to_salla(self):
        from unittest.mock import patch
        from .test_salla_audit import FakeSallaApi, row, CURRENCY
        self.channel.state = 'validate'
        self.env['channel.order.states'].create({
            'channel_id': self.channel.id, 'channel_state': 'delivered', 'odoo_order_state': 'done',
            'odoo_create_invoice': True, 'odoo_set_invoice_state': 'paid'})
        order, _invoice = self._order('ADJ-6', [('item', 380, self.vat), ('coupon', -50, self.vat)])
        self.channel.create_order_mapping(order, 'S-ADJ-6', None, 'delivered')
        CURRENCY['name'] = order.currency_id.name
        audit = self.env['salla.order.audit'].create({
            'channel_id': self.channel.id, 'date_from': '2026-01-01', 'date_to': '2026-01-31'})
        audit.action_start()
        api = FakeSallaApi([[row('S-ADJ-6', 'ADJ-6', 'delivered', 368.0)]])
        with patch.object(type(self.channel), 'getAccessToken', lambda *a, **k: True), \
                patch.object(type(self.channel), 'get_sallaApi', lambda *a, **k: api):
            audit._process(600)
        self.assertEqual(audit.line_ids.category, 'amount_diff')
        audit.action_adjust_totals()
        audit._process(600)
        self.assertEqual(audit.state, 'done')
        self.assertEqual(audit.line_ids.category, 'ok', audit.line_ids.fix_error)
        self.assertAlmostEqual(self._net(order), 368.0)

    def test_blocked_journal_parameters_are_accepted(self):
        order, invoice = self._order('ADJ-7', [('item', 380, self.vat)])
        self.env['order.feed'].create({
            'channel_id': self.channel.id, 'store_id': 'st-ADJ-7', 'name': 'ADJ-7', 'order_state': 'restored'})
        self.channel.create_order_mapping(order, 'st-ADJ-7', None, 'restored')
        res = self.channel.salla_refund_restored_orders(store_ids=['st-ADJ-7'], include_blocked=True)
        self.assertNotIn('Failed', res['params']['message'], res['params']['message'])
        self.assertTrue(order.invoice_ids.filtered(lambda m: m.move_type == 'out_refund' and m.state == 'posted'))
        res = self.channel.salla_cancel_duplicate_orders(refs=['ADJ-7'], include_blocked=True)
        self.assertNotIn('Failed', res['params']['message'], res['params']['message'])
        res = self.channel.salla_report_missing_einvoices(dry_run=True)
        self.assertTrue(res['params']['message'])

    def test_rebuild_posts_its_credit_note_with_zero_tax_on_the_untaxed_line(self):
        order, invoice = self._order('ADJ-8', [('item', 380, self.env['account.tax']), ('coupon', -380, self.vat),
                                                ('shipping', 51.57, self.vat)])
        self.channel._salla_adjust_order_total(order, 59.31)
        note = order.invoice_ids.filtered(lambda m: m.move_type == 'out_refund' and m.reversed_entry_id == invoice)
        self.assertEqual(note.state, 'posted')
        self.assertEqual(note.invoice_line_ids.filtered(lambda l: l.price_unit == 380).tax_ids, self.zero)
        self.assertAlmostEqual(self._net(order), 59.31)

    def test_lowering_credit_note_has_positive_quantity_and_price(self):
        order, _invoice = self._order('ADJ-9', [('item', 380, self.vat), ('coupon', -50, self.vat)])
        note = self.channel._salla_adjust_order_total(order, 368.0)
        line = note.invoice_line_ids.filtered(lambda l: l.display_type == 'product')
        self.assertEqual(line.quantity, 1)
        self.assertGreater(line.price_unit, 0)
        self.assertAlmostEqual(note.amount_total, 11.5)
        self.assertEqual(order.invoice_status, 'invoiced')

    def test_zatca_price_of_a_switched_credit_note_line_is_positive(self):
        order, _invoice = self._order('ADJ-10', [('item', 380, self.vat)])
        self.env['sale.order.line'].create({
            'order_id': order.id, 'product_id': self.product.id, 'product_uom_qty': 1, 'price_unit': -100,
            self.tax_field: [(6, 0, self.vat.ids)]})
        note = order._create_invoices(final=True)
        self.assertEqual(note.move_type, 'out_refund')
        line = note.invoice_line_ids.filtered(lambda l: l.display_type == 'product')
        self.assertLess(line.quantity, 0)
        vals = self.env['account.edi.xml.ubl_21.zatca']._get_invoice_line_price_vals(line)
        self.assertAlmostEqual(vals['price_amount'], 100)

    def _grouped(self, price_a, price_b, pay=True):
        orders = self.env['sale.order']
        for index, price in enumerate((price_a, price_b)):
            order = self.env['sale.order'].create({
                'partner_id': self.partner.id, 'client_order_ref': 'GRP-%d-%s' % (index, price),
                'company_id': self.company.id,
                'order_line': [(0, 0, {'product_id': self.product.id, 'name': 'item', 'product_uom_qty': 1,
                                       'price_unit': price, self.tax_field: [(6, 0, self.vat.ids)]})],
            })
            order.action_confirm()
            orders |= order
        invoice = orders._create_invoices()
        self.assertEqual(len(invoice), 1)
        invoice.write({'journal_id': self.sale_journal.id})
        invoice.action_post()
        if pay:
            self.env['account.payment.register'].with_context(
                active_model='account.move', active_ids=invoice.ids,
            ).create({'journal_id': self.bank_journal.id}).action_create_payments()
        return orders[0], orders[1], invoice

    def test_grouped_invoice_counts_each_order_for_its_lines(self):
        first, second, invoice = self._grouped(100, 200)
        self.assertAlmostEqual(invoice.amount_total, 345)
        self.assertAlmostEqual(self._net(first), 115)
        self.assertAlmostEqual(self._net(second), 230)
        self.assertEqual(self.channel._salla_standing_invoices(first), invoice)

    def test_adjustment_of_a_grouped_order_moves_its_own_part(self):
        first, second, invoice = self._grouped(100, 200)
        note = self.channel._salla_adjust_order_total(first, 103.5)
        self.assertAlmostEqual(note.amount_total, 11.5)
        self.assertEqual(note.reversed_entry_id, invoice)
        self.assertAlmostEqual(self._net(first), 103.5)
        self.assertAlmostEqual(self._net(second), 230)
        # the invoice still bills the order: a second adjustment finds it
        self.assertEqual(self.channel._salla_standing_invoices(first), invoice)
        debit = self.channel._salla_adjust_order_total(first, 115)
        self.assertEqual(debit.move_type, 'out_invoice')
        self.assertAlmostEqual(self._net(first), 115)

    def test_rebuild_refuses_a_grouped_invoice(self):
        first, _second, _invoice = self._grouped(100, 200)
        with self.assertRaises(ValueError):
            self.channel._salla_rebuild_order_invoice(first, 115)

    def _zatca_journal(self):
        zatca = self.env['account.edi.format'].search([('code', '=', 'sa_zatca')], limit=1)
        if not zatca or 'l10n_sa_compliance_checks_passed' not in self.sale_journal._fields:
            self.skipTest('Saudi e-invoicing is not installed')
        self.sale_journal.write({'edi_format_ids': [(6, 0, zatca.ids)], 'l10n_sa_compliance_checks_passed': True})
        return zatca

    def test_held_corrections_get_no_zatca_document(self):
        zatca = self._zatca_journal()
        Format = type(zatca)
        with patch.object(Format, '_check_move_configuration', lambda self, move: []), \
                patch.object(Format, '_get_move_applicability',
                             lambda self, move: {'post': lambda moves: {}} if self.code == 'sa_zatca' else None):
            order, invoice = self._order('ADJ-H1', [('item', 380, self.vat)])
            self.assertTrue(self.channel._salla_zatca_docs(invoice), 'posting in the journal creates the document')
            self.env['ir.config_parameter'].sudo().set_param('odoo_salla_integration.hold_zatca', '1')
            note = self.channel._salla_adjust_order_total(order, 368.0)
            self.assertEqual(note.state, 'posted')
            self.assertFalse(self.channel._salla_zatca_docs(note))
            self.assertTrue(any('on hold' in (body or '') for body in note.message_ids.mapped('body')))
            # hold lifted: a correction of a sent invoice goes to ZATCA again
            self.env['ir.config_parameter'].sudo().set_param('odoo_salla_integration.hold_zatca', '')
            debit = self.channel._salla_adjust_order_total(order, 391.0)
            self.assertEqual(self.channel._salla_zatca_docs(debit).state, 'to_send')

    def test_export_order_taxed_by_mistake_is_invoiced_again_at_zero(self):
        # Salla: no VAT on the order (export); the invoice put 15% on one line
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id, 'client_order_ref': 'ADJ-X1', 'company_id': self.company.id,
            'order_line': [(0, 0, {'product_id': self.product.id, 'name': name, 'product_uom_qty': 1,
                                   'price_unit': price, self.tax_field: [(5, 0, 0)]})
                           for name, price in (('item A', 300), ('item B', 200))],
        })
        order.action_confirm()
        invoice = order._create_invoices()
        invoice.write({'journal_id': self.sale_journal.id})
        lines = invoice.invoice_line_ids.filtered(lambda l: l.display_type == 'product')
        lines[0].tax_ids = self.vat
        lines[1].tax_ids = self.zero
        invoice.action_post()
        self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=invoice.ids,
        ).create({'journal_id': self.bank_journal.id}).action_create_payments()
        self.assertAlmostEqual(invoice.amount_total, 545)
        self.channel._salla_adjust_order_total(order, 500.0)
        self.assertAlmostEqual(self._net(order), 500)
        new = order.invoice_ids.filtered(lambda m: m.move_type == 'out_invoice' and m.state == 'posted' and m != invoice)
        self.assertEqual(len(new), 1)
        self.assertEqual(new.invoice_line_ids.filtered(lambda l: l.display_type == 'product').tax_ids, self.zero)
        self.assertIn(new.payment_state, ('paid', 'in_payment'))
        refund = self.env['account.payment'].search([
            ('payment_type', '=', 'outbound'), ('partner_id', '=', self.partner.id), ('memo', 'like', 'ADJ-X1')])
        self.assertAlmostEqual(refund.amount, 45)
        self.assertEqual(refund.journal_id, self.bank_journal)

    def test_connector_tax_takes_the_tax_account_and_grids(self):
        account = self.env['account.account'].create({
            'name': 'Salla test VAT output', 'code': 'SLVAT1', 'account_type': 'liability_current'})
        tag = self.env['account.account.tag'].create({'name': 'Salla test grid', 'applicability': 'taxes'})
        self.vat.invoice_repartition_line_ids.filtered(lambda l: l.repartition_type == 'tax').write(
            {'account_id': account.id, 'tag_ids': [(6, 0, tag.ids)]})
        self.vat.refund_repartition_line_ids.filtered(lambda l: l.repartition_type == 'tax').write({'account_id': account.id})
        self.vat.invoice_repartition_line_ids.filtered(lambda l: l.repartition_type == 'base').write({'tag_ids': [(6, 0, tag.ids)]})
        bare = self.env['account.tax'].create({
            'name': 'Salla Tax 15.0%', 'amount': 15, 'amount_type': 'percent', 'type_tax_use': 'sale',
            'company_id': self.company.id})
        self.channel._salla_complete_taxes(bare)
        lines = (bare.invoice_repartition_line_ids | bare.refund_repartition_line_ids).filtered(lambda l: l.repartition_type == 'tax')
        self.assertTrue(all(line.account_id for line in lines))
        self.assertTrue(bare.invoice_repartition_line_ids.tag_ids)
