# -*- coding: utf-8 -*-
"""Salla totals brought into Odoo, and the e-invoicing rule of the corrections.

- _salla_adjust_order_total: an order edited in Salla after the import (shipping recalculated,
  coupon changed, items removed) keeps the lines of the import in Odoo, because the connector only
  updates draft orders. One adjustment line on the sale order, invoiced on its own, brings the
  invoiced total to Salla's total: a debit note when Salla is higher, a credit note when it is
  lower, paid or refunded through the journal that received the order's payment, dated like the
  order's invoice.
- _salla_rebuild_order_invoice: the invoice mixes a product line without VAT with lines under VAT
  (old imports): an adjustment cannot express that (ZATCA refuses a negative VAT base), so the
  invoice is credited, the untaxed lines take the VAT of the other lines, as in Salla, and the order
  is invoiced again; the payment moves to the new invoice.
- _salla_post_like_origin: a correction follows the e-invoicing of the invoice it corrects. It is
  sent to ZATCA when that invoice was sent, kept out of ZATCA when that invoice never was, and it is
  posted without e-invoicing document in a journal whose ZATCA onboarding is not done yet, like the
  rest of that journal.
- salla_report_missing_einvoices: invoices posted in an onboarded journal that never got their
  e-invoicing document (the base connector swallowed the ZATCA errors raised after posting) get
  one, so the ZATCA cron sends them, when ZATCA can accept them.
- Hold: while the system parameter odoo_salla_integration.hold_zatca is set, what the Salla
  repair tools post (credit notes, adjustments, invoices made again, invoices of the audit and
  backfill runs) stays out of ZATCA: no e-invoicing document, the ZATCA cron is not woken. The
  invoices of the orders the store sends every day go to ZATCA as usual. Once the parameter is
  removed, salla_report_missing_einvoices creates the documents of what was held.
- Grouped invoices: an older bulk invoicing put several orders of one customer on one invoice.
  What such an invoice, or its credit note, holds for one order is the total of that order's
  lines (_salla_move_order_amount).
- _salla_bring_order_to_total: an order changed in Salla after the import (coupon added or
  removed) keeps its imported lines once it is confirmed. Before its first invoice it gets one
  adjustment line on the sale order, so the invoice that goes to ZATCA already has Salla's total.
"""
import ast
import collections
import logging
import math
from contextlib import contextmanager

from odoo import api, fields, models

from .salla_audit import AMOUNT_TOLERANCE, AMOUNT_TOLERANCE_FOREIGN

_logger = logging.getLogger(__name__)

SALLA_ADJUST_CODE = 'SALLA-ADJUST'
ZATCA_CODE = 'sa_zatca'
HOLD_PARAM = 'odoo_salla_integration.hold_zatca'


class MultiChannelSale(models.Model):
    _inherit = 'multi.channel.sale'

    # ------------------------------------------------------------------ e-invoicing
    def _salla_has_einvoicing(self):
        return 'edi_document_ids' in self.env['account.move']._fields

    def _salla_zatca_docs(self, moves):
        if not self._salla_has_einvoicing():
            return self.env['account.move'].browse()
        return moves.edi_document_ids.filtered(lambda d: d.edi_format_id.code == ZATCA_CODE)

    def _salla_zatca_on_hold(self):
        value = self.env['ir.config_parameter'].sudo().get_param(HOLD_PARAM) or ''
        return value.strip().lower() in ('1', 'true', 'yes')

    def _salla_post_held(self, move):
        """Post a correction while they are on hold: its e-invoicing document is dropped in the
        same transaction and the ZATCA cron is not woken, so nothing reaches ZATCA."""
        move.with_context(skip_account_edi_cron_trigger=True).action_post()
        docs = self._salla_zatca_docs(move).filtered(lambda d: d.state == 'to_send')
        if docs:
            docs.unlink()
            move.message_post(body='Not sent to ZATCA: Salla corrections are on hold (system parameter %s).' % HOLD_PARAM)
        return move

    @contextmanager
    def _salla_post_without_einvoice(self, journals):
        """Post in journals that carry the ZATCA format but are not onboarded: the format is taken off
        for the current transaction only and put back before the block ends, so the documents posted
        meanwhile get no e-invoicing document, like the rest of those journals. Use it inside a
        savepoint: when the block fails, the rollback restores the format."""
        journals = journals.filtered(lambda j: 'edi_format_ids' in j._fields and j.edi_format_ids)
        saved = [(journal, journal.edi_format_ids) for journal in journals]
        for journal, _formats in saved:
            journal.write({'edi_format_ids': [(5, 0, 0)]})
        yield
        for journal, formats in saved:
            journal.write({'edi_format_ids': [(6, 0, formats.ids)]})

    def _salla_post_new(self, move):
        """Post a new invoice of a Salla order: sent to ZATCA as usual, kept like the rest of its
        journal when that journal is not onboarded, kept out of ZATCA while corrections are on hold."""
        self._salla_lock_journal_posting(move.journal_id)
        if move.journal_id in self._salla_blocked_journals(move.company_id):
            with self._salla_post_without_einvoice(move.journal_id):
                move.action_post()
        elif self._salla_zatca_on_hold():
            self._salla_post_held(move)
        else:
            move.action_post()
        return move

    def _salla_post_like_origin(self, move, origin):
        """Post a correction of `origin` (credit note, debit note, adjustment): ZATCA sees it only
        when it saw `origin`."""
        self._salla_post_new(move)
        docs = self._salla_zatca_docs(move)
        if docs and origin and not self._salla_zatca_docs(origin):
            docs.filtered(lambda d: d.state == 'to_send').unlink()
            move.message_post(body='Not sent to ZATCA: the invoice it corrects (%s) was never sent either.' % origin.name)
        return move

    @api.model
    def salla_report_missing_einvoices(self, limit=2000, dry_run=True):
        """Posted invoices and credit notes of onboarded ZATCA journals without e-invoicing document:
        create the document (the ZATCA cron sends it) when ZATCA can accept the move. A reversed
        invoice goes too when its credit note already went, so that ZATCA sees both; a credit note
        whose invoice never went stays out."""
        title = 'Salla: missing ZATCA documents'
        if not self._salla_has_einvoicing():
            return self._salla_repair_notify(title, ['Electronic invoicing is not installed.'])
        held = not dry_run and self._salla_zatca_on_hold()
        if held:
            dry_run = True
        zatca = self.env['account.edi.format'].search([('code', '=', ZATCA_CODE)], limit=1)
        journals = self.env['account.journal'].search([('edi_format_ids', 'in', zatca.ids)]).filtered(
            lambda j: j._l10n_sa_ready_to_submit_einvoices())
        moves = self.env['account.move'].search([
            ('journal_id', 'in', journals.ids), ('state', '=', 'posted'),
            ('move_type', 'in', ('out_invoice', 'out_refund')), ('edi_document_ids', '=', False),
        ], order='invoice_date, id')
        ready, skipped = self.env['account.move'], collections.Counter()
        for move in moves:
            if len(ready) >= limit:
                skipped['left for the next run'] += 1
                continue
            product_lines = move.invoice_line_ids.filtered(lambda l: l.display_type == 'product')
            if any(not line.tax_ids for line in product_lines):
                skipped['line without tax'] += 1
                continue
            if move.currency_id.decimal_places > 2:
                skipped['three-decimal currency (ZATCA BR-DEC)'] += 1
                continue
            if 'l10n_sa_confirmation_datetime' in move._fields and not move.l10n_sa_confirmation_datetime:
                # ZATCA cannot build the document of a move posted before e-invoicing was installed
                skipped['posted before e-invoicing (no confirmation date)'] += 1
                continue
            if move.move_type == 'out_invoice':
                notes = move.reversal_move_ids.filtered(lambda m: m.state == 'posted')
                if notes and not self._salla_zatca_docs(notes):
                    skipped['reversed, its credit note was not sent either'] += 1
                    continue
            elif not move.reversed_entry_id or not self._salla_zatca_docs(move.reversed_entry_id):
                skipped['credit note of an invoice never sent'] += 1
                continue
            errors = zatca._check_move_configuration(move)
            if errors:
                skipped['configuration: %s' % errors[0][:60]] += 1
                continue
            ready |= move
        if not dry_run and ready:
            self.env['account.edi.document'].create([
                {'move_id': move.id, 'edi_format_id': zatca.id, 'state': 'to_send'} for move in ready])
        lines = ['%s %d document(s) for ZATCA (%.2f SAR).' % (
            'Would create' if dry_run else 'Created', len(ready), sum(ready.mapped('amount_total_signed')))]
        if held:
            lines.insert(0, 'Corrections are on hold (system parameter %s): nothing created.' % HOLD_PARAM)
        lines += ['Skipped, %s: %d' % (reason, count) for reason, count in skipped.most_common()]
        lines += ready[:10].mapped('name')
        return self._salla_repair_notify(title, lines)

    # ------------------------------------------------------------------ taxes
    def _salla_complete_taxes(self, taxes):
        """A tax the connector creates for a new Salla rate ("Salla Tax 15.0%") has no tax account
        and no tax grids: its VAT would be booked as sales and miss the VAT return. It takes the
        account and grids of the company's sale tax of the same rate that has them."""
        def tax_lines(tax):
            return (tax.invoice_repartition_line_ids | tax.refund_repartition_line_ids).filtered(
                lambda l: l.repartition_type == 'tax')

        for tax in taxes.filtered(lambda t: t.amount_type == 'percent' and t.amount > 0):
            if all(line.account_id for line in tax_lines(tax)) and tax.invoice_repartition_line_ids.tag_ids:
                continue
            refs = self.env['account.tax'].search([
                ('id', '!=', tax.id), ('type_tax_use', '=', 'sale'), ('amount_type', '=', 'percent'),
                ('amount', '=', tax.amount), ('company_id', '=', tax.company_id.id)], order='sequence, id')
            ref = refs.filtered(lambda t: t.price_include == tax.price_include and all(
                line.account_id for line in tax_lines(t)) and t.invoice_repartition_line_ids.tag_ids)[:1]
            if not ref:
                _logger.warning('Salla tax %s has no tax account and no sale tax of %s%% to copy it from', tax.name, tax.amount)
                continue
            for field in ('invoice_repartition_line_ids', 'refund_repartition_line_ids'):
                for kind in ('base', 'tax'):
                    src = ref[field].filtered(lambda l: l.repartition_type == kind).sorted('sequence')[:1]
                    dst = tax[field].filtered(lambda l: l.repartition_type == kind).sorted('sequence')[:1]
                    if src and dst:
                        vals = {'tag_ids': [(6, 0, src.tag_ids.ids)]}
                        if kind == 'tax':
                            vals['account_id'] = src.account_id.id
                        dst.write(vals)
            _logger.info('Salla tax %s completed from %s (tax account and grids)', tax.name, ref.name)

    # ------------------------------------------------------------------ totals
    def _salla_move_other_orders(self, move, order):
        """Sale orders other than `order` that `move` bills too (older grouped invoices)."""
        return move.invoice_line_ids.sale_line_ids.order_id - order

    def _salla_move_order_amount(self, move, order):
        """What a customer invoice or credit note bills for `order`, in the move currency, tax
        included: all of it, unless it groups several orders; then the lines of `order`, the lines
        of no order shared in proportion, and the rounding of the move on the biggest part, so that
        the parts of its orders add up to its total."""
        lines = move.invoice_line_ids.filtered(lambda l: l.display_type == 'product')
        orders = lines.sale_line_ids.order_id
        if not (orders - order):
            return move.amount_total
        parts = dict.fromkeys(orders, 0.0)
        loose = 0.0
        for line in lines:
            if len(line.sale_line_ids.order_id) == 1:
                parts[line.sale_line_ids.order_id] += line.price_total
            else:
                loose += line.price_total
        linked = sum(parts.values())
        for key in parts:
            parts[key] += loose * parts[key] / linked if linked else loose / len(parts)
        biggest = max(parts, key=lambda o: (parts[o], -o.id))
        parts[biggest] += move.amount_total - sum(parts.values())
        return move.currency_id.round(parts.get(order, 0.0))

    def _salla_order_net(self, order):
        """Invoiced total of the order in its currency: posted invoices minus posted credit notes,
        each for what it bills the order; a correction tied to one of its invoices only through its
        origin (credit or debit note typed by hand) counts too."""
        Move = self.env['account.move']
        moves = order.invoice_ids.filtered(lambda m: m.state == 'posted')
        if moves:
            domain = [('reversed_entry_id', 'in', moves.ids)]
            if 'debit_origin_id' in Move._fields:
                domain = ['|', ('debit_origin_id', 'in', moves.ids)] + domain
            moves |= Move.search([('state', '=', 'posted'), ('id', 'not in', moves.ids)] + domain)
        net = 0.0
        for move in moves:
            if move.move_type == 'out_invoice':
                net += self._salla_move_order_amount(move, order)
            elif move.move_type == 'out_refund':
                net -= self._salla_move_order_amount(move, order)
        return order.currency_id.round(net)

    def _salla_order_adjusted(self, order):
        """The order carries a posted adjustment (its total was brought to Salla's)."""
        return bool(order.invoice_ids.filtered(lambda m: m.state == 'posted').invoice_line_ids.filtered(
            lambda l: l.product_id.default_code == SALLA_ADJUST_CODE))

    def _salla_adjustment_product(self):
        Product = self.env['product.product'].with_context(active_test=False)
        product = Product.search([('default_code', '=', SALLA_ADJUST_CODE)], limit=1)
        if not product:
            product = Product.create({
                'name': 'Salla order total adjustment', 'default_code': SALLA_ADJUST_CODE,
                'type': 'service', 'invoice_policy': 'order', 'sale_ok': True, 'purchase_ok': False,
                'taxes_id': [(5, 0, 0)], 'supplier_taxes_id': [(5, 0, 0)],
            })
        return product

    def _salla_order_payment_journal(self, order, invoices):
        """Journal that received the order's money, or the one mapped to its Salla payment method."""
        for invoice in invoices:
            payments = invoice._get_reconciled_payments().filtered(
                lambda p: p.state not in ('cancel', 'canceled', 'rejected'))
            if payments:
                return payments[:1].journal_id
        channel = self.search([('channel', '=', 'salla'), ('company_id', '=', order.company_id.id)], limit=1)
        feed = self.env['order.feed'].search([('channel_id', 'in', channel.ids), ('name', '=', order.client_order_ref)], limit=1)
        mapping = self.env['channel.account.journal.mappings'].search([
            ('channel_id', 'in', channel.ids), ('store_journal_name', '=', feed.payment_method or '-')], limit=1)
        return self.env['account.journal'].browse(mapping.odoo_journal_id) if mapping else self.env['account.journal']

    def _salla_register_payment(self, move, journal, date):
        self._salla_lock_journal_posting(journal)
        self.env['account.payment.register'].with_context(active_model='account.move', active_ids=move.ids).create({
            'journal_id': journal.id, 'payment_date': date}).action_create_payments()

    def _salla_zero_tax(self, company):
        return self.search([('channel', '=', 'salla'), ('company_id', '=', company.id),
                            ('salla_zero_tax_id', '!=', False)], limit=1).salla_zero_tax_id

    def _salla_adjust_order_total(self, order, target, date=None, reason=None):
        """Bring the invoiced total of a Salla order to `target` (Salla's total, order currency).
        Returns the adjustment invoice or credit note (empty when nothing differs). `date` and
        `reason` date and describe it when it is not a total adjustment (return of the order)."""
        currency = order.currency_id
        diff = currency.round(target - self._salla_order_net(order))
        if currency.is_zero(diff):
            return self.env['account.move']
        standing = self._salla_standing_invoices(order)
        if not standing:
            raise ValueError('%s has no invoice to adjust' % order.name)
        base = standing.sorted(lambda m: (m.invoice_date or fields.Date.today(), m.id))[-1]
        product_lines = base.invoice_line_ids.filtered(lambda l: l.display_type == 'product')
        if len({tuple(sorted(line.tax_ids.ids)) for line in product_lines}) > 1:
            return self._salla_rebuild_order_invoice(order, target)
        taxes = product_lines[:1].tax_ids or self._salla_zero_tax(order.company_id)
        if not taxes or any(t.amount_type != 'percent' or t.price_include for t in taxes):
            raise ValueError('%s: taxes %s cannot carry an adjustment' % (base.name, taxes.mapped('name')))
        rate = sum(taxes.mapped('amount')) / 100.0
        locked = 'locked' in order._fields and order.locked
        if locked:
            order.action_unlock()
        tax_field = 'tax_ids' if 'tax_ids' in order.order_line._fields else 'tax_id'
        # a lower total is a negative quantity at a positive price: its credit note then carries a
        # positive quantity and price, as ZATCA wants
        sign = -1 if diff < 0 else 1
        line = self.env['sale.order.line'].create({
            'order_id': order.id, 'product_id': self._salla_adjustment_product().id, 'product_uom_qty': sign,
            'price_unit': currency.round(abs(diff) / (1 + rate)), tax_field: [(6, 0, taxes.ids)],
            'name': 'Salla order %s: total brought to Salla (%s %s)' % (order.client_order_ref, target, currency.name),
        })
        # the tax is rounded on the base: move the base by a cent until the line total is the difference
        for _attempt in range(6):
            gap = currency.round(abs(diff) - abs(line.price_total))
            if currency.is_zero(gap):
                break
            step = currency.round(gap / (1 + rate)) or math.copysign(currency.rounding, gap)
            line.price_unit = currency.round(line.price_unit + step)
        if not currency.is_zero(diff - line.price_total):
            raise ValueError('%s: the adjustment cannot reach %s to the cent' % (order.name, diff))
        if (order._get_invoiceable_lines(final=True) - line).filtered(lambda l: not l.display_type):
            raise ValueError('%s has other lines left to invoice' % order.name)
        move = order.with_context(raise_if_nothing_to_invoice=False)._create_invoices(final=True)
        if len(move) != 1:
            raise ValueError('%s: the adjustment was not invoiced' % order.name)
        vals = {'invoice_date': date or base.invoice_date, 'journal_id': base.journal_id.id,
                'ref': reason or 'Salla order %s: total brought to Salla (%s)' % (order.client_order_ref, base.name)}
        if move.move_type == 'out_refund':
            vals['reversed_entry_id'] = base.id
        elif 'debit_origin_id' in move._fields:
            vals['debit_origin_id'] = base.id
        move.write(vals)
        account = product_lines[:1].account_id
        if account:
            move.invoice_line_ids.filtered(lambda l: l.display_type == 'product').write({'account_id': account.id})
        self._salla_post_like_origin(move, base)
        if locked:
            order.action_lock()
        journal = self._salla_order_payment_journal(order, base)
        if move.move_type == 'out_refund':
            if base.amount_residual:
                receivable = (base.line_ids + move.line_ids).filtered(
                    lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled)
                if len(receivable) > 1:
                    receivable.reconcile()
            if move.amount_residual and journal:
                self._salla_register_payment(move, journal, move.invoice_date)
        elif self._salla_invoice_settled(base) and journal:
            self._salla_register_payment(move, journal, move.invoice_date)
        order.message_post(body='Invoiced total brought to Salla\'s total %s %s with %s.' % (target, currency.name, move.name))
        return move

    # ------------------------------------------------------------------ before the first invoice
    def _salla_total_tolerance(self, order):
        """Gap below which an order total is Salla's (Salla rounds foreign lines in their currency)."""
        return AMOUNT_TOLERANCE if order.currency_id == order.company_id.currency_id else AMOUNT_TOLERANCE_FOREIGN

    @api.model
    def _salla_feed_total(self, feed):
        """Total with VAT that the lines of an order feed (Salla's order as last imported) give in
        Odoo: products, delivery and charges add, discounts subtract, the VAT comes on top."""
        total = 0.0
        for line in feed.line_ids:
            try:
                base = round(float(line.line_price_unit or 0) * float(line.line_product_uom_qty or 1), 2)
                taxes = ast.literal_eval(line.line_taxes) if line.line_taxes else []
                rate = sum(float(t.get('rate') or 0) for t in taxes if not t.get('included_in_price'))
            except (TypeError, ValueError, SyntaxError, AttributeError):
                return None
            amount = base + round(base * rate / 100.0, 2)
            total += -amount if line.line_source == 'discount' else amount
        return round(total, 2)

    def _salla_order_target(self, order, channel):
        """Salla's total of an order about to be invoiced: the one the sweep just read from the
        Salla order list (context salla_order_totals), else the total of the order's feed."""
        amount, currency = (self.env.context.get('salla_order_totals') or {}).get(order.client_order_ref, (None, None))
        if amount is not None and currency in (False, '', order.currency_id.name):
            return amount
        feed = self.env['order.feed'].search([
            ('channel_id', '=', channel.id), ('name', '=', order.client_order_ref)], limit=1)
        return self._salla_feed_total(feed) if feed.line_ids else None

    def _salla_order_total_changed(self, order, total):
        """`order`, not invoiced yet, no longer has Salla's `total` ((amount, currency) of the
        Salla order list): the order was changed in Salla after the import."""
        if not order or not total or order.state == 'cancel' or total[0] is None:
            return False
        amount, currency = total
        if currency and currency != order.currency_id.name:
            return False
        if order.invoice_ids.filtered(lambda m: m.state != 'cancel'):
            return False
        return abs(order.amount_total - amount) > self._salla_total_tolerance(order)

    def _salla_adjust_lines_like_sales(self, invoice):
        """The adjustment lines of a draft invoice go to the income account of its other product
        lines, as the separate adjustments do, so the sales reports keep one account."""
        lines = invoice.invoice_line_ids.filtered(lambda l: l.display_type == 'product')
        adjust = lines.filtered(lambda l: l.product_id.default_code == SALLA_ADJUST_CODE)
        account = (lines - adjust)[:1].account_id
        if adjust and account and adjust.account_id != account:
            adjust.write({'account_id': account.id})

    def _salla_drop_order_lines(self, order, lines):
        """A confirmed order keeps its lines: the ones no longer wanted get no quantity instead."""
        if not lines:
            return
        if order.state == 'draft':
            lines.unlink()
        else:
            lines.write({'product_uom_qty': 0})

    def _salla_bring_order_to_total(self, order, target):
        """Before the first invoice of `order`, one adjustment line (rewritten on every call)
        brings the order to Salla's `target` total. Returns the line; nothing when the order
        already matches, is invoiced, or mixes VAT rates (the daily check corrects those later)."""
        SaleLine = self.env['sale.order.line']
        if target is None or order.state == 'cancel' or order.invoice_ids.filtered(lambda m: m.state != 'cancel'):
            return SaleLine
        currency = order.currency_id
        product = self._salla_adjustment_product()
        tax_field = 'tax_ids' if 'tax_ids' in SaleLine._fields else 'tax_id'
        lines = order.order_line.filtered(lambda l: not l.display_type)
        current = lines.filtered(lambda l: l.product_id == product)
        diff = currency.round(target - (order.amount_total - sum(current.mapped('price_total'))))
        locked = 'locked' in order._fields and order.locked
        if abs(diff) <= self._salla_total_tolerance(order):
            if current:
                if locked:
                    order.action_unlock()
                self._salla_drop_order_lines(order, current)
                if locked:
                    order.action_lock()
            return SaleLine
        priced = (lines - current).filtered(lambda l: l.product_uom_qty and l.price_unit)
        tax_sets = {tuple(sorted(l[tax_field].ids)) for l in priced}
        if len(tax_sets) > 1:
            _logger.info('Salla order %s differs from Salla by %s but mixes VAT rates: left to the daily check',
                         order.client_order_ref, diff)
            return SaleLine
        taxes = priced[:1][tax_field] or self._salla_zero_tax(order.company_id)
        if any(t.amount_type != 'percent' or t.price_include for t in taxes):
            return SaleLine
        rate = sum(taxes.mapped('amount')) / 100.0
        if locked:
            order.action_unlock()
        vals = {
            'price_unit': currency.round(diff / (1 + rate)), 'product_uom_qty': 1, tax_field: [(6, 0, taxes.ids)],
            'name': 'Salla order %s: total brought to Salla (%s %s)' % (order.client_order_ref, target, currency.name),
        }
        if current:
            line = current[0]
            line.write(vals)
            self._salla_drop_order_lines(order, current - line)
        else:
            line = SaleLine.create(dict(vals, order_id=order.id, product_id=product.id))
        # the tax is rounded on the base: move the base by a cent until the line total is the difference
        for _attempt in range(6):
            gap = currency.round(diff - line.price_total)
            if currency.is_zero(gap):
                break
            line.price_unit = currency.round(line.price_unit + (
                currency.round(gap / (1 + rate)) or math.copysign(currency.rounding, gap)))
        if locked:
            order.action_lock()
        order.message_post(body='Changed in Salla after the import: order brought to Salla\'s total %s %s '
                                'before its invoice.' % (target, currency.name))
        return line

    def _salla_refund_excess(self, order, payments, journal, date):
        """What the payments received above the rebuilt invoice goes back to the customer from the
        journal that received it, so that the journal holds what Salla collected."""
        credit = payments.move_id.line_ids.filtered(
            lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled)
        excess = -sum(credit.mapped('amount_residual_currency'))
        currency = order.currency_id
        if currency.compare_amounts(excess, 0) <= 0:
            return self.env['account.payment']
        self._salla_lock_journal_posting(journal)
        refund = self.env['account.payment'].create({
            'payment_type': 'outbound', 'partner_type': 'customer', 'partner_id': payments[:1].partner_id.id,
            'amount': currency.round(excess), 'currency_id': currency.id, 'journal_id': journal.id, 'date': date,
            'memo': 'Salla order %s: received above the invoice' % order.client_order_ref,
        })
        refund.action_post()
        (credit + refund.move_id.line_ids.filtered(
            lambda l: l.account_id.account_type == 'asset_receivable')).reconcile()
        return refund

    def _salla_rebuild_order_invoice(self, order, target):
        """The order's invoice mixes lines without VAT and lines under VAT (old imports; Salla puts
        VAT on every line): credit note for the invoice, the untaxed lines take the VAT of the other
        lines, the order is invoiced again and its payment moves to the new invoice. An order with
        no VAT at all in Salla (export) whose invoice taxed a line by mistake is invoiced again with
        the channel's 0% on every line; the money received above the new invoice goes back."""
        currency = order.currency_id
        standing = self._salla_standing_invoices(order)
        grouped = standing.filtered(lambda m: self._salla_move_other_orders(m, order))
        if grouped:
            # crediting it would take the sale of the other orders out of the books
            raise ValueError('%s: invoice %s also bills other orders' % (order.name, ', '.join(grouped.mapped('name'))))
        tax_field = 'tax_ids' if 'tax_ids' in order.order_line._fields else 'tax_id'
        vat = order.order_line.filtered(lambda l: not l.display_type).mapped(tax_field).filtered(
            lambda t: t.amount_type == 'percent' and t.amount > 0 and not t.price_include)
        if not vat and not order.order_line.filtered(lambda l: not l.display_type).mapped(tax_field):
            vat = self._salla_zero_tax(order.company_id)
        if len(vat) != 1:
            raise ValueError('%s: no single VAT to put on the untaxed lines' % order.name)
        payments = self.env['account.payment']
        for invoice in standing:
            payments |= invoice._get_reconciled_payments().filtered(lambda p: p.state not in ('cancel', 'canceled', 'rejected'))
        journal = self._salla_order_payment_journal(order, standing)
        # free the payments, credit every standing invoice
        for invoice in standing:
            invoice.line_ids.filtered(lambda l: l.account_id.account_type == 'asset_receivable').remove_move_reconcile()
            note = invoice._reverse_moves(default_values_list=[{
                'invoice_date': invoice.invoice_date, 'date': invoice.date,
                'ref': 'Salla order %s: VAT of every line as in Salla (%s)' % (order.client_order_ref, invoice.name),
            }], cancel=False)
            self._salla_post_credit_note(note)
            (invoice.line_ids + note.line_ids).filtered(
                lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled).reconcile()
        locked = 'locked' in order._fields and order.locked
        if locked:
            order.action_unlock()
        order.order_line.filtered(lambda l: not l.display_type and vat not in l[tax_field]).write({tax_field: [(6, 0, vat.ids)]})
        new = order.with_context(raise_if_nothing_to_invoice=False)._create_invoices(final=True)
        if len(new) != 1 or new.move_type != 'out_invoice':
            raise ValueError('%s: the order was not invoiced again' % order.name)
        base = standing.sorted(lambda m: (m.invoice_date or fields.Date.today(), m.id))[-1]
        new.write({'invoice_date': base.invoice_date, 'journal_id': base.journal_id.id})
        self._salla_post_new(new)
        if locked:
            order.action_lock()
        receivable = new.line_ids.filtered(lambda l: l.account_id.account_type == 'asset_receivable')
        for payment in payments:
            lines = (receivable + payment.move_id.line_ids).filtered(
                lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled)
            if len(lines) > 1:
                lines.reconcile()
        if new.amount_residual > 0 and payments and journal:
            self._salla_register_payment(new, journal, new.invoice_date)
        elif payments and journal:
            self._salla_refund_excess(order, payments, journal, new.invoice_date)
        leftover = currency.round(target - self._salla_order_net(order))
        if not currency.is_zero(leftover):
            return self._salla_adjust_order_total(order, target)
        order.message_post(body='Invoice rebuilt with the VAT of every line as in Salla: %s.' % new.name)
        return new
