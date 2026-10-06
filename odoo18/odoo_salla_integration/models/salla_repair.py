# -*- coding: utf-8 -*-
"""One-off repairs, run from the server actions "Salla: ..." (Action menu of the channel).

- salla_repair_zero_tax_invoices: posted, unpaid customer invoices of Salla orders whose lines
  carry no tax get the channel's 0% tax and are posted again; the feed cron then registers
  the payment.
- salla_fix_dates: the channel time zone becomes Asia/Riyadh, order dates are recomputed from
  the Salla order date (they were stored as if Salla sent UTC) and connector payments are moved
  to the invoice date, so date-based reports line up.
"""
import logging

import odoo

import pytz
from dateutil import parser

from odoo import api, models

_logger = logging.getLogger(__name__)
SALLA_TZ = 'Asia/Riyadh'


class MultiChannelSale(models.Model):
    _inherit = 'multi.channel.sale'

    def _salla_repair_notify(self, title, lines):
        message = '\n'.join(lines)
        _logger.info('%s: %s', title, message)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {'title': title, 'message': message, 'sticky': True, 'type': 'info'},
        }

    def _salla_repair_commit(self):
        if self.env.registry.in_test_mode() or getattr(odoo.modules.module, 'current_test', None) or odoo.tools.config['test_enable']:
            return
        self.env.cr.commit()

    @api.model
    def salla_repair_zero_tax_invoices(self, limit=500):
        """Posted, unpaid Salla invoices whose lines carry no tax.

        Entries of a Saudi sales journal are hash-locked once posted, so they cannot go back
        to draft: the invoice is reversed with a credit note (0% tax on its lines), the credit
        note is reconciled with it, and a new invoice with the 0% tax is created from the sale
        order and posted on the original invoice date. The feed cron then registers the payment
        on the new invoice. Invoices that can still be reset to draft are simply fixed in place.
        """
        SaleLine = self.env['sale.order.line']
        tax_field = 'tax_ids' if 'tax_ids' in SaleLine._fields else 'tax_id'
        fixed, failed, paid, not_ready = [], [], [], {}
        channels = self.search([('channel', '=', 'salla'), ('salla_zero_tax_id', '!=', False)])
        if not channels:
            return self._salla_repair_notify('Salla repair', ['Set "Tax for Salla lines without tax" on the Salla channel first.'])
        for channel in channels:
            zero = channel.salla_zero_tax_id
            base_domain = [
                ('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
                ('payment_state', '=', 'not_paid'), ('company_id', '=', channel.company_id.id),
                ('invoice_line_ids', 'any', [('display_type', '=', 'product'), ('tax_ids', '=', False)]),
                ('invoice_line_ids.sale_line_ids.order_id.channel_mapping_ids.channel_id', '=', channel.id),
            ]
            # journals with the e-invoicing format but no ZATCA onboarding cannot post anything:
            # count their invoices for the report and keep them out of the batch
            Journal = self.env['account.journal']
            blocked = Journal.browse()
            if 'l10n_sa_compliance_checks_passed' in Journal._fields:
                blocked = Journal.search([('edi_format_ids', '!=', False), ('l10n_sa_compliance_checks_passed', '=', False),
                                          ('company_id', '=', channel.company_id.id)])
            for group in self.env['account.move'].read_group(base_domain + [('journal_id', 'in', blocked.ids)], ['id:count'], ['journal_id']):
                not_ready[group['journal_id'][1]] = not_ready.get(group['journal_id'][1], 0) + group['journal_id_count']
            moves = self.env['account.move'].search(base_domain + [('journal_id', 'not in', blocked.ids)], limit=limit)
            for move in moves:
                orders = move.invoice_line_ids.sale_line_ids.order_id
                try:
                    with self.env.cr.savepoint():
                        orders.order_line.filtered(
                            lambda l: not l.display_type and not l[tax_field]
                        ).with_context(skip_tax_fix=True).write({tax_field: [(6, 0, zero.ids)]})
                        if self._salla_move_can_reset(move):
                            move.button_draft()
                            move.invoice_line_ids.filtered(
                                lambda l: l.display_type == 'product' and not l.tax_ids
                            ).write({'tax_ids': [(6, 0, zero.ids)]})
                            move.action_post()
                            fixed.append(move.name)
                        else:
                            new_move = self._salla_replace_locked_invoice(move, orders, zero)
                            fixed.append('%s -> %s' % (move.name, new_move.name))
                        paid.extend(self._salla_pay_repaired_orders(channel, orders))
                except Exception as e:  # keep going, report at the end
                    failed.append('%s: %s' % (move.name, str(e)[:150]))
                self._salla_repair_commit()
            # replacement invoices left unpaid by an earlier or interrupted run
            unpaid = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'), ('state', '=', 'posted'),
                ('payment_state', '=', 'not_paid'), ('company_id', '=', channel.company_id.id),
                ('invoice_line_ids', 'any', [('display_type', '=', 'product'), ('tax_ids', 'in', zero.ids)]),
                ('invoice_line_ids.sale_line_ids.order_id.channel_mapping_ids.channel_id', '=', channel.id),
            ], limit=limit)
            for move in unpaid:
                try:
                    with self.env.cr.savepoint():
                        paid.extend(self._salla_pay_repaired_orders(channel, move.invoice_line_ids.sale_line_ids.order_id))
                except Exception as e:
                    failed.append('%s: %s' % (move.name, str(e)[:150]))
                self._salla_repair_commit()
        lines = ['Fixed: %d invoice(s).' % len(fixed),
                 'Payments registered: %d.' % len(paid)]
        lines.extend(fixed[:10])
        for journal_name, count in not_ready.items():
            lines.append('Skipped %d invoice(s) of journal "%s": complete its ZATCA onboarding (CSID) first.' % (count, journal_name))
        if failed:
            lines.append('Failed: %d' % len(failed))
            lines.extend(failed[:20])
        return self._salla_repair_notify('Salla: invoices without tax', lines)

    def _salla_pay_repaired_orders(self, channel, orders):
        """Register the payment of the orders' open invoice the way the connector does
        (journal of the Salla payment method, payment on the invoice date), when the Salla
        status of the order is mapped to a paid invoice."""
        paid = []
        Skeleton = self.env['multi.channel.skeleton']
        for order in orders:
            feed = self.env['order.feed'].search([
                ('channel_id', '=', channel.id), ('name', '=', order.client_order_ref)], limit=1)
            state_map = feed and channel.order_state_ids.filtered(lambda st: st.channel_state == feed.order_state)
            if not feed or not state_map or state_map[0].odoo_set_invoice_state != 'paid'                     or not feed.payment_method:
                continue
            mapping = self.env['channel.account.journal.mappings'].search([
                ('channel_id', '=', channel.id), ('store_journal_name', '=', feed.payment_method)], limit=1)
            if not mapping:
                continue
            res = Skeleton.SetOrderPaid({
                'order_id': order.id, 'journal_id': mapping.odoo_journal_id,
                'channel_id': channel, 'date_invoice': order.date_order,
            })
            if not res.get('status'):
                raise ValueError(res.get('status_message') or 'payment failed')
            paid.append(order.name)
        return paid

    def _salla_move_can_reset(self, move):
        for field in ('inalterable_hash', 'secured'):
            if field in move._fields and move[field]:
                return False
        return True

    def _salla_replace_locked_invoice(self, move, orders, zero):
        reversal = move._reverse_moves(default_values_list=[{
            'invoice_date': move.invoice_date,
            'date': move.date,
            'ref': 'Reversal of %s: 0%% tax missing on export lines' % move.name,
        }], cancel=False)
        reversal.invoice_line_ids.filtered(
            lambda l: l.display_type == 'product' and not l.tax_ids
        ).write({'tax_ids': [(6, 0, zero.ids)]})
        reversal.action_post()
        receivable = (move.line_ids + reversal.line_ids).filtered(
            lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled)
        receivable.reconcile()
        orders.invalidate_recordset()
        new_move = orders.with_context(raise_if_nothing_to_invoice=False)._create_invoices()
        if not new_move:
            raise ValueError('nothing left to invoice on %s' % orders.mapped('name'))
        new_move.invoice_line_ids.filtered(
            lambda l: l.display_type == 'product' and not l.tax_ids
        ).write({'tax_ids': [(6, 0, zero.ids)]})
        new_move.write({'invoice_date': move.invoice_date, 'ref': move.ref or move.name})
        new_move.action_post()
        return new_move

    @api.model
    def salla_cancel_unlinked_payments(self, limit=3000):
        """Payments of the connector journals that are linked to no invoice.

        A bulk run on 2026-09-20 registered payments twice and left thousands of them
        unmatched (their memo is the invoice name). When that invoice is already paid by
        another payment, the unlinked payment is a duplicate and is cancelled; when the
        invoice is still open, the payment is matched with it instead; anything else is
        only reported.
        """
        cancelled, matched, kept, failed = [], [], [], []
        Move = self.env['account.move']
        for channel in self.search([('channel', '=', 'salla')]):
            mappings = self.env['channel.account.journal.mappings'].search([('channel_id', '=', channel.id)])
            journal_ids = set(mappings.mapped('odoo_journal_id'))
            # older journals of the same payment method (e.g. "tamara_installment0")
            prefixes = [name for name in mappings.mapped('store_journal_name') if name]
            for journal in self.env['account.journal'].search([
                    ('company_id', '=', channel.company_id.id), ('type', 'in', ('bank', 'cash'))]):
                if any(journal.name.startswith(prefix) for prefix in prefixes):
                    journal_ids.add(journal.id)
            payments = self.env['account.payment'].search([
                ('journal_id', 'in', list(journal_ids)), ('state', 'in', ('paid', 'in_process', 'posted')),
                ('company_id', '=', channel.company_id.id)], limit=limit * 3)
            count = 0
            for payment in payments:
                if payment.reconciled_invoice_ids or payment.reconciled_bill_ids:
                    continue
                if count >= limit:
                    break
                count += 1
                invoice = Move.search([('name', '=', payment.memo or ''), ('move_type', '=', 'out_invoice')], limit=1) if payment.memo else Move
                try:
                    with self.env.cr.savepoint():
                        if invoice and invoice.state == 'posted' and invoice.payment_state in ('paid', 'in_payment', 'reversed'):
                            payment.action_draft()
                            payment.action_cancel()
                            cancelled.append(payment.name)
                        elif invoice and invoice.state == 'posted' and invoice.payment_state in ('not_paid', 'partial')                                 and invoice.currency_id == payment.currency_id                                 and abs(invoice.amount_residual - payment.amount) < 0.01:
                            lines = (payment.move_id.line_ids + invoice.line_ids).filtered(
                                lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled)
                            lines.reconcile()
                            matched.append('%s -> %s' % (payment.name, invoice.name))
                        else:
                            kept.append('%s (%s: %s)' % (payment.name, payment.memo or 'no memo',
                                                         invoice.payment_state if invoice else 'invoice not found'))
                except Exception as e:
                    failed.append('%s: %s' % (payment.name, str(e)[:120]))
                if count % 200 == 0:
                    self._salla_repair_commit()
            self._salla_repair_commit()
        lines = ['Cancelled duplicates: %d.' % len(cancelled),
                 'Matched with their open invoice: %d.' % len(matched),
                 'Left untouched (invoice not found or not paid by another payment): %d.' % len(kept)]
        lines.extend(kept[:10])
        if failed:
            lines.append('Failed: %d' % len(failed))
            lines.extend(failed[:10])
        return self._salla_repair_notify('Salla: unlinked payments', lines)

    @api.model
    def salla_fix_dates(self, limit=50000):
        zone = pytz.timezone(SALLA_TZ)
        n_orders = n_payments = 0
        failed = []
        for channel in self.search([('channel', '=', 'salla')]):
            if channel.wk_time_zone != SALLA_TZ:
                channel.wk_time_zone = SALLA_TZ
                self._salla_repair_commit()
            # 1) order dates: Salla sends local (Riyadh) time; recompute the UTC value
            feeds = self.env['order.feed'].search([
                ('channel_id', '=', channel.id), ('date_order', '!=', False)], limit=limit)
            mappings = self.env['channel.order.mappings'].search([
                ('channel_id', '=', channel.id), ('store_order_id', 'in', feeds.mapped('store_id'))])
            order_by_store = {m.store_order_id: m.order_name for m in mappings if m.order_name}
            count = 0
            for feed in feeds:
                order = order_by_store.get(feed.store_id)
                if not order or not order.date_order:
                    continue
                try:
                    local = parser.parse(feed.date_order, ignoretz=True)
                except (ValueError, TypeError, OverflowError):
                    continue
                expected = zone.localize(local).astimezone(pytz.utc).replace(tzinfo=None)
                if abs((order.date_order - expected).total_seconds()) > 60:
                    try:
                        with self.env.cr.savepoint():
                            order.write({'date_order': expected})
                        n_orders += 1
                    except Exception as e:
                        failed.append('%s: %s' % (order.name, str(e)[:120]))
                count += 1
                if count % 500 == 0:
                    self._salla_repair_commit()
            self._salla_repair_commit()
            # 2) payments registered by the connector: move them to the invoice date
            journal_ids = self.env['channel.account.journal.mappings'].search(
                [('channel_id', '=', channel.id)]).mapped('odoo_journal_id')
            payments = self.env['account.payment'].search([
                ('journal_id', 'in', list(journal_ids)), ('state', 'in', ('paid', 'in_process', 'posted')),
            ], limit=limit)
            count = 0
            for payment in payments:
                if not payment.reconciled_invoice_ids:
                    continue
                dates = payment.reconciled_invoice_ids.mapped('invoice_date')
                inv_date = min(d for d in dates if d) if any(dates) else False
                if not inv_date or payment.date == inv_date:
                    continue
                try:
                    with self.env.cr.savepoint():
                        # the date of a posted entry is read-only: reset, re-date, post and
                        # reconcile the payment with its invoices again
                        invoices = payment.reconciled_invoice_ids
                        payment.action_draft()
                        payment.write({'date': inv_date})
                        payment.action_post()
                        lines = (payment.move_id.line_ids + invoices.line_ids).filtered(
                            lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled)
                        lines.reconcile()
                        if any(inv.payment_state not in ('paid', 'in_payment') for inv in invoices):
                            raise ValueError('invoice not paid after re-reconciliation')
                    n_payments += 1
                except Exception as e:
                    failed.append('%s: %s' % (payment.name, str(e)[:120]))
                count += 1
                if count % 500 == 0:
                    self._salla_repair_commit()
            self._salla_repair_commit()
        lines = ['Channel time zone: %s.' % SALLA_TZ,
                 'Order dates corrected: %d.' % n_orders,
                 'Payments moved to their invoice date: %d.' % n_payments]
        if failed:
            lines.append('Failed: %d' % len(failed))
            lines.extend(failed[:20])
        return self._salla_repair_notify('Salla: dates', lines)
