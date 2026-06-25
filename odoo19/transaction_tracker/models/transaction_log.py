# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

import pytz

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TransactionLog(models.Model):
    _name = 'transaction.log'
    _description = 'Transaction Log'
    _order = 'create_date desc, id desc'
    _rec_name = 'name'

    # ------------------------------------------------------------------
    # Fields
    # ------------------------------------------------------------------
    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        default=lambda self: _('New'),
        index=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        index=True,
        default=lambda self: self.env.user,
    )
    model_name = fields.Char(
        string='Model',
        required=True,
        index=True,
        help='Technical name of the model (e.g. sale.order)',
    )
    res_id = fields.Integer(
        string='Record ID',
        required=True,
        index=True,
        help='Database ID of the affected record',
    )
    record_display_name = fields.Char(
        string='Record',
        help='Display name of the affected record at the time of the operation',
    )
    operation = fields.Selection(
        [
            ('create', 'Create'),
            ('write', 'Write'),
            ('unlink', 'Delete'),
            ('read', 'Read'),
        ],
        string='Operation',
        required=True,
        index=True,
    )
    module_name = fields.Char(
        string='Module',
        index=True,
        help='Odoo addon that owns the model (e.g. sale)',
    )
    old_values = fields.Text(
        string='Old Values',
        help='JSON snapshot of field values before the operation (write/unlink only)',
    )
    new_values = fields.Text(
        string='New Values',
        help='JSON snapshot of field values after the operation (create/write only)',
    )
    changed_fields = fields.Char(
        string='Changed Fields',
        help='Comma-separated list of fields that changed during write',
    )
    ip_address = fields.Char(
        string='IP Address',
        help='IP address of the user who performed the operation',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    is_suspicious = fields.Boolean(
        string='Suspicious',
        default=False,
        help='Flagged as potentially suspicious (e.g. bulk delete)',
    )
    note = fields.Text(
        string='Notes',
    )

    # ------------------------------------------------------------------
    # Computed fields
    # ------------------------------------------------------------------
    record_ref = fields.Char(
        string='Record Reference',
        compute='_compute_record_ref',
        help='Model,RecordID for quick lookup',
    )

    @api.depends('model_name', 'res_id')
    def _compute_record_ref(self):
        for rec in self:
            rec.record_ref = '%s,%d' % (rec.model_name, rec.res_id) if rec.model_name and rec.res_id else ''

    # ------------------------------------------------------------------
    # CRUD overrides
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'transaction.log'
                ) or _('New')
        return super().create(vals_list)

    # Prevent update and delete of log records — they are immutable
    def write(self, vals):
        if self.env.context.get('skip_transaction_tracking'):
            return super().write(vals)
        raise UserError(_(
            'Transaction log records are immutable and cannot be modified.'
        ))

    def unlink(self):
        if self.env.context.get('skip_transaction_tracking'):
            return super().unlink()
        raise UserError(_(
            'Transaction log records are immutable and cannot be deleted.'
        ))

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def action_open_record(self):
        """Open the source record that was tracked."""
        self.ensure_one()
        if not self.model_name or not self.res_id:
            raise UserError(_('Cannot open the source record.'))
        # Check if the record still exists
        try:
            Model = self.env[self.model_name]
            record = Model.browse(self.res_id).exists()
            if not record:
                raise UserError(_(
                    'The source record (%s,%d) has been deleted.'
                ) % (self.model_name, self.res_id))
        except KeyError:
            raise UserError(_('Model %s no longer exists.') % self.model_name)

        return {
            'type': 'ir.actions.act_window',
            'res_model': self.model_name,
            'res_id': self.res_id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_export_pdf(self):
        """Export selected logs as PDF report."""
        self.ensure_one()
        return self.env.ref(
            'transaction_tracker.action_report_transaction_log'
        ).report_action(self)

    def action_export_excel(self):
        """Export selected logs as Excel report."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/transaction_tracker/export_excel?log_ids=%s' % ','.join(
                str(i) for i in self.ids
            ),
            'target': 'self',
        }

    # ------------------------------------------------------------------
    # Utility methods
    # ------------------------------------------------------------------
    @api.model
    def _log_operation(self, operation, model_name, res_id, record_display_name='',
                       old_values=None, new_values=None, changed_fields='',
                       module_name='', ip_address='', is_suspicious=False):
        """Create a transaction log entry. Called from the base hook."""
        # Skip if tracking is disabled for this model
        config = self.env['transaction.tracker.config']._get_config(model_name)
        if not config:
            return False

        # Check operation-level tracking
        op_field = 'track_%s' % operation
        if config:
            try:
                if not getattr(config, op_field, True):
                    return False
            except Exception:
                return False

        self.with_context(skip_transaction_tracking=True).sudo().create({
            'user_id': self.env.uid,
            'model_name': model_name,
            'res_id': res_id,
            'record_display_name': record_display_name,
            'operation': operation,
            'module_name': module_name,
            'old_values': json.dumps(old_values, default=str) if old_values else False,
            'new_values': json.dumps(new_values, default=str) if new_values else False,
            'changed_fields': changed_fields,
            'ip_address': ip_address,
            'is_suspicious': is_suspicious,
        })
        return True

    @api.model
    def _get_ip_address(self):
        """Extract client IP from the HTTP request if available."""
        try:
            from odoo import http
            http_request = http.request
            if http_request and hasattr(http_request, 'httprequest'):
                forwarded = http_request.httprequest.headers.get(
                    'X-Forwarded-For', ''
                )
                if forwarded:
                    return forwarded.split(',')[0].strip()
                return http_request.httprequest.remote_addr or ''
        except Exception:
            pass
        return ''

    @api.model
    def get_dashboard_data(self):
        """Return aggregated data for the dashboard.

        All date-range filters use the current user's timezone so that
        "today" / "this week" / "this month" are correct for the user's
        local time, not UTC.
        """
        user_tz = self.env.user.tz or 'UTC'
        local_tz = pytz.timezone(user_tz)

        today_local = fields.Date.context_today(self)
        today_start_local = local_tz.localize(
            datetime.combine(today_local, datetime.min.time()),
        )
        today_start_utc = today_start_local.astimezone(pytz.UTC).replace(tzinfo=None)

        week_ago_utc = today_start_utc - timedelta(days=7)
        month_ago_utc = today_start_utc - timedelta(days=30)

        # Total logs
        total = self.search_count([])

        # Today's logs (user's local day)
        today_logs = self.search_count([
            ('create_date', '>=', today_start_utc),
        ])

        # Last 7 days
        week_logs = self.search_count([
            ('create_date', '>=', week_ago_utc),
        ])

        # Last 30 days
        month_logs = self.search_count([
            ('create_date', '>=', month_ago_utc),
        ])

        # By operation (last 30 days)
        by_operation = self._read_group(
            [('create_date', '>=', month_ago_utc)],
            ['operation'],
            ['__count'],
        )

        # By user - top 10 (last 30 days)
        by_user = self._read_group(
            [('create_date', '>=', month_ago_utc)],
            ['user_id'],
            ['__count'],
            limit=10,
            orderby='__count desc',
        )

        # By model - top 10 (last 30 days)
        by_model = self._read_group(
            [('create_date', '>=', month_ago_utc)],
            ['model_name'],
            ['__count'],
            limit=10,
            orderby='__count desc',
        )

        # Suspicious count (last 30 days)
        suspicious_count = self.search_count([
            ('is_suspicious', '=', True),
            ('create_date', '>=', month_ago_utc),
        ])

        return {
            'total': total,
            'today': today_logs,
            'week': week_logs,
            'month': month_logs,
            'by_operation': [
                {'operation': op, 'count': count} for op, count in by_operation
            ] if by_operation else [],
            'by_user': [
                {'user_id': user.id, 'user_name': user.display_name, 'count': count}
                for user, count in by_user
            ] if by_user else [],
            'by_model': [
                {'model_name': model or 'Unknown', 'count': count}
                for model, count in by_model
            ] if by_model else [],
            'suspicious_count': suspicious_count,
        }
