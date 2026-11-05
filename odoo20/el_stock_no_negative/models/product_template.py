# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    allow_negative_stock = fields.Boolean(
        string='Allow Negative Stock',
        default=False,
        help='If checked, this product can have negative stock quantities. '
             'This overrides the global setting and category setting.'
    )

    def _get_allow_negative_stock(self):
        """Check if negative stock is allowed for this product"""
        self.ensure_one()
        # Check product level
        if self.allow_negative_stock:
            return True
        # Check category level
        if self.categ_id.allow_negative_stock:
            return True
        # Check global setting
        param = self.env['ir.config_parameter'].sudo().search([('key', '=', 'stock.allow_negative_stock')], limit=1)
        if param and param.value == 'True':
            return True
        return False


class ProductCategory(models.Model):
    _inherit = 'product.category'

    allow_negative_stock = fields.Boolean(
        string='Allow Negative Stock',
        default=False,
        help='If checked, all products in this category can have negative stock quantities. '
             'This overrides the global setting.'
    )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_allow_negative_stock(self):
        """Check if negative stock is allowed for this product variant"""
        self.ensure_one()
        # Check template level
        if self.product_tmpl_id.allow_negative_stock:
            return True
        # Check global setting
        param = self.env['ir.config_parameter'].sudo().search([('key', '=', 'stock.allow_negative_stock')], limit=1)
        if param and param.value == 'True':
            return True
        return False