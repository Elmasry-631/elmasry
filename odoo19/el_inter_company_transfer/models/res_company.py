# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    inter_company_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Inter Company Warehouse',
        domain="[('company_id', '=', id)]",
        help='Default warehouse used for inter-company transfers.',
    )
