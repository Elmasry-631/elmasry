# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo import exceptions, _
from odoo.exceptions import  ValidationError

class SaleOrder(models.Model):
    _inherit = 'purchase.order'

    amount_tax_for_sale = fields.Float('Amount Tax')
    amount_tax_for_sale_percent = fields.Boolean('Amount Tax Percent %')


    @api.depends('order_line.price_total', 'amount_tax_for_sale', 'amount_tax_for_sale_percent')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = amount_total_after_new_tax_sale = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                amount_total_after_new_tax_sale = amount_untaxed + amount_tax
                if order.amount_tax_for_sale_percent:
                    amount_total_after_new_tax_sale += (amount_total_after_new_tax_sale * order.amount_tax_for_sale) / 100
                else:
                    amount_total_after_new_tax_sale += order.amount_tax_for_sale
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_total_after_new_tax_sale,
            })
