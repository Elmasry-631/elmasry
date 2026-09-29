# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sales_commission_type = fields.Many2one(
        'sales.commission.type',
        string='Sales Commission Type',
        tracking=True,
    )
