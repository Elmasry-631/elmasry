# -*- coding: utf-8 -*-

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    x_meta_leadgen_id = fields.Char(index=True, copy=False)
    x_meta_platform = fields.Selection(
        [('facebook', 'Facebook'), ('instagram', 'Instagram'), ('both', 'Both')],
        copy=False,
    )
    x_meta_page_id = fields.Many2one('meta.page', string='Meta Page', copy=False, ondelete='set null')
    x_meta_form_id = fields.Many2one('meta.lead.form', string='Meta Form', copy=False, ondelete='set null')
    x_meta_campaign_name = fields.Char(copy=False)
    x_meta_ad_name = fields.Char(copy=False)
    x_meta_created_time = fields.Datetime(copy=False)

    _sql_constraints = [
        (
            'meta_leadgen_id_unique',
            'unique(x_meta_leadgen_id)',
            'Meta lead identifier must be unique.',
        ),
    ]
