# -*- coding: utf-8 -*-
"""Refunds of restored/canceled Salla orders and cleanup of duplicate orders.

- _salla_refund_order: every standing customer invoice of the order gets a credit note; an
  unpaid invoice is closed by it, a paid one has its money refunded from the journal that
  received the payment. Runs from the feed evaluation (Salla status restored / refunded /
  canceled) and from the server action "Salla: Refund restored orders" for the orders that were
  already in that state.
  A live copy of such an order left by an older import, while the mapped copy is cancelled (or
  there is none), is settled the same way and cancelled like the Salla order.
- salla_cancel_duplicate_orders: two sale orders for one Salla order (same client_order_ref).
  The one without channel mapping loses its payments (cancelled) and invoices (credit notes)
  and is cancelled; the mapped one is kept.
- An invoice that groups several orders (older bulk invoicing) is credited for the lines of the
  returned or duplicate order only: the other orders keep their sale and their payment.
"""
import logging

from odoo import Command, api, fields, models

_logger = logging.getLogger(__name__)
SALLA_REFUND_STATES = ('restored', 'refunded', 'canceled', 'cancelled')
SALLA_POST_LOCK_CLASS = 714002


class MultiChannelSale(models.Model):
    _inherit = 'multi.channel.sale'

    def _salla_lock_journal_posting(self, journals):
        """The Salla jobs post in a hash-locked journal one at a time; the lock is held until the
        transaction ends. Two jobs posting side by side (an import and "Invoice and Pay") took
        numbers whose predecessor was not committed yet, and Odoo refused the second posting with
        "a gap has been detected in the sequence"."""
        for journal in journals.filtered(lambda j: j.restrict_mode_hash_table).sorted('id'):
            self.env.cr.execute('SELECT pg_advisory_xact_lock(%s, %s)', (SALLA_POST_LOCK_CLASS, journal.id))

    def _salla_blocked_journals(self, company):
        """Journals with the e-invoicing format but no ZATCA onboarding: nothing can be posted there."""
        Journal = self.env['account.journal']
        if 'l10n_sa_compliance_checks_passed' not in Journal._fields:
            return Journal.browse()
        return Journal.search([('edi_format_ids', '!=', False), ('l10n_sa_compliance_checks_passed', '=', False),
                               ('company_id', '=', company.id)])

    def _salla_post_credit_note(self, note):
        """Post a credit note; product lines without tax get the channel's 0% tax first, because
        the Saudi e-invoicing refuses to post a move without tax (old export invoices had none)."""
        untaxed = note.invoice_line_ids.filtered(lambda l: l.display_type == 'product' and not l.tax_ids)
        if untaxed:
            zero = self.search([('channel', '=', 'salla'), ('company_id', '=', note.company_id.id),
                                ('salla_zero_tax_id', '!=', False)], limit=1).salla_zero_tax_id
            if zero:
                untaxed.write({'tax_ids': [(6, 0, zero.ids)]})
        return self._salla_post_like_origin(note, note.reversed_entry_id)

    @api.model
    def _salla_invoice_settled(self, move):
        """Paid, or posted with nothing left to pay: invoices in a three-decimal currency (KWD,
        OMR) can stay "partially paid" with a zero residual on both sides of the reconciliation."""
        return move.payment_state in ('paid', 'in_payment') or (
            move.state == 'posted' and move.currency_id.is_zero(move.amount_residual))

    def _salla_standing_invoices(self, order):
        """Posted customer invoices of the order whose part for the order is not credited in full:
        a credit note of part of it (total adjustment) leaves it standing, the credit note of
        another order of a grouped invoice does not touch the part of this one. An invoice that no
        credit note of the order reverses stands whatever its total (free orders invoice 0)."""
        invoices = order.invoice_ids.filtered(
            lambda m: m.move_type == 'out_invoice' and m.state == 'posted' and m.payment_state != 'reversed')
        notes = order.invoice_ids.filtered(lambda m: m.move_type == 'out_refund' and m.state == 'posted')
        standing = self.env['account.move']
        for invoice in invoices:
            own_notes = notes.filtered(lambda n: n.reversed_entry_id == invoice)
            if not own_notes:
                standing |= invoice
                continue
            credited = sum(self._salla_move_order_amount(note, order) for note in own_notes)
            if invoice.currency_id.compare_amounts(self._salla_move_order_amount(invoice, order), credited) > 0:
                standing |= invoice
        return standing

    def _salla_refund_order(self, order, refund_date=None, reason=None, include_blocked=False):
        """Credit note for every standing invoice of the order; the money of a paid invoice is
        refunded from the journal that received it. Returns the credit notes (empty when there
        was nothing to do, so the call is safe to repeat).

        An order whose total was brought to Salla's by an adjustment gets one credit note of what
        the books hold for it, so that it nets to zero."""
        refund_date = refund_date or fields.Date.context_today(self)
        blocked = self._salla_blocked_journals(order.company_id)
        notes = self.env['account.move']
        standing = self._salla_standing_invoices(order)
        skipped = standing.filtered(lambda m: m.journal_id in blocked) if not include_blocked else notes
        for invoice in skipped:
            _logger.info('Salla refund: %s skipped, journal %s is not onboarded', invoice.name, invoice.journal_id.name)
        if standing and self._salla_order_adjusted(order):
            if skipped:
                return notes
            return self._salla_adjust_order_total(
                order, 0.0, date=refund_date,
                reason=reason or 'Salla order %s returned' % (order.client_order_ref or order.name))
        for invoice in standing - skipped:
            notes |= self._salla_refund_invoice_part(
                invoice, order, refund_date,
                reason or 'Salla order %s returned: %s' % (order.client_order_ref or order.name, invoice.name))
        return notes

    def _salla_refund_invoice_part(self, invoice, order, date, ref):
        """Credit note of what `invoice` bills for `order` (all of it, unless the invoice groups
        several orders: then only the lines of `order`), matched with the invoice while it is open;
        the money of a paid invoice is refunded from the journal that received it."""
        payments = invoice._get_reconciled_payments().filtered(lambda p: p.state not in ('cancel', 'canceled', 'rejected'))
        note = invoice._reverse_moves(default_values_list=[{
            'invoice_date': date,
            'date': date,
            'ref': ref,
        }], cancel=False)
        if self._salla_move_other_orders(invoice, order):
            others = note.invoice_line_ids.filtered(
                lambda l: l.display_type == 'product' and not (l.sale_line_ids.order_id & order))
            note.write({'invoice_line_ids': [Command.delete(line.id) for line in others]})
        self._salla_post_credit_note(note)
        if invoice.amount_residual:
            receivable = (invoice.line_ids + note.line_ids).filtered(
                lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled)
            if len(receivable) > 1:
                receivable.reconcile()
        if note.amount_residual and payments:
            self._salla_lock_journal_posting(payments[0].journal_id)
            wizard = self.env['account.payment.register'].with_context(
                active_model='account.move', active_ids=note.ids,
            ).create({'journal_id': payments[0].journal_id.id, 'payment_date': date})
            wizard.action_create_payments()
        return note

    def _salla_settle_returned_twin(self, twin, refund_date, cancel, include_blocked=False):
        """A live copy of a returned/cancelled Salla order whose mapped copy is cancelled (or
        missing): credit notes (and refunds) for its invoices, then cancelled like the Salla order."""
        notes = self._salla_refund_order(twin, refund_date=refund_date, include_blocked=include_blocked)
        if cancel:
            if self._salla_standing_invoices(twin):
                raise ValueError('%s still has a standing invoice' % twin.name)
            twin.invoice_ids.filtered(lambda m: m.state == 'draft').button_cancel()
            twin.message_post(body='Cancelled: Salla order %s is cancelled (older copy of a cancelled order).'
                              % twin.client_order_ref)
            # from_webhook: the connector must not push this cancellation to the Salla store
            twin.with_context(disable_cancel_warning=True, from_webhook=True).action_cancel()
            if twin.state != 'cancel':
                twin.write({'state': 'cancel'})
        return notes

    @api.model
    def salla_refund_restored_orders(self, limit=300, store_ids=None, include_blocked=False):
        """Orders whose Salla status is restored/refunded/canceled and that still carry a standing
        invoice: credit note (+ refund payment when the invoice was paid), dated on the day the
        status was received.

        An older import can have left a live copy of the order (same client_order_ref) while the
        copy mapped to the channel is cancelled, or not mapped at all: that copy is settled the
        same way, then cancelled when the Salla status maps to a cancelled order, otherwise it
        takes the channel mapping."""
        done, failed, skipped, blocked_refs = [], [], 0, []
        Order = self.env['sale.order']
        for channel in self.search([('channel', '=', 'salla')]):
            feed_domain = [('channel_id', '=', channel.id), ('order_state', 'in', SALLA_REFUND_STATES)]
            if store_ids is not None:
                feed_domain.append(('store_id', 'in', list(store_ids)))
            feeds = self.env['order.feed'].search(feed_domain)
            mappings = self.env['channel.order.mappings'].search([
                ('channel_id', '=', channel.id), ('store_order_id', 'in', feeds.mapped('store_id'))])
            order_by_store = {m.store_order_id: m.order_name for m in mappings if m.order_name}
            live_by_ref = {}
            for live in Order.search([('client_order_ref', 'in', [f.name for f in feeds if f.name]),
                                      ('company_id', '=', channel.company_id.id), ('state', '!=', 'cancel')]):
                live_by_ref[live.client_order_ref] = live_by_ref.get(live.client_order_ref, Order) | live
            cancel_states = set(channel.order_state_ids.filtered(
                lambda s: s.odoo_order_state == 'cancelled').mapped('channel_state'))
            blocked = self._salla_blocked_journals(channel.company_id)
            count = 0
            for feed in feeds:
                order = order_by_store.get(feed.store_id) or Order
                twins = Order
                if not order or order.state == 'cancel':
                    twins = live_by_ref.get(feed.name, Order) - order
                if not twins and (not order or not self._salla_standing_invoices(order)):
                    continue
                if not include_blocked and any(
                        move.journal_id in blocked for twin in twins for move in self._salla_standing_invoices(twin)):
                    blocked_refs.append(feed.name)
                    continue
                if count >= limit:
                    skipped += 1
                    continue
                count += 1
                refund_date = fields.Date.to_date(feed.write_date) if feed.write_date else None
                try:
                    with self.env.cr.savepoint():
                        notes = self.env['account.move']
                        if order and self._salla_standing_invoices(order):
                            notes |= self._salla_refund_order(order, refund_date=refund_date, include_blocked=include_blocked)
                        cancel = feed.order_state in cancel_states
                        for twin in twins:
                            notes |= self._salla_settle_returned_twin(twin, refund_date, cancel, include_blocked)
                        if twins and not cancel:
                            keep = self._salla_pick_order_to_keep(twins)
                            if order:
                                self._salla_move_mapping(keep, order)
                            else:
                                channel.create_order_mapping(keep, feed.store_id, None, feed.order_state)
                    if notes or twins:
                        done.append('%s -> %s' % (', '.join((order | twins).mapped('name')),
                                                  ', '.join(notes.mapped('name')) or 'cancelled'))
                except Exception as e:  # keep going, report at the end
                    failed.append('%s: %s' % (', '.join((order | twins).mapped('name')), str(e)[:150]))
                if count % 20 == 0:
                    self._salla_repair_commit()
            self._salla_repair_commit()
        lines = ['Credit notes created for %d order(s).' % len(done)]
        if skipped:
            lines.append('%d more order(s) left for the next run.' % skipped)
        if blocked_refs:
            lines.append('Skipped, invoice in a journal without ZATCA onboarding: %d (%s)' % (
                len(blocked_refs), ', '.join(blocked_refs[:10])))
        lines.extend(done[:10])
        if failed:
            lines.append('Failed: %d' % len(failed))
            lines.extend(failed[:20])
        return self._salla_repair_notify('Salla: restored orders', lines)

    @api.model
    def salla_cancel_duplicate_orders(self, limit=400, refs=None, include_blocked=False):
        """Sale orders that share a client_order_ref (one Salla order imported twice).

        The order that carries the accounting is kept: a paid invoice first, then a posted
        invoice, then the one mapped to the channel, then the oldest. The channel mapping is moved
        to the kept order. The other orders are cancelled; only an invoice that duplicates one of
        the kept order is reversed (credit note) and its payment cancelled. When the kept order has
        no invoice at all, the twin's invoice is never reversed: that twin is kept instead.
        Groups touching a journal that cannot post (no ZATCA onboarding) are skipped and counted.
        """
        cancelled, failed, skipped_blocked, moved, left = [], [], [], 0, 0
        Order = self.env['sale.order']
        # duplicates are per company: several Salla channels of one company share the orders
        for company in self.search([('channel', '=', 'salla')]).mapped('company_id'):
            blocked = self._salla_blocked_journals(company)
            query = """
                SELECT client_order_ref FROM sale_order
                 WHERE company_id = %s AND state != 'cancel'
                   AND client_order_ref IS NOT NULL AND client_order_ref != ''"""
            params = [company.id]
            if refs is not None:
                query += " AND client_order_ref = ANY(%s)"
                params.append(list(refs))
            query += " GROUP BY client_order_ref HAVING count(*) > 1 ORDER BY client_order_ref"
            self.env.cr.execute(query, params)
            dup_refs = [row[0] for row in self.env.cr.fetchall()]
            count = 0
            for ref in dup_refs:
                if count >= limit:
                    break
                orders = Order.search([('client_order_ref', '=', ref), ('company_id', '=', company.id),
                                       ('state', '!=', 'cancel')], order='id')
                keep = self._salla_pick_order_to_keep(orders)
                twins = orders - keep
                to_reverse = self._salla_twin_invoices_to_reverse(keep, twins)
                if not include_blocked and to_reverse.filtered(lambda m: m.journal_id in blocked):
                    skipped_blocked.append(ref)
                    continue
                count += 1
                try:
                    with self.env.cr.savepoint():
                        if self._salla_move_mapping(keep, twins):
                            moved += 1
                        for dup in twins:
                            self._salla_cancel_duplicate(dup, keep, to_reverse)
                    cancelled.append('%s (kept %s)' % (', '.join(twins.mapped('name')), keep.name))
                except Exception as e:
                    failed.append('%s: %s' % (ref, str(e)[:150]))
                if count % 25 == 0:
                    self._salla_repair_commit()
            self._salla_repair_commit()
            left += len(dup_refs) - count - len(skipped_blocked) - len(failed)
        lines = ['Duplicate groups cleaned: %d (mapping moved to the invoiced order in %d).' % (len(cancelled), moved)]
        if left > 0:
            lines.append('%d group(s) left for the next run.' % left)
        if skipped_blocked:
            lines.append('Skipped, invoice in a journal without ZATCA onboarding: %d (%s)' % (
                len(skipped_blocked), ', '.join(skipped_blocked[:10])))
        lines.extend(cancelled[:10])
        if failed:
            lines.append('Failed: %d' % len(failed))
            lines.extend(failed[:20])
        return self._salla_repair_notify('Salla: duplicate orders', lines)

    def _salla_order_rank(self, order):
        standing = self._salla_standing_invoices(order)
        paid = standing.filtered(lambda m: m.payment_state in ('paid', 'in_payment', 'partial'))
        return (bool(paid), bool(standing), bool(order.channel_mapping_ids), -order.id)

    def _salla_pick_order_to_keep(self, orders):
        return max(orders, key=self._salla_order_rank)

    def _salla_twin_invoices_to_reverse(self, keep, twins):
        """Standing invoices of the twins. They only duplicate something when the kept order has
        an invoice itself (the kept order is chosen so that this is always the case when any twin
        has one)."""
        if not self._salla_standing_invoices(keep):
            return self.env['account.move']
        invoices = self.env['account.move']
        for twin in twins:
            invoices |= self._salla_standing_invoices(twin)
        return invoices

    def _salla_move_mapping(self, keep, twins):
        """The channel mappings of the cancelled twins point to the kept order (one per channel)."""
        moved = False
        for mapping in twins.mapped('channel_mapping_ids'):
            if keep.channel_mapping_ids.filtered(lambda m: m.channel_id == mapping.channel_id):
                continue  # never unlink a mapping: the connector deletes the order feed with it
            mapping.write({'order_name': keep.id, 'odoo_order_id': keep.id})
            keep.invalidate_recordset(['channel_mapping_ids'])
            moved = True
        return moved

    def _salla_cancel_duplicate(self, dup, keep, to_reverse):
        for invoice in self._salla_standing_invoices(dup):
            if invoice not in to_reverse:
                raise ValueError('invoice %s of %s would be left alone on a cancelled order' % (invoice.name, dup.name))
            if self._salla_move_other_orders(invoice, dup):
                # a grouped invoice also bills other orders: only the duplicate's lines are credited
                # and their money refunded, the payment stays with the other orders
                self._salla_refund_invoice_part(
                    invoice, dup, invoice.invoice_date,
                    'Duplicate of %s (Salla order %s): %s' % (keep.name, dup.client_order_ref, invoice.name))
                continue
            for payment in invoice._get_reconciled_payments().filtered(lambda p: p.state not in ('cancel', 'canceled', 'rejected')):
                if payment.reconciled_invoice_ids - invoice:
                    raise ValueError('payment %s also pays another invoice' % payment.name)
                payment.action_draft()
                payment.action_cancel()
            note = invoice._reverse_moves(default_values_list=[{
                'invoice_date': invoice.invoice_date,
                'date': invoice.date,
                'ref': 'Duplicate of %s (Salla order %s): %s' % (keep.name, dup.client_order_ref, invoice.name),
            }], cancel=False)
            self._salla_post_credit_note(note)
            receivable = (invoice.line_ids + note.line_ids).filtered(
                lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled)
            if len(receivable) > 1:
                receivable.reconcile()
        dup.invoice_ids.filtered(lambda m: m.state == 'draft').button_cancel()
        dup.message_post(body='Cancelled: duplicate of %s for Salla order %s.' % (keep.name, dup.client_order_ref))
        # from_webhook: the connector must not push this cancellation to the Salla store
        dup.with_context(disable_cancel_warning=True, from_webhook=True).action_cancel()
        if dup.state != 'cancel':
            dup.write({'state': 'cancel'})
