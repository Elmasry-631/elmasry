# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MetaLeadForm(models.Model):
    _name = 'meta.lead.form'
    _description = 'Meta Lead Form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    DEFAULT_FIELD_MAP = {
        'full_name': 'contact_name',
        'email': 'email_from',
        'phone_number': 'phone',
        'city': 'city',
        'street_address': 'street',
        'company_name': 'partner_name',
        'job_title': 'function',
        'country': 'country_id',
        'state': 'state_id',
    }

    name = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one(related='page_id.company_id', store=True, readonly=True)
    page_id = fields.Many2one('meta.page', required=True, ondelete='cascade', tracking=True)
    form_id = fields.Char(required=True, index=True)
    status = fields.Char(default='ACTIVE', tracking=True)
    locale = fields.Char()
    created_time = fields.Datetime()
    crm_team_id = fields.Many2one('crm.team', string='Sales Team', domain="[('company_id', '=', company_id)]", tracking=True)
    utm_source_id = fields.Many2one('utm.source', tracking=True)
    utm_medium_id = fields.Many2one('utm.medium', tracking=True)
    fetch_frequency_minutes = fields.Selection(
        [('15', 'Every 15 minutes'), ('30', 'Every 30 minutes'), ('60', 'Every 60 minutes')],
        string='Fetch Frequency',
        default='30',
        required=True,
        tracking=True,
    )
    mapping_ids = fields.One2many('meta.lead.field.mapping', 'form_id', string='Field Mapping')
    mapping_count = fields.Integer(compute='_compute_counts')
    lead_count = fields.Integer(compute='_compute_counts')
    last_fetch_date = fields.Datetime()
    questions_json = fields.Text()
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('meta_form_unique', 'unique(page_id, form_id)', 'Meta form ID must be unique per page.'),
    ]

    def _compute_counts(self):
        lead_model = self.env['crm.lead']
        for rec in self:
            rec.mapping_count = len(rec.mapping_ids)
            rec.lead_count = lead_model.search_count([('x_meta_form_id', '=', rec.id)])

    def action_view_leads(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Leads'),
            'res_model': 'crm.lead',
            'view_mode': 'list,form',
            'domain': [('x_meta_form_id', '=', self.id)],
        }

    def action_fetch_form_fields(self):
        self.ensure_one()
        self.page_id.action_fetch_forms()
        return self._notify(_("Form schema refreshed from Meta."))

    def _notify(self, message):
        return self.page_id.credential_id._display_notification(_("Meta Lead Ads"), message)

    def _is_fetch_due(self):
        self.ensure_one()
        if not self.last_fetch_date:
            return True
        interval = int(self.fetch_frequency_minutes or 30)
        next_run = fields.Datetime.to_datetime(self.last_fetch_date) + timedelta(minutes=interval)
        return fields.Datetime.now() >= next_run

    def _ensure_default_mappings(self, questions=None):
        questions = questions or []
        ir_field_model = self.env['ir.model.fields']
        for question in questions:
            key = question.get('key')
            target_name = self.DEFAULT_FIELD_MAP.get(key)
            if not key or not target_name:
                continue
            if self.mapping_ids.filtered(lambda m: m.meta_field_key == key):
                continue
            field_rec = ir_field_model.search([('model', '=', 'crm.lead'), ('name', '=', target_name)], limit=1)
            if not field_rec:
                continue
            lookup_field = 'name' if field_rec.ttype in ('many2one', 'many2many') else False
            self.env['meta.lead.field.mapping'].create({
                'form_id': self.id,
                'meta_field_key': key,
                'odoo_field_id': field_rec.id,
                'lookup_field': lookup_field,
                'is_default': True,
            })

    def _meta_field_dict(self, lead_payload):
        return {item.get('name'): item.get('values', []) for item in lead_payload.get('field_data', []) if item.get('name')}

    def _apply_transform(self, mapping, value):
        if value in (False, None):
            return value
        if mapping.transform == 'lowercase' and isinstance(value, str):
            return value.lower()
        if mapping.transform == 'strip' and isinstance(value, str):
            return value.strip()
        return value

    def _map_relational_value(self, mapping, raw_values):
        model = self.env[mapping.odoo_field_id.relation]
        lookup_field = mapping.lookup_field or 'name'
        values = [self._apply_transform(mapping, v) for v in raw_values if v not in (None, '')]
        if mapping.odoo_field_name == 'tag_ids' and mapping.odoo_field_id.relation == 'crm.tag':
            ids = []
            for value in values:
                parts = [part.strip() for part in value.split(',') if part.strip()]
                for part in parts:
                    tag = model.search([('name', '=', part)], limit=1)
                    if not tag:
                        tag = model.create({'name': part})
                    ids.append(tag.id)
            return [(6, 0, list(set(ids)))] if ids else False
        record_ids = []
        for value in values:
            parts = [part.strip() for part in value.split(',')] if mapping.odoo_field_ttype == 'many2many' else [value]
            for part in filter(None, parts):
                record = model.search([(lookup_field, '=', part)], limit=1)
                if not record:
                    self.env['meta.sync.log'].log(
                        'warning',
                        'lookup_failed',
                        _("Could not map '%(value)s' to %(relation)s using field %(field)s.") % {
                            'value': part,
                            'relation': mapping.odoo_field_id.relation,
                            'field': lookup_field,
                        },
                        credential=self.page_id.credential_id,
                        page=self.page_id,
                        form=self,
                    )
                    continue
                record_ids.append(record.id)
        if mapping.odoo_field_ttype == 'many2one':
            return record_ids[:1] and record_ids[0] or False
        return [(6, 0, list(set(record_ids)))] if record_ids else False

    def _build_lead_vals(self, lead_payload):
        self.ensure_one()
        field_data = self._meta_field_dict(lead_payload)
        vals = {
            'name': lead_payload.get('campaign_name') or self.name,
            'type': 'lead',
            'team_id': self.crm_team_id.id or False,
            'company_id': self.company_id.id,
            'x_meta_leadgen_id': lead_payload.get('id'),
            'x_meta_platform': lead_payload.get('platform') or self.page_id.platform,
            'x_meta_page_id': self.page_id.id,
            'x_meta_form_id': self.id,
            'x_meta_campaign_name': lead_payload.get('campaign_name'),
            'x_meta_ad_name': lead_payload.get('ad_name'),
            'x_meta_created_time': self.page_id.credential_id._meta_datetime_to_odoo(lead_payload.get('created_time')),
            'utm_source_id': self.utm_source_id.id or False,
            'utm_medium_id': self.utm_medium_id.id or False,
        }
        campaign_name = lead_payload.get('campaign_name')
        if campaign_name:
            campaign = self.env['utm.campaign'].search([('name', '=', campaign_name)], limit=1)
            if not campaign:
                campaign = self.env['utm.campaign'].create({'name': campaign_name})
            vals['campaign_id'] = campaign.id
        for mapping in self.mapping_ids.filtered('active'):
            raw_values = field_data.get(mapping.meta_field_key) or []
            raw_value = raw_values and raw_values[0] or False
            if mapping.odoo_field_ttype in ('many2one', 'many2many'):
                mapped_value = self._map_relational_value(mapping, raw_values)
            else:
                mapped_value = self._apply_transform(mapping, raw_value)
            if mapped_value not in (False, None, [], ''):
                vals[mapping.odoo_field_name] = mapped_value
        return vals

    def _import_meta_lead(self, lead_payload):
        self.ensure_one()
        lead_model = self.env['crm.lead'].sudo()
        leadgen_id = lead_payload.get('id')
        if not leadgen_id:
            return False
        existing = lead_model.search([('x_meta_leadgen_id', '=', leadgen_id)], limit=1)
        if existing:
            return False
        vals = self._build_lead_vals(lead_payload)
        lead = lead_model.create(vals)
        lead.message_post(body=_("Imported from Meta. Page: %(page)s, Form: %(form)s, Campaign: %(campaign)s") % {
            'page': self.page_id.name,
            'form': self.name,
            'campaign': lead_payload.get('campaign_name') or '-',
        })
        return lead

    def action_fetch_leads(self):
        imported = 0
        for form in self:
            imported += form._fetch_new_leads()
        return self._notify(_("Imported %(count)s new lead(s).") % {'count': imported})

    def _fetch_new_leads(self):
        self.ensure_one()
        if not self.page_id.page_access_token:
            raise UserError(_("Page access token is missing for %s.") % self.page_id.name)
        endpoint = '/%s/leads' % self.form_id
        params = {
            'fields': 'id,created_time,ad_id,ad_name,adset_id,adset_name,campaign_id,campaign_name,form_id,platform,field_data',
            'access_token': self.page_id.page_access_token,
        }
        leads = self.page_id.credential_id._meta_paginated_get(endpoint, params=params)
        imported = 0
        for lead_payload in leads:
            created = self._import_meta_lead(lead_payload)
            if created and created.x_meta_leadgen_id == lead_payload.get('id'):
                imported += 1
        self.write({'last_fetch_date': fields.Datetime.now()})
        self.page_id.credential_id.last_sync_date = fields.Datetime.now()
        self.message_post(body=_("Fetched leads from Meta. Imported %(count)s new lead(s).") % {'count': imported})
        return imported

    @api.model
    def _cron_fetch_all_leads(self):
        total = 0
        forms = self.search([('active', '=', True), ('page_id.is_active', '=', True), ('page_id.credential_id.state', '=', 'connected')])
        for form in forms:
            if not form._is_fetch_due():
                continue
            try:
                total += form._fetch_new_leads()
                self.env.cr.commit()
            except Exception as error:
                self.env['meta.sync.log'].log(
                    'error',
                    'fetch_leads',
                    str(error),
                    credential=form.page_id.credential_id,
                    page=form.page_id,
                    form=form,
                )
                self.env.cr.rollback()
        return total
