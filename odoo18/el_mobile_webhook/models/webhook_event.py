import hashlib
import hmac
import json
import logging
import uuid
from datetime import timedelta
from urllib.parse import urlparse

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MobileWebhookEvent(models.Model):
    _name = 'mobile.webhook.event'
    _description = 'Mobile Webhook Event'
    _order = 'create_date desc, id desc'

    event_uuid = fields.Char(required=True, readonly=True, copy=False, index=True, default=lambda self: str(uuid.uuid4()))
    event_type = fields.Char(required=True, readonly=True, index=True)
    res_model = fields.Char(required=True, readonly=True, index=True)
    res_id = fields.Integer(required=True, readonly=True, index=True)
    record_name = fields.Char(required=True, readonly=True)
    company_id = fields.Many2one('res.company', required=True, readonly=True, index=True, default=lambda self: self.env.company)
    previous_status = fields.Char(readonly=True)
    status = fields.Char(required=True, readonly=True)
    payload_json = fields.Text(required=True, readonly=True)
    state = fields.Selection([('pending', 'Pending'), ('retrying', 'Retrying'), ('sent', 'Sent'), ('failed', 'Failed'), ('cancelled', 'Cancelled')], required=True, default='pending', index=True, copy=False)
    attempts = fields.Integer(default=0, readonly=True, copy=False)
    next_attempt_at = fields.Datetime(default=fields.Datetime.now, readonly=True, copy=False, index=True)
    sent_at = fields.Datetime(readonly=True, copy=False)
    last_error = fields.Char(readonly=True, copy=False)

    _sql_constraints = [('mobile_webhook_event_uuid_uniq', 'unique(event_uuid)', 'Webhook event ID must be unique.')]

    @api.constrains('event_uuid')
    def _check_event_uuid(self):
        for event in self:
            try:
                uuid.UUID(event.event_uuid)
            except (TypeError, ValueError) as exc:
                raise ValidationError(_('Event ID must be a UUID.')) from exc

    @api.model
    def _queue_status_change(self, record, event_type, previous_status, status):
        if previous_status == status:
            return
        payload = {'event_id': str(uuid.uuid4()), 'event': event_type, 'timestamp': fields.Datetime.to_string(fields.Datetime.now()), 'company_id': record.company_id.id, 'model': record._name, 'record_id': record.id, 'record_name': record.display_name, 'previous_status': previous_status, 'status': status}
        self.create({'event_uuid': payload['event_id'], 'event_type': event_type, 'res_model': record._name, 'res_id': record.id, 'record_name': record.display_name, 'company_id': record.company_id.id, 'previous_status': previous_status, 'status': status, 'payload_json': json.dumps(payload, separators=(',', ':'), sort_keys=True)})

    def _settings(self):
        params = self.env['ir.config_parameter'].sudo()
        return (params.get_param('el_mobile_webhook.endpoint', '').strip(), params.get_param('el_mobile_webhook.secret', ''), int(params.get_param('el_mobile_webhook.timeout', '10')), int(params.get_param('el_mobile_webhook.retry_limit', '5')))

    @staticmethod
    def _validate_endpoint(endpoint):
        parsed = urlparse(endpoint)
        if parsed.scheme != 'https' or not parsed.netloc:
            raise ValidationError(_('Webhook endpoint must be a valid HTTPS URL.'))

    def _deliver(self):
        self.ensure_one()
        endpoint, secret, timeout, retry_limit = self._settings()
        if not endpoint or not secret:
            raise UserError(_('Configure the mobile webhook endpoint and secret first.'))
        self._validate_endpoint(endpoint)
        body = self.payload_json.encode()
        signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        try:
            response = requests.post(endpoint, data=body, headers={'Content-Type': 'application/json', 'X-Odoo-Webhook-Id': self.event_uuid, 'X-Odoo-Webhook-Event': self.event_type, 'X-Odoo-Webhook-Signature': f'sha256={signature}'}, timeout=(3, timeout))
            response.raise_for_status()
        except requests.RequestException as exc:
            self._schedule_retry(str(exc), retry_limit)
            return False
        self.write({'state': 'sent', 'sent_at': fields.Datetime.now(), 'last_error': False})
        return True

    def _schedule_retry(self, error, retry_limit):
        self.ensure_one()
        attempts = self.attempts + 1
        values = {'attempts': attempts, 'last_error': error[:512]}
        if attempts >= retry_limit:
            values['state'] = 'failed'
        else:
            values.update({'state': 'retrying', 'next_attempt_at': fields.Datetime.now() + timedelta(seconds=min(60 * 2 ** (attempts - 1), 3600))})
        self.write(values)
        _logger.warning('Mobile webhook delivery failed for event %s (attempt %s).', self.event_uuid, attempts)

    @api.model
    def _cron_process_queue(self):
        events = self.search([('state', 'in', ('pending', 'retrying')), ('next_attempt_at', '<=', fields.Datetime.now())], limit=50)
        for event in events:
            try:
                with self.env.cr.savepoint():
                    event._deliver()
            except (UserError, ValidationError) as exc:
                event._schedule_retry(str(exc), 1)
            except Exception:
                _logger.exception('Unexpected mobile webhook error for event %s.', event.event_uuid)
                event._schedule_retry('Unexpected delivery error.', 1)

    def action_retry(self):
        self.write({'state': 'pending', 'attempts': 0, 'next_attempt_at': fields.Datetime.now(), 'last_error': False})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_send_now(self):
        self._deliver()
