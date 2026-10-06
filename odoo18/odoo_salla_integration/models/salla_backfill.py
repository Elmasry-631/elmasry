# -*- coding: utf-8 -*-
"""Salla order backfill: import every order of a date range in small chunks driven by a cron.

A manual import of a whole week through the wizard runs inside one HTTP request and
dies on the request time limit (2,000+ orders, 3 API calls each). This model stores the
order ids of the range once, then a 5-minute cron imports them 10 at a time, commits
after every chunk and resumes where it stopped.
"""
import json
import logging
import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

BACKFILL_CHUNK = 10          # order ids per import call (keeps ApiTransaction paging sane)
BACKFILL_TIME_BUDGET = 480   # seconds of work per cron run


class SallaOrderBackfill(models.Model):
    _name = 'salla.order.backfill'
    _description = 'Salla Order Backfill'
    _order = 'id desc'

    name = fields.Char(compute='_compute_name', store=True)
    channel_id = fields.Many2one(
        'multi.channel.sale', string='Channel', required=True,
        domain=[('channel', '=', 'salla')], ondelete='cascade',
    )
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('done', 'Done'),
    ], default='draft', required=True, copy=False)
    order_ids_json = fields.Text(default='[]', copy=False)
    failed_ids_json = fields.Text(default='[]', copy=False)
    total_count = fields.Integer(copy=False)
    done_count = fields.Integer(copy=False)
    remaining_count = fields.Integer(compute='_compute_counts')
    failed_count = fields.Integer(compute='_compute_counts')
    failed_ids_display = fields.Text(compute='_compute_counts')
    progress = fields.Float(compute='_compute_counts')
    last_run = fields.Datetime(copy=False)
    last_error = fields.Text(copy=False)

    @api.depends('channel_id', 'date_from', 'date_to')
    def _compute_name(self):
        for rec in self:
            rec.name = '%s %s -> %s' % (rec.channel_id.name or 'Salla', rec.date_from or '', rec.date_to or '')

    @api.depends('total_count', 'done_count', 'order_ids_json', 'failed_ids_json')
    def _compute_counts(self):
        for rec in self:
            failed = json.loads(rec.failed_ids_json or '[]')
            remaining = json.loads(rec.order_ids_json or '[]')
            rec.failed_count = len(failed)
            rec.failed_ids_display = ', '.join(failed)
            rec.remaining_count = len(remaining)
            rec.progress = (100.0 * rec.done_count / rec.total_count) if rec.total_count else 0.0

    # ------------------------------------------------------------------ actions
    def action_start(self):
        self.ensure_one()
        if self.state == 'running':
            raise UserError(_('This backfill is already running.'))
        if self.date_to < self.date_from:
            raise UserError(_('The end date must be after the start date.'))
        if self.channel_id.state != 'validate':
            raise UserError(_('The channel is not connected.'))
        ids = self._collect_order_ids()
        self.write({
            'order_ids_json': json.dumps(ids),
            'failed_ids_json': '[]',
            'total_count': len(ids),
            'done_count': 0,
            'last_error': False,
            'state': 'running' if ids else 'done',
        })
        return True

    def action_retry_failed(self):
        self.ensure_one()
        failed = json.loads(self.failed_ids_json or '[]')
        if not failed:
            return True
        remaining = json.loads(self.order_ids_json or '[]')
        self.write({
            'order_ids_json': json.dumps(remaining + failed),
            'failed_ids_json': '[]',
            'total_count': self.done_count + len(remaining) + len(failed),
            'state': 'running',
        })
        return True

    def action_reset(self):
        self.write({
            'state': 'draft', 'order_ids_json': '[]', 'failed_ids_json': '[]',
            'total_count': 0, 'done_count': 0, 'last_error': False,
        })
        return True

    def action_run_now(self):
        """Process one time budget immediately (same code path as the cron)."""
        self.ensure_one()
        if self.state != 'running':
            raise UserError(_('Start the backfill first.'))
        if not self._process(BACKFILL_TIME_BUDGET):
            raise UserError(_('Another Salla order import is running on this channel. Try again later.'))
        return True

    # ------------------------------------------------------------------ internals
    def _collect_order_ids(self):
        """List the ids of the orders created in the range (30 per API call)."""
        self.ensure_one()
        channel = self.channel_id
        channel.with_context(operation=True).getAccessToken()
        api = channel.get_sallaApi()
        ids, page = [], 1
        while True:
            res = api.salla_response(api.import_url + 'orders', params={
                'from_date': self.date_from.strftime('%Y-%m-%d'),
                'to_date': self.date_to.strftime('%Y-%m-%d'),
                'per_page': 30,
                'page': page,
                'sort_by': 'created_at-asc',
            })
            rows = (res or {}).get('data') or []
            if not rows:
                break
            ids.extend(str(r.get('id')) for r in rows if r.get('id'))
            links = ((res or {}).get('pagination') or {}).get('links') or {}
            if not links.get('next'):
                break
            page += 1
        seen, unique = set(), []
        for store_id in ids:
            if store_id not in seen:
                seen.add(store_id)
                unique.append(store_id)
        _logger.info('Salla backfill %s: %s order id(s) collected for %s..%s',
                     self.id, len(unique), self.date_from, self.date_to)
        return unique

    @api.model
    def cron_process(self):
        for backfill in self.search([('state', '=', 'running')]):
            try:
                backfill._process(BACKFILL_TIME_BUDGET)
            except Exception as e:
                _logger.exception('Salla backfill %s failed: %s', backfill.id, e)
                self.env.cr.rollback()
        return True

    def _process(self, time_budget):
        """Import chunks until the time budget is spent. Returns False when the channel is busy."""
        self.ensure_one()
        channel = self.channel_id
        if not channel._salla_try_acquire_order_import_lock():
            _logger.info('Salla backfill %s: channel %s busy, retry next run', self.id, channel.id)
            return False
        start = time.time()
        try:
            remaining = json.loads(self.order_ids_json or '[]')
            failed = json.loads(self.failed_ids_json or '[]')
            # a backfill is a repair run: its postings follow the hold of the Salla corrections
            ImportOp = self.env['import.operation'].with_context(salla_repair=True)
            while remaining and (time.time() - start) < time_budget:
                chunk, remaining = remaining[:BACKFILL_CHUNK], remaining[BACKFILL_CHUNK:]
                try:
                    ImportOp.create({'channel_id': channel.id}).import_with_filter(
                        object='sale.order', filter_type='id', object_id=','.join(chunk),
                        from_cron=True, force_evaluate_feed=True,
                    )
                except Exception as e:
                    _logger.exception('Salla backfill %s: chunk failed: %s', self.id, e)
                    self.env.cr.rollback()
                    self.write({'last_error': str(e)[:1000]})
                # An order counts as failed when no mapping exists after the import.
                for store_id in chunk:
                    if not channel.match_order_mappings(store_id):
                        failed.append(store_id)
                self.write({
                    'order_ids_json': json.dumps(remaining),
                    'failed_ids_json': json.dumps(failed),
                    'done_count': self.total_count - len(remaining),
                    'last_run': fields.Datetime.now(),
                })
                self.env.cr.commit()
            if not remaining:
                self.write({'state': 'done'})
                self.env.cr.commit()
            _logger.info('Salla backfill %s: %s/%s done, %s failed, %s remaining',
                         self.id, self.done_count, self.total_count, len(failed), len(remaining))
        finally:
            channel._salla_release_order_import_lock()
        return True
