# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError
import json
from math import ceil
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    tax_totals_amount = fields.Float(compute='_compute_tax_totals_amount')

    @api.depends('tax_totals')
    def _compute_tax_totals_amount(self):
        for record in self:
            if record.tax_totals:
                # Check if tax_totals is a binary field that needs decoding
                if isinstance(record.tax_totals, bytes):
                    tax_totals_data = json.loads(record.tax_totals.decode('utf-8'))
                elif isinstance(record.tax_totals, str):
                    # Handle case where it's a string that needs json loading
                    tax_totals_data = json.loads(record.tax_totals)
                elif isinstance(record.tax_totals, dict):
                    # Handle case where it's already a dictionary
                    tax_totals_data = record.tax_totals
                else:
                    # In case it's a different type, skip processing
                    continue

                record.tax_totals_amount = tax_totals_data.get('amount_total', 0.0)

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = amount_discount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_unit * line.product_uom_qty
                amount_tax += line.price_tax
                amount_discount += (line.product_uom_qty * line.price_unit * line.discount) / 100
                

            # Always round up amount_untaxed
            amount_untaxed_rounded = amount_untaxed

            order.update({
                'amount_untaxed': amount_untaxed_rounded,
                'amount_tax': amount_tax,
                'amount_discount': amount_discount,
                'amount_total': amount_untaxed_rounded,
            })


    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')], string='Discount type',
                                     readonly=True,
                                     states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                     default='percent')
    discount_rate = fields.Float('Discount Rate', digits=dp.get_precision('Account'),
                                 readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all',
                                 track_visibility='always')
    amount_total = fields.Monetary(string='Total before Discount', store=True, readonly=True, compute='_amount_all',
                                   track_visibility='always')
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_all',
                                      digits=dp.get_precision('Account'), track_visibility='always')

    @api.onchange('discount_type', 'discount_rate', 'order_line')
    def supply_rate(self):
        for order in self:
            _logger.info("### amount_untaxed: %s, Discount rate: %s, , Tax Totals: %s",order.amount_untaxed, order.amount_discount, order.tax_totals)
            if order.discount_type == 'percent':
                for line in order.order_line:
                    line.discount = order.discount_rate
            else:
                total = discount = 0.0
                for line in order.order_line:
                    total += (line.product_uom_qty * line.price_unit)
                if total > 0 and order.discount_rate != 0:
                    discount = (order.discount_rate / total) * 100
                else:
                    discount = 0
                for line in order.order_line:
                    line.discount = discount
                    new_sub_price = line.price_unit - (line.price_unit * (discount / 100))
                    line.total_discount = new_sub_price


    def _prepare_invoice(self, ):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate,
        })
        return invoice_vals

    def button_dummy(self):

        self.supply_rate()
        return True



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount = fields.Float(string='Discount (%)', digits=(16, 20), default=0.0)
    total_discount = fields.Float(string="Total Discount", default=0.0, store=True)