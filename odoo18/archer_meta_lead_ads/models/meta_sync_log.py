# -*- coding: utf-8 -*-

from datetime import timedelta

from odoo import api, fields, models, _


class MetaSyncLog(models.Model):
    _name = 'meta.sync.log'
    _description = 'Meta Sync Log'
    _order = 'create_date desc, id desc'

    name = fields.Char(
        string='Summary',
        compute='_compute_name',
        store=True,
    )
    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    level = fields.Selection(
        [('info', 'Info'), ('warning', 'Warning'), ('error', 'Error')],
        required=True,
        default='error',
        index=True,
    )
    category = fields.Char(required=True, index=True)
    message = fields.Text(required=True)
    credential_id = fields.Many2one('meta.app.credential', ondelete='cascade')
    page_id = fields.Many2one('meta.page', ondelete='cascade')
    form_id = fields.Many2one('meta.lead.form', ondelete='cascade')
    lead_id = fields.Many2one('crm.lead', ondelete='set null')

    @api.depends('level', 'category')
    def _compute_name(self):
        for rec in self:
            rec.name = "[%s] %s" % (rec.level.upper(), rec.category)

    @api.model
    def log(self, level, category, message, credential=None, page=None, form=None, lead=None, company=None):
        company = company or credential.company_id or page.company_id or form.company_id or self.env.company
        return self.create({
            'level': level,
            'category': category,
            'message': message,
            'credential_id': credential.id if credential else False,
            'page_id': page.id if page else False,
            'form_id': form.id if form else False,
            'lead_id': lead.id if lead else False,
            'company_id': company.id,
        })

    @api.model
    def _cron_cleanup_old_logs(self):
        cutoff = fields.Datetime.now() - timedelta(days=90)
        old_logs = self.search([('create_date', '<', cutoff)])
        old_logs.unlink()
        return True
