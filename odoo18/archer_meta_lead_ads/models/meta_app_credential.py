# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
from datetime import timedelta

import requests

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class MetaAppCredential(models.Model):
    _name = 'meta.app.credential'
    _description = 'Meta App Credential'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    GRAPH_API_BASE = 'https://graph.facebook.com/v19.0'
    OAUTH_DIALOG = 'https://www.facebook.com/v19.0/dialog/oauth'
    OAUTH_SCOPE = ','.join([
        'pages_show_list',
        'pages_read_engagement',
        'pages_manage_metadata',
        'leads_retrieval',
        'ads_management',
        'business_management',
    ])

    name = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.company,
        tracking=True,
        index=True,
    )
    app_id = fields.Char(required=True, tracking=True)
    app_secret = fields.Char(required=True)
    user_access_token = fields.Text()
    token_expiry_date = fields.Datetime(tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('connected', 'Connected'), ('expired', 'Expired'), ('error', 'Error')],
        default='draft',
        required=True,
        tracking=True,
    )
    redirect_uri = fields.Char(compute='_compute_redirect_uri')
    page_ids = fields.One2many('meta.page', 'credential_id', string='Pages')
    page_count = fields.Integer(compute='_compute_counts')
    sync_issue_count = fields.Integer(compute='_compute_counts')
    last_sync_date = fields.Datetime()
    notes = fields.Html(tracking=True)
    active = fields.Boolean(default=True, tracking=True)

    _sql_constraints = [
        ('meta_credential_unique', 'unique(company_id, app_id)', 'App ID must be unique per company.'),
    ]

    def _compute_redirect_uri(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url', '')
        for rec in self:
            rec.redirect_uri = '%s/meta_lead_ads/oauth/callback' % base_url.rstrip('/')

    def _compute_counts(self):
        log_model = self.env['meta.sync.log']
        for rec in self:
            rec.page_count = len(rec.page_ids)
            rec.sync_issue_count = log_model.search_count([
                ('credential_id', '=', rec.id),
                ('level', 'in', ('warning', 'error')),
            ])

    def _display_notification(self, title, message, notif_type='success'):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'type': notif_type,
                'sticky': False,
            },
        }

    def _json_dump(self, payload):
        return json.dumps(payload, indent=2, ensure_ascii=False)

    def _meta_datetime_to_odoo(self, value):
        if not value:
            return False
        normalized = value.replace('Z', '+00:00')
        return fields.Datetime.to_string(fields.Datetime.from_string(normalized))

    def _get_state_secret(self):
        return self.env['ir.config_parameter'].sudo().get_param('database.secret') or self.env.cr.dbname

    def _build_oauth_state(self):
        self.ensure_one()
        payload = {
            'credential_id': self.id,
            'ts': int(fields.Datetime.now().timestamp()),
        }
        raw = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()
        signature = hmac.new(self._get_state_secret().encode(), raw, hashlib.sha256).hexdigest()
        token = {
            'payload': base64.urlsafe_b64encode(raw).decode(),
            'sig': signature,
        }
        return base64.urlsafe_b64encode(json.dumps(token, separators=(',', ':')).encode()).decode()

    @api.model
    def _validate_oauth_state(self, token):
        if not token:
            return False
        try:
            token_json = base64.urlsafe_b64decode(token.encode()).decode()
            data = json.loads(token_json)
            payload_raw = base64.urlsafe_b64decode(data['payload'].encode())
            expected = hmac.new(self._get_state_secret().encode(), payload_raw, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(expected, data['sig']):
                return False
            payload = json.loads(payload_raw.decode())
            now_ts = int(fields.Datetime.now().timestamp())
            if now_ts - int(payload['ts']) > 600:
                return False
            return int(payload['credential_id'])
        except Exception:
            return False

    def _meta_get(self, endpoint, params=None):
        url = endpoint if endpoint.startswith('http') else '%s%s' % (self.GRAPH_API_BASE, endpoint)
        response = requests.get(url, params=params or {}, timeout=30)
        if response.status_code >= 400:
            try:
                payload = response.json()
                message = payload.get('error', {}).get('message') or response.text
            except Exception:
                message = response.text
            raise UserError(_("Meta request failed: %s") % message)
        return response.json()

    def _meta_paginated_get(self, endpoint, params=None):
        items = []
        next_url = endpoint if endpoint.startswith('http') else '%s%s' % (self.GRAPH_API_BASE, endpoint)
        next_params = params or {}
        while next_url:
            response = self._meta_get(next_url, params=next_params)
            items.extend(response.get('data', []))
            next_url = response.get('paging', {}).get('next')
            next_params = None
        return items

    def action_generate_token(self):
        self.ensure_one()
        state = self._build_oauth_state()
        url = (
            '%s?client_id=%s&redirect_uri=%s&state=%s&scope=%s&response_type=code'
            % (
                self.OAUTH_DIALOG,
                self.app_id,
                self.redirect_uri,
                state,
                self.OAUTH_SCOPE,
            )
        )
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }

    def action_exchange_oauth_code(self, code):
        self.ensure_one()
        short_lived = self._meta_get('/oauth/access_token', params={
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'redirect_uri': self.redirect_uri,
            'code': code,
        })
        long_lived = self._meta_get('/oauth/access_token', params={
            'grant_type': 'fb_exchange_token',
            'client_id': self.app_id,
            'client_secret': self.app_secret,
            'fb_exchange_token': short_lived.get('access_token'),
        })
        expiry = fields.Datetime.now() + timedelta(seconds=int(long_lived.get('expires_in', 0)))
        self.write({
            'user_access_token': long_lived.get('access_token'),
            'token_expiry_date': expiry,
            'state': 'connected',
        })
        self.message_post(body=_("Access token regenerated. Expires on %s.") % expiry)
        return True

    def action_test_connection(self):
        self.ensure_one()
        if not self.user_access_token:
            raise UserError(_("User access token is missing. Click Generate Token first."))
        payload = self._meta_get('/me', params={'access_token': self.user_access_token})
        self.write({'state': 'connected'})
        self.message_post(body=_("Connection test passed for Meta user %(name)s (%(id)s).") % {
            'name': payload.get('name'),
            'id': payload.get('id'),
        })
        return self._display_notification(_("Connection passed"), _("Token is valid and Meta API responded successfully."))

    def action_fetch_pages(self):
        self.ensure_one()
        if not self.user_access_token:
            raise UserError(_("User access token is missing. Click Generate Token first."))
        records = self._meta_paginated_get('/me/accounts', params={
            'fields': 'id,name,category,access_token,instagram_business_account,fan_count',
            'access_token': self.user_access_token,
        })
        created = 0
        updated = 0
        page_model = self.env['meta.page']
        for data in records:
            platform = 'facebook'
            instagram_account = data.get('instagram_business_account', {})
            if instagram_account and instagram_account.get('id'):
                platform = 'both'
            values = {
                'name': data.get('name') or data.get('id'),
                'credential_id': self.id,
                'page_id': data.get('id'),
                'page_access_token': data.get('access_token'),
                'category': data.get('category'),
                'platform': platform,
                'instagram_account_id': instagram_account.get('id'),
                'fan_count': data.get('fan_count') or 0,
                'is_active': True,
            }
            page = page_model.search([('credential_id', '=', self.id), ('page_id', '=', data.get('id'))], limit=1)
            if page:
                page.write(values)
                updated += 1
            else:
                page_model.create(values)
                created += 1
        self.write({'last_sync_date': fields.Datetime.now(), 'state': 'connected'})
        self.message_post(body=_("Fetched %(created)s new page(s) and updated %(updated)s page(s).") % {
            'created': created,
            'updated': updated,
        })
        return self._display_notification(
            _("Pages fetched"),
            _("Created %(created)s page(s), updated %(updated)s page(s).") % {
                'created': created,
                'updated': updated,
            },
        )

    def action_view_pages(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Pages'),
            'res_model': 'meta.page',
            'view_mode': 'list,form',
            'domain': [('credential_id', '=', self.id)],
            'context': {'default_credential_id': self.id},
        }

    def action_view_sync_issues(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sync Issues'),
            'res_model': 'meta.sync.log',
            'view_mode': 'list,form',
            'domain': [('credential_id', '=', self.id)],
        }

    @api.model
    def _cron_check_token_expiry(self):
        todo = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
        for credential in self.search([('state', '=', 'connected'), ('token_expiry_date', '!=', False)]):
            days = (fields.Datetime.to_datetime(credential.token_expiry_date) - fields.Datetime.now()).days
            if days <= 0:
                credential.state = 'expired'
                credential.message_post(body=_("Meta token has expired."))
            if days <= 7 and todo:
                credential.activity_schedule(
                    todo.id,
                    summary=_("Meta token expiring soon"),
                    note=_("The Meta token expires in %(days)s day(s). Generate a fresh token.") % {
                        'days': max(days, 0),
                    },
                    user_id=credential.create_uid.id or self.env.uid,
                )
        return True
