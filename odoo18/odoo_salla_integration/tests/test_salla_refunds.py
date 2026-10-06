from odoo.addons.odoo_multi_channel_sale.tests.common import (
    TestMultiChannelCommon,
)
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestSallaRefunds(TestMultiChannelCommon):

    def setUp(self):
        super().setUp()
        self.channel.channel = 'salla'
        self.company = self.channel.company_id
        self.sale_journal = self.env['account.journal'].create({
            'name': 'Salla test sales', 'code': 'SLTS', 'type': 'sale', 'company_id': self.company.id})
        # no ZATCA checks in tests: the invoices of the connector flow go to the default sale journal
        if 'edi_format_ids' in self.sale_journal._fields:
            self.env['account.journal'].search([('type', '=', 'sale'), ('company_id', '=', self.company.id)]).write(
                {'edi_format_ids': [(5, 0, 0)]})
        self.bank_journal = self.env['account.journal'].create({
            'name': 'Salla test bank', 'code': 'SLTB', 'type': 'bank', 'company_id': self.company.id})
        self.partner = self.env['res.partner'].create({'name': 'Salla test customer'})
        self.zero_tax = self.env['account.tax'].create({
            'name': 'Salla refund test 0%', 'amount': 0, 'amount_type': 'percent',
            'type_tax_use': 'sale', 'company_id': self.company.id})
        self.product = self.env['product.product'].create({
            'name': 'Salla test service', 'type': 'service', 'invoice_policy': 'order', 'list_price': 100})

    def _order(self, ref, mapped=True, store_id=None):
        ref = 'SALLA-TEST-%s' % ref
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id, 'client_order_ref': ref, 'company_id': self.company.id,
            'order_line': [(0, 0, {'product_id': self.product.id, 'product_uom_qty': 1, 'price_unit': 100})],
        })
        order.action_confirm()
        if mapped:
            self.channel.create_order_mapping(order, store_id or 'st-%s' % ref, None, 'delivered')
        return order

    def _invoice(self, order, pay=False):
        invoice = order._create_invoices()
        invoice.write({'journal_id': self.sale_journal.id})
        invoice.action_post()
        if pay:
            wizard = self.env['account.payment.register'].with_context(
                active_model='account.move', active_ids=invoice.ids,
            ).create({'journal_id': self.bank_journal.id})
            wizard.action_create_payments()
            self.assertIn(invoice.payment_state, ('paid', 'in_payment'))
        return invoice

    def test_refund_paid_invoice_pays_the_money_back(self):
        order = self._order('R1')
        invoice = self._invoice(order, pay=True)
        notes = self.channel._salla_refund_order(order)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes.move_type, 'out_refund')
        self.assertEqual(notes.state, 'posted')
        self.assertEqual(notes.reversed_entry_id, invoice)
        self.assertIn(notes.payment_state, ('paid', 'in_payment'))
        refund = notes._get_reconciled_payments()
        self.assertEqual(refund.payment_type, 'outbound')
        self.assertEqual(refund.journal_id, self.bank_journal)
        self.assertEqual(refund.amount, invoice.amount_total)
        # a second call has nothing left to do
        self.assertFalse(self.channel._salla_refund_order(order))

    def test_refund_unpaid_invoice_closes_it(self):
        order = self._order('R2')
        invoice = self._invoice(order)
        notes = self.channel._salla_refund_order(order)
        self.assertEqual(len(notes), 1)
        self.assertEqual(invoice.payment_state, 'reversed')
        self.assertFalse(notes._get_reconciled_payments())
        self.assertFalse(self.channel._salla_refund_order(order))

    def test_restored_feed_action_creates_the_credit_note(self):
        order = self._order('R3', store_id='st-R3')
        invoice = self._invoice(order, pay=True)
        self.env['order.feed'].create({
            'channel_id': self.channel.id, 'store_id': 'st-R3', 'name': 'SALLA-TEST-R3', 'order_state': 'restored'})
        self.channel.salla_refund_restored_orders(store_ids=['st-R3'])
        note = order.invoice_ids.filtered(lambda m: m.move_type == 'out_refund')
        self.assertEqual(len(note), 1)
        self.assertEqual(note.reversed_entry_id, invoice)
        self.channel.salla_refund_restored_orders(store_ids=['st-R3'])
        self.assertEqual(len(order.invoice_ids.filtered(lambda m: m.move_type == 'out_refund')), 1)

    def test_existing_order_is_mapped_not_created_again(self):
        order = self._order('D1', mapped=False)
        feed = self.env['order.feed'].create({
            'channel_id': self.channel.id, 'store_id': 'st-D1', 'name': 'SALLA-TEST-D1', 'order_state': 'delivered'})
        mapping = feed._salla_existing_order_mapping(
            self.channel, {'client_order_ref': 'SALLA-TEST-D1', 'order_state': 'delivered'}, 'st-D1', None)
        self.assertTrue(mapping)
        self.assertEqual(mapping.order_name, order)
        self.assertEqual(mapping.store_order_id, 'st-D1')
        self.assertFalse(feed._salla_existing_order_mapping(
            self.channel, {'client_order_ref': 'SALLA-TEST-unknown'}, 'st-X', None))

    def test_duplicate_order_is_cancelled_with_its_payment_and_invoice(self):
        keep = self._order('D2')
        keep_invoice = self._invoice(keep, pay=True)
        dup = self._order('D2', mapped=False)
        dup_invoice = self._invoice(dup, pay=True)
        dup_payment = dup_invoice._get_reconciled_payments()
        self.channel.salla_cancel_duplicate_orders(refs=['SALLA-TEST-D2'])
        self.assertEqual(dup.state, 'cancel')
        self.assertIn(dup_payment.state, ('cancel', 'canceled'))
        self.assertEqual(dup_invoice.payment_state, 'reversed')
        self.assertEqual(keep.state, 'sale')
        self.assertIn(keep_invoice.payment_state, ('paid', 'in_payment'))
        self.assertEqual(len(keep.invoice_ids), 1)

    def test_paid_twin_is_kept_and_takes_the_mapping(self):
        mapped = self._order('D3', store_id='st-D3')
        twin = self._order('D3', mapped=False)
        twin_invoice = self._invoice(twin, pay=True)
        payment = twin_invoice._get_reconciled_payments()
        res = self.channel.salla_cancel_duplicate_orders(refs=['SALLA-TEST-D3'])
        self.assertNotIn('Failed', res['params']['message'], res['params']['message'])
        self.assertEqual(mapped.state, 'cancel')
        self.assertEqual(twin.state, 'sale')
        self.assertIn(twin_invoice.payment_state, ('paid', 'in_payment'))
        self.assertNotIn(payment.state, ('cancel', 'canceled'))
        self.assertFalse(twin.invoice_ids.filtered(lambda m: m.move_type == 'out_refund'))
        mapping = self.env['channel.order.mappings'].search([('store_order_id', '=', 'st-D3')])
        self.assertEqual(mapping.order_name, twin)
        self.assertEqual(mapping.odoo_order_id, twin.id)

    def test_unpaid_invoice_twin_is_kept_when_the_mapped_order_has_none(self):
        mapped = self._order('D4', store_id='st-D4')
        twin = self._order('D4', mapped=False)
        twin_invoice = self._invoice(twin)
        self.channel.salla_cancel_duplicate_orders(refs=['SALLA-TEST-D4'])
        self.assertEqual(mapped.state, 'cancel')
        self.assertEqual(twin.state, 'sale')
        self.assertEqual(twin_invoice.payment_state, 'not_paid')
        self.assertEqual(self.env['channel.order.mappings'].search([('store_order_id', '=', 'st-D4')]).order_name, twin)

    def test_unpaid_duplicate_invoice_is_reversed_when_the_kept_order_is_paid(self):
        keep = self._order('D5', store_id='st-D5')
        keep_invoice = self._invoice(keep, pay=True)
        twin = self._order('D5', mapped=False)
        twin_invoice = self._invoice(twin)
        self.channel.salla_cancel_duplicate_orders(refs=['SALLA-TEST-D5'])
        self.assertEqual(twin.state, 'cancel')
        self.assertEqual(twin_invoice.payment_state, 'reversed')
        self.assertIn(keep_invoice.payment_state, ('paid', 'in_payment'))

    def _untaxed(self, order):
        tax_field = 'tax_ids' if 'tax_ids' in order.order_line._fields else 'tax_id'
        order.order_line.write({tax_field: [(5, 0, 0)]})
        return order

    def test_untaxed_duplicate_invoice_is_reversed_with_the_zero_tax(self):
        self.channel.salla_zero_tax_id = self.zero_tax
        keep = self._order('D6', store_id='st-D6')
        self._invoice(keep, pay=True)
        twin = self._untaxed(self._order('D6', mapped=False))
        twin_invoice = self._invoice(twin, pay=True)
        self.assertFalse(twin_invoice.invoice_line_ids.tax_ids)
        res = self.channel.salla_cancel_duplicate_orders(refs=['SALLA-TEST-D6'])
        self.assertNotIn('Failed', res['params']['message'], res['params']['message'])
        self.assertEqual(twin.state, 'cancel')
        self.assertEqual(twin_invoice.payment_state, 'reversed')
        note = twin.invoice_ids.filtered(lambda m: m.move_type == 'out_refund')
        self.assertEqual(note.state, 'posted')
        self.assertEqual(note.invoice_line_ids.filtered(lambda l: l.display_type == 'product').tax_ids, self.zero_tax)
        self.assertEqual(note.amount_total, twin_invoice.amount_total)

    def test_untaxed_paid_invoice_is_refunded_with_the_zero_tax(self):
        self.channel.salla_zero_tax_id = self.zero_tax
        order = self._untaxed(self._order('R4'))
        invoice = self._invoice(order, pay=True)
        notes = self.channel._salla_refund_order(order)
        self.assertEqual(notes.state, 'posted')
        self.assertEqual(notes.invoice_line_ids.filtered(lambda l: l.display_type == 'product').tax_ids, self.zero_tax)
        self.assertEqual(notes.amount_total, invoice.amount_total)
        self.assertIn(notes.payment_state, ('paid', 'in_payment'))

    def _cancelled_copy_and_live_twin(self, ref, state, pay=True):
        """The connector's copy is mapped and cancelled, an older import left a live invoiced copy."""
        mapped = self._order(ref, store_id='st-%s' % ref)
        mapped._action_cancel()
        self.assertEqual(mapped.state, 'cancel')
        twin = self._order(ref, mapped=False)
        invoice = self._invoice(twin, pay=pay)
        self.env['order.feed'].create({
            'channel_id': self.channel.id, 'store_id': 'st-%s' % ref, 'name': 'SALLA-TEST-%s' % ref,
            'order_state': state})
        return mapped, twin, invoice

    def test_live_copy_of_a_cancelled_order_is_refunded_and_cancelled(self):
        self.env['channel.order.states'].create({
            'channel_id': self.channel.id, 'channel_state': 'canceled', 'odoo_order_state': 'cancelled'})
        mapped, twin, invoice = self._cancelled_copy_and_live_twin('T1', 'canceled')
        res = self.channel.salla_refund_restored_orders(store_ids=['st-T1'])
        self.assertNotIn('Failed', res['params']['message'], res['params']['message'])
        self.assertEqual(twin.state, 'cancel')
        self.assertEqual(mapped.state, 'cancel')
        note = twin.invoice_ids.filtered(lambda m: m.move_type == 'out_refund')
        self.assertEqual(note.state, 'posted')
        self.assertEqual(note.reversed_entry_id, invoice)
        refund = note._get_reconciled_payments()
        self.assertEqual(refund.payment_type, 'outbound')
        self.assertEqual(refund.amount, invoice.amount_total)
        self.assertEqual(self.channel.env['channel.order.mappings'].search(
            [('store_order_id', '=', 'st-T1')]).order_name, mapped)
        # nothing left to do on a second run
        self.channel.salla_refund_restored_orders(store_ids=['st-T1'])
        self.assertEqual(len(twin.invoice_ids.filtered(lambda m: m.move_type == 'out_refund')), 1)

    def test_live_copy_of_a_returned_order_takes_the_mapping(self):
        mapped, twin, invoice = self._cancelled_copy_and_live_twin('T2', 'restored')
        self.channel.salla_refund_restored_orders(store_ids=['st-T2'])
        self.assertEqual(twin.state, 'sale')
        note = twin.invoice_ids.filtered(lambda m: m.move_type == 'out_refund')
        self.assertEqual(note.reversed_entry_id, invoice)
        self.assertIn(note.payment_state, ('paid', 'in_payment'))
        self.assertEqual(self.channel.env['channel.order.mappings'].search(
            [('store_order_id', '=', 'st-T2')]).order_name, twin)

    def test_unpaid_live_copy_without_invoice_is_cancelled(self):
        self.env['channel.order.states'].create({
            'channel_id': self.channel.id, 'channel_state': 'canceled', 'odoo_order_state': 'cancelled'})
        mapped = self._order('T3', store_id='st-T3')
        mapped._action_cancel()
        twin = self._order('T3', mapped=False)
        self.env['order.feed'].create({
            'channel_id': self.channel.id, 'store_id': 'st-T3', 'name': 'SALLA-TEST-T3', 'order_state': 'canceled'})
        self.channel.salla_refund_restored_orders(store_ids=['st-T3'])
        self.assertEqual(twin.state, 'cancel')

    def test_import_lock_is_released_after_a_failed_job(self):
        import psycopg2
        from unittest.mock import patch
        cr = self.channel.env.cr
        real_execute = cr.execute
        calls = {'n': 0}

        def execute(query, params=None, log_exceptions=True):
            if 'pg_advisory_unlock' in str(query) and not calls['n']:
                calls['n'] += 1
                raise psycopg2.errors.InFailedSqlTransaction('current transaction is aborted')
            return real_execute(query, params, log_exceptions)

        self.assertTrue(self.channel._salla_try_acquire_order_import_lock())
        with patch.object(cr, 'execute', side_effect=execute), patch.object(cr, 'rollback') as rollback:
            self.assertTrue(self.channel._salla_release_order_import_lock())
        rollback.assert_called_once()
        # really released: nothing left to unlock
        self.assertFalse(self.channel._salla_release_order_import_lock())

    def test_posting_lock_is_taken_on_hash_locked_journals_only(self):
        locked = self.env['account.journal'].create({
            'name': 'Salla hashed sales', 'code': 'SLHS', 'type': 'sale', 'company_id': self.company.id,
            'restrict_mode_hash_table': True})

        def held(journal):
            self.env.cr.execute("""
                SELECT count(*) FROM pg_locks
                 WHERE locktype = 'advisory' AND pid = pg_backend_pid() AND classid = 714002 AND objid = %s
            """, (journal.id,))
            return self.env.cr.fetchone()[0]

        self.channel._salla_lock_journal_posting(locked | self.sale_journal)
        self.assertTrue(held(locked))
        self.assertFalse(held(self.sale_journal))
        # an invoice still posts and refunds normally while the lock is held by this transaction
        order = self._order('L1')
        invoice = self._invoice(order, pay=True)
        self.assertTrue(self.channel._salla_refund_order(order))
        self.assertIn(invoice.payment_state, ('paid', 'in_payment'))

    def _grouped(self, pay=True):
        first, second = self._order('G1'), self._order('G2')
        second.order_line.price_unit = 50
        invoice = (first | second)._create_invoices()
        self.assertEqual(len(invoice), 1)
        invoice.write({'journal_id': self.sale_journal.id})
        invoice.action_post()
        if pay:
            self.env['account.payment.register'].with_context(
                active_model='account.move', active_ids=invoice.ids,
            ).create({'journal_id': self.bank_journal.id}).action_create_payments()
        return first, second, invoice

    def test_return_of_a_grouped_order_credits_its_lines_only(self):
        first, second, invoice = self._grouped()
        note = self.channel._salla_refund_order(first)
        self.assertEqual(len(note), 1)
        self.assertEqual(note.reversed_entry_id, invoice)
        self.assertEqual(note.amount_total, first.amount_total)
        self.assertEqual(note.invoice_line_ids.sale_line_ids.order_id, first)
        refund = note._get_reconciled_payments()
        self.assertEqual(refund.amount, first.amount_total)
        self.assertEqual(self.channel._salla_order_net(first), 0)
        self.assertEqual(self.channel._salla_order_net(second), second.amount_total)
        self.assertFalse(self.channel._salla_standing_invoices(first))
        self.assertEqual(self.channel._salla_standing_invoices(second), invoice)
        # the other order comes back later: its own lines only
        other = self.channel._salla_refund_order(second)
        self.assertEqual(other.amount_total, second.amount_total)
        self.assertEqual(self.channel._salla_order_net(second), 0)
        self.assertFalse(self.channel._salla_refund_order(first))

    def test_return_of_a_grouped_unpaid_order_leaves_the_rest_open(self):
        first, second, invoice = self._grouped(pay=False)
        self.channel._salla_refund_order(first)
        self.assertEqual(invoice.amount_residual, second.amount_total)

    def test_duplicate_on_a_grouped_invoice_keeps_the_other_order(self):
        keep = self._order('GD')
        self._invoice(keep, pay=True)
        twin, other = self._order('GD', mapped=False), self._order('GD2')
        other.order_line.price_unit = 70
        invoice = (twin | other)._create_invoices()
        invoice.write({'journal_id': self.sale_journal.id})
        invoice.action_post()
        self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=invoice.ids,
        ).create({'journal_id': self.bank_journal.id}).action_create_payments()
        self.channel.salla_cancel_duplicate_orders(refs=[keep.client_order_ref])
        self.assertEqual(twin.state, 'cancel')
        self.assertEqual(self.channel._salla_order_net(twin), 0)
        self.assertEqual(self.channel._salla_order_net(other), other.amount_total)
        payment = invoice._get_reconciled_payments()
        self.assertEqual(len(payment), 1)
        self.assertNotIn(payment.state, ('cancel', 'canceled', 'rejected'))

    def test_free_order_invoice_stands(self):
        order = self._order('Z1')
        order.order_line.price_unit = 0
        invoice = self._invoice(order)
        self.assertEqual(invoice.amount_total, 0)
        self.assertEqual(self.channel._salla_standing_invoices(order), invoice)
        # a credited free order has nothing standing
        self.channel._salla_refund_order(order)
        self.assertFalse(self.channel._salla_standing_invoices(order))

    def test_order_with_no_sale_in_salla_is_credited_and_cancelled(self):
        order = self._order('NS1')
        invoice = self._invoice(order)
        self.channel.salla_credit_orders([order.client_order_ref], cancel=True)
        note = order.invoice_ids.filtered(lambda m: m.move_type == 'out_refund')
        self.assertEqual(note.state, 'posted')
        self.assertEqual(note.reversed_entry_id, invoice)
        self.assertEqual(invoice.payment_state, 'reversed')
        self.assertEqual(order.state, 'cancel')
        self.assertEqual(self.channel._salla_order_net(order), 0)
        # nothing left to do the second time
        self.channel.salla_credit_orders([order.client_order_ref], cancel=True)
        self.assertEqual(len(order.invoice_ids.filtered(lambda m: m.move_type == 'out_refund')), 1)

    def test_manual_copy_of_an_invoice_is_credited(self):
        order = self._order('MC1')
        self._invoice(order, pay=True)
        copy = self.env['account.move'].create({
            'move_type': 'out_invoice', 'partner_id': self.partner.id, 'journal_id': self.sale_journal.id,
            'invoice_line_ids': [(0, 0, {'name': 'manual copy', 'quantity': 1, 'price_unit': 100})],
        })
        copy.action_post()
        self.channel.salla_credit_invoices([copy.name])
        self.assertEqual(copy.payment_state, 'reversed')
        note = self.env['account.move'].search([('reversed_entry_id', '=', copy.id)])
        self.assertEqual(note.state, 'posted')
        self.assertEqual(note.amount_total, copy.amount_total)
        # the order keeps its own paid invoice, a second call does nothing
        self.assertEqual(self.channel._salla_order_net(order), order.amount_total)
        self.channel.salla_credit_invoices([copy.name])
        self.assertEqual(self.env['account.move'].search_count([('reversed_entry_id', '=', copy.id)]), 1)

    def test_return_credit_note_dated_like_salla(self):
        order = self._order('LS1')
        invoice = self._invoice(order, pay=True)
        invoice_date = invoice.invoice_date
        self.env['ir.config_parameter'].sudo().set_param('odoo_salla_integration.returns_on_invoice_date', '1')
        note = self.channel._salla_refund_order(order, refund_date=invoice_date.replace(year=invoice_date.year + 1))
        self.assertEqual(note.invoice_date, invoice_date)
        refund = note._get_reconciled_payments()
        self.assertEqual(refund.date, invoice_date.replace(year=invoice_date.year + 1))
