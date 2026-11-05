# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_negative_stock = fields.Boolean(
        string='Allow Negative Stock Globally',
        config_parameter='stock.allow_negative_stock',
        help='If checked, negative stock will be allowed for all products, locations, and categories '
             'unless explicitly overridden at the product or category level.'
    )

    module_stock_dropshipping = fields.Boolean(
        string='Drop-Shipping',
        help='Allows you to deliver products directly from your vendor to your customer.'
    )