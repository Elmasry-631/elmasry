# -*- coding: utf-8 -*-
"""Salla order audit.

Lists every order of a date range through the Salla order list API (30 per call, read only;
about 20 orders a second instead of the 0.3 of a full import), stores one line per order with
its status, total and payment method, then compares each line with Odoo: mapping, sale order,
duplicates, invoice and payment expected by the channel's order-state mapping, credit note
for returned orders, total. Only the orders that need it are then sent to a backfill.
Both phases run from the cron "Salla - Order Audit" with a time budget and resume by
themselves, so a range of months never depends on one HTTP request.
"""
import json
import logging
import time
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from .salla_refunds import SALLA_REFUND_STATES

_logger = logging.getLogger(__name__)

AUDIT_TIME_BUDGET = 420      # seconds of work per cron run
AUDIT_PER_PAGE = 30
AUDIT_COMPARE_BATCH = 500
AUDIT_FIX_BATCH = 20
AUDIT_WINDOW_DAYS = 7
AUDIT_MAX_PAGES = 500      # Salla stops paging after 500 pages
# daily automatic check: number of days listed (0 = off) and the progress of today's check
DAILY_DAYS_PARAM = 'odoo_salla_integration.daily_check_days'
DAILY_STATE_PARAM = 'odoo_salla_integration.daily_check_state'
AMOUNT_TOLERANCE = 0.05
# Salla converts every line to the customer's currency and rounds it there
AMOUNT_TOLERANCE_FOREIGN = 0.5

CATEGORIES = [
    ('ok', 'OK'),
    ('missing', 'Missing in Odoo'),
    ('duplicate', 'Duplicate orders in Odoo'),
    ('unmapped', 'In Odoo without channel mapping'),
    ('should_refund', 'Returned, invoice not credited'),
    ('not_invoiced', 'Should be invoiced, no posted invoice'),
    ('not_paid', 'Should be paid, invoice not paid'),
    ('status_diff', 'Status differs from Salla'),
    ('amount_diff', 'Total differs from Salla'),
]
# categories the importer can fix by importing the order again
IMPORT_CATEGORIES = ('missing', 'unmapped', 'should_refund', 'status_diff')
# categories fixed in Odoo without asking Salla again (invoice and pay the existing order)
FIX_CATEGORIES = ('not_invoiced', 'not_paid')


class SallaOrderAudit(models.Model):
    _name = 'salla.order.audit'
    _description = 'Salla Order Audit'
    _order = 'id desc'

    name = fields.Char(compute='_compute_name', store=True)
    channel_id = fields.Many2one(
        'multi.channel.sale', required=True, ondelete='cascade',
        domain="[('channel', '=', 'salla')]",
        default=lambda self: self.env['multi.channel.sale'].search([('channel', '=', 'salla')], limit=1))
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True, default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('collecting', 'Listing Salla orders'),
        ('comparing', 'Comparing with Odoo'),
        ('fixing', 'Invoicing and paying'),
        ('adjusting', 'Bringing totals to Salla'),
        ('done', 'Done'),
    ], default='draft', required=True, copy=False)
    next_page = fields.Integer(default=1, copy=False)
    window_start = fields.Date(copy=False, help='Start of the week being listed.')
    line_ids = fields.One2many('salla.order.audit.line', 'audit_id', copy=False)
    line_count = fields.Integer(compute='_compute_counts')
    problem_count = fields.Integer(compute='_compute_counts')
    compared_count = fields.Integer(compute='_compute_counts')
    summary = fields.Text(copy=False, readonly=True)
    last_run = fields.Datetime(copy=False)
    last_error = fields.Text(copy=False)
    backfill_id = fields.Many2one('salla.order.backfill', copy=False, readonly=True)

    @api.depends('channel_id', 'date_from', 'date_to')
    def _compute_name(self):
        for rec in self:
            rec.name = 'Audit %s -> %s' % (rec.date_from or '', rec.date_to or '')

    def _compute_counts(self):
        Line = self.env['salla.order.audit.line']
        for rec in self:
            rec.line_count = Line.search_count([('audit_id', '=', rec.id)])
            rec.compared_count = Line.search_count([('audit_id', '=', rec.id), ('checked', '=', True)])
            rec.problem_count = Line.search_count([('audit_id', '=', rec.id), ('checked', '=', True),
                                                   ('category', '!=', 'ok')])

    # ------------------------------------------------------------------ actions
    def action_start(self):
        for rec in self:
            if rec.date_to < rec.date_from:
                raise UserError(_('The end date must be after the start date.'))
            if rec.channel_id.state != 'validate':
                raise UserError(_('The channel is not connected.'))
            rec.line_ids.unlink()
            rec.write({'state': 'collecting', 'next_page': 1, 'window_start': rec.date_from,
                       'summary': False, 'last_error': False})
        return True

    def action_compare_again(self):
        """Compare the collected lines with Odoo again (after an import), without listing Salla again."""
        for rec in self:
            rec.line_ids.write({'checked': False})
            rec.write({'state': 'comparing', 'summary': False})
        return True

    def action_run_now(self):
        self.ensure_one()
        if self.state not in ('collecting', 'comparing', 'fixing', 'adjusting'):
            raise UserError(_('Start the audit first.'))
        self._process(AUDIT_TIME_BUDGET)
        return True

    def action_open_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': self.name,
            'res_model': 'salla.order.audit.line',
            'view_mode': 'list,pivot,form',
            'domain': [('audit_id', '=', self.id)],
            'context': {'search_default_problems': 1, 'search_default_group_category': 1},
        }

    def action_import_problems(self):
        """Create a backfill with the orders the importer can fix (missing, unmapped, status,
        invoice, payment, returned). Duplicates are left to "Salla: Cancel duplicate orders"."""
        self.ensure_one()
        # a status that differs from the last import also blocks "Invoice and Pay" (it reads the
        # status of the order feed), so those orders are imported again whatever their category
        lines = self.line_ids.filtered(lambda l: l.checked and (
            l.category in IMPORT_CATEGORIES or 'Odoo status' in (l.issues or '')))
        ids = list(dict.fromkeys(lines.mapped('store_id')))
        if not ids:
            raise UserError(_('Nothing to import.'))
        import json
        backfill = self.env['salla.order.backfill'].create({
            'channel_id': self.channel_id.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'order_ids_json': json.dumps(ids),
            'failed_ids_json': '[]',
            'total_count': len(ids),
            'done_count': 0,
            'state': 'running',
        })
        self.backfill_id = backfill
        return {
            'type': 'ir.actions.act_window', 'res_model': 'salla.order.backfill',
            'res_id': backfill.id, 'view_mode': 'form',
        }

    # ------------------------------------------------------------------ cron
    @api.model
    def cron_process(self):
        try:
            self._daily_check()
        except Exception as e:  # never block the audits in progress
            _logger.exception('Salla daily check failed: %s', e)
            self.env.cr.rollback()
        for audit in self.search([('state', 'in', ('collecting', 'comparing', 'fixing', 'adjusting'))], order='id'):
            try:
                audit._process(AUDIT_TIME_BUDGET)
            except Exception as e:
                _logger.exception('Salla audit %s failed: %s', audit.id, e)
                self.env.cr.rollback()
                audit.write({'last_error': str(e)[:1000]})
                self._audit_commit()
        return True

    @api.model
    def _daily_check(self):
        """Once a day, list the orders of the last days and bring Odoo to Salla, step by step
        (each step waits for the cron to finish the previous one): import the orders whose status or
        presence differs, compare again, invoice and pay, bring the totals to Salla. Everything it
        posts goes through the Salla corrections (kept out of ZATCA while they are on hold)."""
        ICP = self.env['ir.config_parameter'].sudo()
        days = int(ICP.get_param(DAILY_DAYS_PARAM) or 0)
        if days <= 0:
            return
        state = json.loads(ICP.get_param(DAILY_STATE_PARAM) or '{}')
        today = fields.Date.context_today(self)
        audit = self.browse(state.get('audit') or []).exists()
        stage = state.get('stage')
        if not audit or (stage == 'finished' and state.get('date') != str(today)):
            if state.get('date') == str(today):
                return
            channel = self.env['multi.channel.sale'].search([('channel', '=', 'salla'), ('state', '=', 'validate')], limit=1)
            if not channel:
                return
            audit = self.create({'channel_id': channel.id, 'date_from': today - timedelta(days=days), 'date_to': today})
            audit.action_start()
            state = {'date': str(today), 'audit': audit.id, 'stage': 'listing'}
        elif audit.state != 'done' or stage == 'finished':
            return
        elif stage == 'listing':
            if audit.line_ids.filtered(lambda l: l.category in IMPORT_CATEGORIES or 'Odoo status' in (l.issues or '')):
                audit.action_import_problems()
                state['stage'] = 'importing'
            else:
                state['stage'] = 'imported'
        elif stage == 'importing':
            if audit.backfill_id and audit.backfill_id.state != 'done':
                return
            audit.action_compare_again()
            state['stage'] = 'imported'
        elif stage == 'imported':
            if audit.line_ids.filtered(lambda l: l.category in FIX_CATEGORIES):
                audit.action_fix_invoices()
            state['stage'] = 'fixed'
        elif stage == 'fixed':
            if audit.line_ids.filtered(lambda l: l.category == 'amount_diff'):
                audit.action_adjust_totals()
            state['stage'] = 'finished'
        ICP.set_param(DAILY_STATE_PARAM, json.dumps(state))
        self._audit_commit()

    def _audit_commit(self):
        # same test-run detection as the repair actions (Odoo 18 does not flag the registry)
        self.env['multi.channel.sale']._salla_repair_commit()

    def _process(self, time_budget):
        self.ensure_one()
        start = time.time()
        if self.state == 'collecting':
            self._collect(start, time_budget)
        if self.state == 'comparing' and (time.time() - start) < time_budget:
            self._compare(start, time_budget)
        if self.state == 'fixing' and (time.time() - start) < time_budget:
            self._fix(start, time_budget)
        if self.state == 'adjusting' and (time.time() - start) < time_budget:
            self._adjust(start, time_budget)
        self.last_run = fields.Datetime.now()
        self._audit_commit()

    def _window(self):
        """Current listing window: one week, so a query never reaches Salla's 500-page limit."""
        window_from = self.window_start or self.date_from
        return window_from, min(window_from + timedelta(days=AUDIT_WINDOW_DAYS - 1), self.date_to)

    def _collect(self, start, time_budget):
        channel = self.channel_id
        if not channel._salla_try_acquire_order_import_lock():
            _logger.info('Salla audit %s: channel busy, retry next run', self.id)
            return
        try:
            channel.with_context(operation=True).getAccessToken()
            api = channel.get_sallaApi()
            Line = self.env['salla.order.audit.line']
            known = set(Line.search([('audit_id', '=', self.id)]).mapped('store_id'))
            while (time.time() - start) < time_budget:
                window_from, window_to = self._window()
                res = api.salla_response(api.import_url + 'orders', params={
                    'from_date': window_from.strftime('%Y-%m-%d'),
                    'to_date': window_to.strftime('%Y-%m-%d'),
                    'per_page': AUDIT_PER_PAGE,
                    'page': self.next_page,
                    'sort_by': 'created_at-asc',
                })
                rows = (res or {}).get('data') or []
                vals = []
                for row in rows:
                    store_id = str(row.get('id') or '')
                    if not store_id or store_id in known:
                        continue
                    known.add(store_id)
                    vals.append(self._line_vals(row))
                if vals:
                    Line.create(vals)
                links = ((res or {}).get('pagination') or {}).get('links') or {}
                if not rows or not links.get('next'):
                    if self.next_page >= AUDIT_MAX_PAGES:
                        self.last_error = 'Salla stopped paging at page %s for %s..%s: orders may be missing' % (
                            self.next_page, window_from, window_to)
                    if window_to >= self.date_to:
                        self.write({'state': 'comparing', 'next_page': 1, 'window_start': False})
                        self._audit_commit()
                        _logger.info('Salla audit %s: %s order(s) listed', self.id, len(known))
                        return
                    self.write({'window_start': window_to + timedelta(days=1), 'next_page': 1})
                else:
                    self.next_page += 1
                self._audit_commit()
        finally:
            channel._salla_release_order_import_lock()

    # ------------------------------------------------------------------ invoice and pay
    def action_fix_invoices(self):
        """Invoice and pay the orders whose Salla status needs a paid invoice (categories
        "no posted invoice" and "invoice not paid"), the way the connector does: invoice on the
        order date, payment in the journal of the Salla payment method on that same date."""
        for rec in self:
            lines = rec.line_ids.filtered(lambda l: l.category in FIX_CATEGORIES)
            if not lines:
                raise UserError(_('Nothing to invoice or pay.'))
            lines.write({'fix_done': False, 'fix_error': False})
            rec.write({'state': 'fixing'})
        return True

    def action_adjust_totals(self):
        """Bring the invoiced total of the orders whose total differs from Salla to Salla's total
        (the order was edited in Salla after the import): an adjustment invoice or credit note per
        order, paid or refunded like the order. Journals without ZATCA onboarding are included."""
        for rec in self:
            lines = rec.line_ids.filtered(lambda l: l.category == 'amount_diff')
            if not lines:
                raise UserError(_('No total differs from Salla.'))
            lines.write({'fix_done': False, 'fix_error': False})
            rec.write({'state': 'adjusting'})
        return True

    def _adjust(self, start, time_budget):
        Line = self.env['salla.order.audit.line']
        Channel = self.env['multi.channel.sale'].with_context(salla_repair=True)
        rules = self._state_rules()
        while (time.time() - start) < time_budget:
            lines = Line.search([('audit_id', '=', self.id), ('category', '=', 'amount_diff'),
                                 ('fix_done', '=', False)], limit=AUDIT_FIX_BATCH)
            if not lines:
                self.write({'state': 'done', 'summary': self._summary()})
                self._audit_commit()
                return
            for line in lines:
                error = False
                try:
                    with self.env.cr.savepoint():
                        order = line.order_id
                        if not order or order.state == 'cancel':
                            raise ValueError('no live Odoo order')
                        if order.currency_id.name != line.currency or not line.total_known:
                            raise ValueError('Salla total in %s, order in %s' % (line.currency, order.currency_id.name))
                        Channel._salla_adjust_order_total(order, line.total)
                except Exception as e:  # keep going, the error stays on the line
                    error = str(e)[:250]
                line.order_id.invalidate_recordset()
                self._compare_lines(line, rules)
                line.write({'fix_done': True, 'fix_error': error})
            self._audit_commit()

    def _fix(self, start, time_budget):
        Line = self.env['salla.order.audit.line']
        Channel = self.env['multi.channel.sale'].with_context(salla_repair=True)
        rules = self._state_rules()
        while (time.time() - start) < time_budget:
            lines = Line.search([('audit_id', '=', self.id), ('category', 'in', FIX_CATEGORIES),
                                 ('fix_done', '=', False)], limit=AUDIT_FIX_BATCH)
            if not lines:
                self.write({'state': 'done', 'summary': self._summary()})
                self._audit_commit()
                return
            for line in lines:
                error = False
                try:
                    with self.env.cr.savepoint():
                        if not line.order_id:
                            raise ValueError('no Odoo order')
                        if not Channel._salla_pay_repaired_orders(self.channel_id, line.order_id):
                            raise ValueError('no journal mapping or status not mapped to a paid invoice')
                except Exception as e:  # keep going, the error stays on the line
                    error = str(e)[:250]
                line.order_id.invalidate_recordset()
                self._compare_lines(line, rules)
                line.write({'fix_done': True, 'fix_error': error})
            self._audit_commit()

    def _line_vals(self, row):
        total = row.get('total') or {}
        amounts = row.get('amounts') or {}
        if not total and amounts:
            total = amounts.get('total') or {}
        status = row.get('status') or {}
        raw_date = ((row.get('date') or {}).get('date') or '')[:19]
        order_date = False
        if raw_date:
            try:
                order_date = fields.Date.to_date(raw_date[:10])
            except ValueError:
                order_date = False
        payment = row.get('payment_method')
        if isinstance(payment, dict):
            payment = payment.get('slug') or payment.get('name')
        return {
            'audit_id': self.id,
            'store_id': str(row.get('id')),
            'reference': str(row.get('reference_id') or row.get('id')),
            'order_date': order_date,
            'order_datetime': raw_date,
            'status': status.get('slug') or '',
            'status_name': status.get('name') or '',
            'total': float(total.get('amount') or 0.0),
            'total_known': total.get('amount') is not None,
            'currency': total.get('currency') or row.get('currency') or '',
            'payment_method': payment or '',
        }

    def _compare(self, start, time_budget):
        Line = self.env['salla.order.audit.line']
        rules = self._state_rules()
        while (time.time() - start) < time_budget:
            lines = Line.search([('audit_id', '=', self.id), ('checked', '=', False)], limit=AUDIT_COMPARE_BATCH)
            if not lines:
                self.write({'state': 'done', 'summary': self._summary()})
                self._audit_commit()
                return
            self._compare_lines(lines, rules)
            self._audit_commit()

    def _state_rules(self):
        rules = {}
        default = False
        for rule in self.channel_id.order_state_ids:
            rules[rule.channel_state] = rule
            if rule.default_order_state:
                default = rule
        rules[None] = default
        return rules

    def _compare_lines(self, lines, rules):
        channel = self.channel_id
        company = channel.company_id
        mappings = self.env['channel.order.mappings'].search([
            ('channel_id', '=', channel.id), ('store_order_id', 'in', lines.mapped('store_id'))])
        mapping_by_store = {}
        for mapping in mappings:
            mapping_by_store.setdefault(mapping.store_order_id, mapping)
        orders = self.env['sale.order'].search([
            ('client_order_ref', 'in', lines.mapped('reference')), ('company_id', '=', company.id),
            ('state', '!=', 'cancel')])
        orders_by_ref = {}
        for order in orders:
            orders_by_ref.setdefault(order.client_order_ref, self.env['sale.order'])
            orders_by_ref[order.client_order_ref] |= order
        # orders cancelled in Odoo: fine when Salla cancelled them too
        cancelled = self.env['sale.order'].search([
            ('client_order_ref', 'in', lines.mapped('reference')), ('company_id', '=', company.id),
            ('state', '=', 'cancel')])
        cancelled_by_ref = {}
        for order in cancelled:
            cancelled_by_ref.setdefault(order.client_order_ref, order)
        Channel = self.env['multi.channel.sale']
        for line in lines:
            mapping = mapping_by_store.get(line.store_id)
            mapped_order = mapping.order_name if mapping and mapping.order_name and mapping.order_name.state != 'cancel' else False
            live = orders_by_ref.get(line.reference, self.env['sale.order'])
            order = mapped_order or live[:1]
            issues = []
            invoice_state = 'none'
            rule = rules.get(line.status) or rules.get(None)
            if not order and rule and rule.odoo_order_state == 'cancelled' and cancelled_by_ref.get(line.reference):
                order = cancelled_by_ref[line.reference]
                category = 'ok'
            elif not order:
                category = 'missing'
                issues.append('not in Odoo')
            else:
                standing = Channel._salla_standing_invoices(order)
                if standing and all(Channel._salla_invoice_settled(m) for m in standing):
                    invoice_state = 'paid'
                elif standing:
                    invoice_state = 'posted'
                elif order.invoice_ids.filtered(lambda m: m.move_type == 'out_refund' and m.state == 'posted'):
                    invoice_state = 'credited'
                rule = rules.get(line.status) or rules.get(None)
                if len(live | (mapped_order or self.env['sale.order'])) > 1:
                    issues.append('%d live orders' % len(live | (mapped_order or self.env['sale.order'])))
                if not mapped_order:
                    issues.append('no channel mapping')
                if line.status in SALLA_REFUND_STATES:
                    if standing:
                        issues.append('returned but invoice %s not credited' % ', '.join(standing.mapped('name')))
                elif rule and rule.odoo_order_state != 'cancelled' and rule.odoo_create_invoice:
                    if not standing:
                        # a credited invoice (a grouped invoice reversed for another order) leaves
                        # the sale out of the books as much as no invoice at all
                        issues.append('no posted invoice' if invoice_state != 'credited' else 'no posted invoice (credited)')
                    elif rule.odoo_set_invoice_state == 'paid' and invoice_state == 'posted':
                        issues.append('invoice not paid')
                if mapping and (mapping.store_order_status or '') != line.status:
                    issues.append('Odoo status %s' % (mapping.store_order_status or '-'))
                # what the books hold for the order: the invoiced net once invoiced, else the order
                # total; a returned or cancelled order must net to zero, its total does not matter
                odoo_total = Channel._salla_order_net(order) if order.invoice_ids.filtered(
                    lambda m: m.state == 'posted') else order.amount_total
                tolerance = AMOUNT_TOLERANCE if line.currency == company.currency_id.name else AMOUNT_TOLERANCE_FOREIGN
                if line.total_known and order.currency_id.name == line.currency and invoice_state != 'credited' \
                        and line.status not in SALLA_REFUND_STATES and abs(odoo_total - line.total) > tolerance:
                    issues.append('Odoo total %.2f' % odoo_total)
                category = self._category(issues)
            line.write({
                'order_id': order.id if order else False,
                'order_count': len(live),
                'odoo_status': mapping.store_order_status if mapping else False,
                'odoo_total': (Channel._salla_order_net(order) if order.invoice_ids.filtered(
                    lambda m: m.state == 'posted') else order.amount_total) if order else 0.0,
                'invoice_state': invoice_state,
                'category': category,
                'issues': '; '.join(issues),
                'checked': True,
            })

    @staticmethod
    def _category(issues):
        text = ' | '.join(issues)
        for key, needle in (('duplicate', 'live orders'), ('unmapped', 'no channel mapping'),
                            ('should_refund', 'not credited'), ('not_invoiced', 'no posted invoice'),
                            ('not_paid', 'invoice not paid'), ('status_diff', 'Odoo status'),
                            ('amount_diff', 'Odoo total')):
            if needle in text:
                return key
        return 'ok'

    def _summary(self):
        Line = self.env['salla.order.audit.line']
        labels = dict(CATEGORIES)
        rows = Line.read_group([('audit_id', '=', self.id)], ['total:sum'], ['category'], lazy=False)
        out = ['%s: %d order(s), %.2f' % (labels.get(r['category'], r['category']), r['__count'], r['total'] or 0.0)
               for r in sorted(rows, key=lambda r: -r['__count'])]
        return '\n'.join(out)


class SallaOrderAuditLine(models.Model):
    _name = 'salla.order.audit.line'
    _description = 'Salla Order Audit Line'
    _order = 'order_datetime, id'
    _rec_name = 'reference'

    audit_id = fields.Many2one('salla.order.audit', required=True, ondelete='cascade', index=True)
    store_id = fields.Char('Salla order id', index=True)
    reference = fields.Char('Salla reference', index=True)
    order_date = fields.Date('Order date')
    order_datetime = fields.Char('Salla date')
    status = fields.Char('Salla status')
    status_name = fields.Char('Salla status name')
    total = fields.Float('Salla total')
    total_known = fields.Boolean(help='Salla sent a total for this order in the list.')
    currency = fields.Char()
    payment_method = fields.Char()
    checked = fields.Boolean(index=True)
    order_id = fields.Many2one('sale.order', 'Odoo order')
    order_count = fields.Integer('Live Odoo orders')
    odoo_status = fields.Char('Odoo status')
    odoo_total = fields.Float('Odoo total')
    total_diff = fields.Float(compute='_compute_total_diff', store=True)
    invoice_state = fields.Selection([
        ('none', 'No invoice'), ('posted', 'Invoiced, not paid'), ('paid', 'Paid'), ('credited', 'Credited'),
    ])
    category = fields.Selection(CATEGORIES, index=True)
    issues = fields.Char()
    fix_done = fields.Boolean(copy=False)
    fix_error = fields.Char(copy=False)

    @api.depends('total', 'odoo_total')
    def _compute_total_diff(self):
        for line in self:
            line.total_diff = line.odoo_total - line.total
