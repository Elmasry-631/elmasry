# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError


class MetaPage(models.Model):
    _name = 'meta.page'
    _description = 'Meta Page'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one(related='credential_id.company_id', store=True, readonly=True)
    credential_id = fields.Many2one('meta.app.credential', required=True, ondelete='cascade', tracking=True)
    page_id = fields.Char(required=True, index=True)
    page_access_token = fields.Text()
    category = fields.Char(tracking=True)
    platform = fields.Selection(
        [('facebook', 'Facebook'), ('instagram', 'Instagram'), ('both', 'Both')],
        default='facebook',
        required=True,
        tracking=True,
    )
    instagram_account_id = fields.Char(string='Instagram Business Account ID')
    fan_count = fields.Integer()
    is_active = fields.Boolean(default=True, tracking=True)
    form_ids = fields.One2many('meta.lead.form', 'page_id', string='Forms')
    form_count = fields.Integer(compute='_compute_counts')
    lead_count = fields.Integer(compute='_compute_counts')

    _sql_constraints = [
        ('meta_page_unique', 'unique(credential_id, page_id)', 'Meta page ID must be unique per credential.'),
    ]

    def _compute_counts(self):
        lead_model = self.env['crm.lead']
        for rec in self:
            rec.form_count = len(rec.form_ids)
            rec.lead_count = lead_model.search_count([('x_meta_page_id', '=', rec.id)])

    def action_view_forms(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Forms'),
            'res_model': 'meta.lead.form',
            'view_mode': 'list,form',
            'domain': [('page_id', '=', self.id)],
            'context': {'default_page_id': self.id},
        }

    def action_view_leads(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Leads'),
            'res_model': 'crm.lead',
            'view_mode': 'list,form',
            'domain': [('x_meta_page_id', '=', self.id)],
        }

    def action_fetch_forms(self):
        self.ensure_one()
        if not self.page_access_token:
            raise UserError(_("Page access token is missing. Fetch pages again from the credential."))
        endpoint = '/%s/leadgen_forms' % self.page_id
        params = {
            'fields': 'id,name,status,locale,created_time,questions',
            'access_token': self.page_access_token,
        }
        response = self.credential_id._meta_paginated_get(endpoint, params=params)
        form_model = self.env['meta.lead.form']
        created = 0
        updated = 0
        for form_data in response:
            if form_data.get('status') not in ('ACTIVE', 'ARCHIVED'):
                continue
            values = {
                'name': form_data.get('name') or form_data.get('id'),
                'form_id': form_data.get('id'),
                'page_id': self.id,
                'status': form_data.get('status', 'ACTIVE'),
                'locale': form_data.get('locale'),
                'created_time': self.credential_id._meta_datetime_to_odoo(form_data.get('created_time')),
                'questions_json': self.credential_id._json_dump(form_data.get('questions') or []),
                'active': True,
            }
            form = form_model.search([('page_id', '=', self.id), ('form_id', '=', form_data.get('id'))], limit=1)
            if form:
                form.write(values)
                updated += 1
            else:
                form = form_model.create(values)
                created += 1
            form._ensure_default_mappings(form_data.get('questions') or [])
        self.message_post(body=_("Fetched forms from Meta. Created: %(created)s, Updated: %(updated)s.") % {
            'created': created,
            'updated': updated,
        })
        return self.credential_id._display_notification(
            _("Forms fetched"),
            _("Created %(created)s form(s), updated %(updated)s form(s).") % {
                'created': created,
                'updated': updated,
            },
        )
