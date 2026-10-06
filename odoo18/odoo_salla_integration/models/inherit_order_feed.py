# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from odoo import fields, models

from .salla_refunds import SALLA_REFUND_STATES

_logger = logging.getLogger(__name__)


class OrderFeed(models.Model):
    _inherit = 'order.feed'

    def _apply_order_import(self, channel_id, vals, match, store_id, store_source,
                            store_partner_id, date_invoice, date_shipping, confirmation_date):
        if channel_id.channel == 'salla' and not match:
            match = self._salla_existing_order_mapping(channel_id, vals, store_id, store_source)
        return super()._apply_order_import(
            channel_id, vals, match, store_id, store_source,
            store_partner_id, date_invoice, date_shipping, confirmation_date)

    def _salla_existing_order_mapping(self, channel_id, vals, store_id, store_source):
        """A Salla order that is already in Odoo (an older import that left no mapping) is mapped
        instead of being created a second time."""
        ref = vals.get('client_order_ref') or self.name
        if not ref:
            return False
        order = self.env['sale.order'].search([
            ('client_order_ref', '=', ref), ('company_id', '=', channel_id.company_id.id),
            ('state', '!=', 'cancel')], order='id', limit=1)
        if not order:
            return False
        _logger.info('Salla order %s already exists as %s: mapped, not created again', ref, order.name)
        return channel_id.create_order_mapping(order, store_id, store_source, vals.get('order_state'))

    def import_order(self, channel_id):
        res = super().import_order(channel_id)
        if channel_id.channel != 'salla':
            return res
        mapping = res.get('update_id') or res.get('create_id')
        order = mapping and mapping.order_name
        if order and self.order_state in SALLA_REFUND_STATES:
            self._salla_refund_returned_order(channel_id, order)
            return res
        if self.state != 'done' or not order:
            return res
        state_map = (
            channel_id.order_state_ids.filtered(lambda s: s.channel_state == self.order_state)
            or channel_id.order_state_ids.filtered('default_order_state')
        )
        if not state_map or not state_map[0].odoo_create_invoice:
            return res
        posted = order.invoice_ids.filtered(
            lambda move: move.move_type == 'out_invoice' and move.state == 'posted')
        problem = False
        if not posted:
            problem = 'Invoice was not created or posted for a Salla status that requires one'
        elif state_map[0].odoo_set_invoice_state == 'paid' and any(
            move.payment_state not in ('paid', 'in_payment', 'reversed') for move in posted
        ):
            problem = 'Invoice posted but the payment was not registered'
        if problem:
            # Error state makes the feed evaluation cron retry it automatically.
            self.set_feed_state(state='error')
            self.message = "<span class='text-danger'>%s</span><br/>%s" % (problem, self.message)
            res['message'] = (res.get('message') or '') + '<br/>' + problem
        return res

    def _salla_refund_returned_order(self, channel_id, order):
        """Salla says the order came back: credit note (and refund of the money) for its invoices."""
        try:
            with self.env.cr.savepoint():
                notes = channel_id._salla_refund_order(order)
        except Exception as e:
            self.message = "<span class='text-danger'>Refund of the returned order failed: %s</span><br/>%s" % (e, self.message)
            self.set_feed_state(state='error')
            return
        if notes:
            self.message = 'Order returned in Salla: credit note %s created.<br/>%s' % (', '.join(notes.mapped('name')), self.message)

    def get_taxes_ids(self, taxes):
        """Salla sends no tax for zero-rated lines (exports); give them the channel's 0% tax."""
        res = super().get_taxes_ids(taxes)
        channel = self.channel_id
        if channel.channel == 'salla':
            tax_ids = [tid for command in res or [] if command and command[0] == 6 for tid in command[2]]
            if tax_ids:
                channel._salla_complete_taxes(self.env['account.tax'].browse(tax_ids))
        if channel.channel != 'salla' or not channel.salla_zero_tax_id:
            return res
        for command in res or []:
            if command and command[0] == 6 and command[2]:
                return res
        return [(6, 0, channel.salla_zero_tax_id.ids)]


class _SallaInvoiceRollback(Exception):
    """Internal: unwind a failed invoice posting (carries the connector result)."""


class MultiChannelSkeleton(models.TransientModel):
    _inherit = 'multi.channel.skeleton'

    def SetOrderPaid(self, payment_data):
        """Salla: post the invoice on the order date, register the payment on that same date,
        and never leave an invoice posted when the step failed.

        The base method registers the payment on today's date (the wizard default) and swallows
        errors raised after posting (ZATCA validation), which left posted invoices without
        payment or EDI document on production.
        """
        channel = payment_data.get('channel_id')
        if not channel or getattr(channel, 'channel', False) != 'salla':
            return super().SetOrderPaid(payment_data)
        order = self.env['sale.order'].browse(payment_data.get('order_id'))
        posted_before = set(order.invoice_ids.filtered(lambda m: m.state == 'posted').ids)
        try:
            with self.env.cr.savepoint():
                res = self._salla_set_order_paid(order, payment_data.get('journal_id'), payment_data.get('date_invoice'),
                                                 channel=channel)
                if not res.get('status'):
                    order.invalidate_recordset(['invoice_ids'])
                    posted_after = set(order.invoice_ids.filtered(lambda m: m.state == 'posted').ids)
                    if posted_after - posted_before:
                        raise _SallaInvoiceRollback(res)
        except _SallaInvoiceRollback as unwind:
            res = dict(unwind.args[0])
            res['status_message'] = (res.get('status_message') or '') + \
                '<br/>The invoice posting was rolled back; fix the cause and evaluate the feed again.'
        return res

    def _salla_zero_tax_order_lines(self, order, zero):
        """Order lines imported without any tax get the channel's 0% tax (the Saudi e-invoicing
        refuses an invoice line without tax); new imports already do this in get_taxes_ids."""
        tax_field = 'tax_ids' if 'tax_ids' in order.order_line._fields else 'tax_id'
        lines = order.order_line.filtered(lambda l: not l.display_type and not l[tax_field])
        if lines:
            lines.with_context(skip_tax_fix=True).write({tax_field: [(6, 0, zero.ids)]})

    def _salla_local_date(self, value, channel=None):
        """Invoice date of a Salla order: the day of the order in the store's time zone.
        The order date is stored in UTC, so an order placed between midnight and 03:00 in
        Riyadh would otherwise be invoiced on the previous day (or year)."""
        if not value:
            return value
        if isinstance(value, str):
            value = fields.Datetime.to_datetime(value) if len(value) > 10 else fields.Date.to_date(value)
        if isinstance(value, datetime):
            tz = (channel and channel.wk_time_zone) or self.env.user.tz or 'Asia/Riyadh'
            return fields.Date.context_today(self.with_context(tz=tz), timestamp=value)
        return value

    def _salla_set_order_paid(self, order, journal_id, date_invoice, channel=None):
        status_message = ''
        date_invoice = self._salla_local_date(date_invoice, channel)
        zero = channel.salla_zero_tax_id if channel and 'salla_zero_tax_id' in channel._fields else False
        if zero:
            self._salla_zero_tax_order_lines(order, zero)
        Channel = self.env['multi.channel.sale']
        settled = Channel._salla_invoice_settled
        # an invoice whose part for this order was credited in full (a grouped invoice reversed
        # for another order) does not bill the order any more
        standing = Channel._salla_standing_invoices(order)
        invoices = order.invoice_ids.filtered(lambda m: m.move_type == 'out_invoice' and m.state == 'draft') \
            | standing.filtered(lambda m: not settled(m))
        # A draft that already carries a number (posted once, then reset) cannot be posted again
        # in a hash-locked journal ("a gap has been detected in the sequence"): a fresh invoice
        # with the next number replaces it.
        stale = invoices.filtered(lambda m: m.state == 'draft' and m.name and m.name != '/')
        if stale:
            stale.button_cancel()
            status_message += 'Old draft %s cancelled. ' % ', '.join(stale.mapped('name'))
            invoices -= stale
        if not invoices and channel:
            # changed in Salla after the import (a coupon added or removed): the first invoice
            # already carries Salla's total
            try:
                with self.env.cr.savepoint():
                    Channel._salla_bring_order_to_total(order, Channel._salla_order_target(order, channel))
            except Exception as e:  # the invoice goes on; the daily check corrects the total later
                _logger.warning("Salla order %s not brought to Salla's total: %s", order.client_order_ref, e)
                status_message += "Total not brought to Salla's: %s. " % e
        if not invoices and standing.filtered(settled):
            return {'status': True, 'status_message': 'Invoice already paid. '}
        if not invoices and order.invoice_ids:
            # the connector refuses to invoice an order that has any invoice, even a cancelled one
            try:
                invoices = order.with_context(raise_if_nothing_to_invoice=False)._create_invoices()[:1]
            except Exception as e:
                return {'status': False, 'status_message': status_message + '<br/>Error in creating Invoice: %s <br/>' % e}
            if not invoices:
                return {'status': False, 'status_message': status_message + '<br/>Nothing left to invoice on the order.<br/>'}
            status_message += 'Invoice==> Created. '
        elif not invoices:
            created = self.create_order_invoice(order)
            status_message += created.get('status_message') or ''
            if not created.get('status'):
                return {'status': False, 'status_message': status_message}
            invoices = created['invoice_id']
        if len(invoices) > 1:
            return {'status': False, 'status_message': status_message +
                    '<br/>Multiple validated Invoices found for the Odoo order. Cannot make Payment<br/>'}
        invoice = invoices[0]
        try:
            if invoice.state == 'draft':
                if zero:
                    invoice.invoice_line_ids.filtered(
                        lambda l: l.display_type == 'product' and not l.tax_ids
                    ).write({'tax_ids': [(6, 0, zero.ids)]})
                if date_invoice:
                    invoice.write({'invoice_date': date_invoice})
                Channel._salla_adjust_lines_like_sales(invoice)
                if self.env.context.get('salla_repair'):
                    # audit and backfill runs post like every other Salla correction
                    Channel._salla_post_new(invoice)
                else:
                    Channel._salla_lock_journal_posting(invoice.journal_id)
                    invoice.action_post()
            if invoice.payment_state in ('paid', 'in_payment', 'reversed'):
                return {'status': True, 'status_message': status_message + 'Invoice already paid. '}
            payment_date = invoice.invoice_date or fields.Date.context_today(self)
            self.env['multi.channel.sale']._salla_lock_journal_posting(self.env['account.journal'].browse(journal_id))
            wizard = self.env['account.payment.register'].with_context(
                active_model='account.move', active_ids=invoice.ids,
            ).create({'journal_id': journal_id, 'payment_date': payment_date})
            wizard.action_create_payments()
            status_message += 'Invoice==> Paid. '
        except Exception as e:
            return {'status': False, 'status_message': status_message + '<br/>Error while invoice processing.%r<br/>' % (e,)}
        return {'status': True, 'status_message': status_message}
