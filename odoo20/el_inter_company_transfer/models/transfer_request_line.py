# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class InterCompanyTransferRequestLine(models.Model):
    _name = 'inter.company.transfer.request.line'
    _description = 'Inter Company Transfer Request Line'
    _order = 'request_id, sequence, id'

    request_id = fields.Many2one(
        'inter.company.transfer.request',
        string='Transfer Request',
        required=True,
        ondelete='cascade',
        index=True,
    )

    sequence = fields.Integer(string='Sequence', default=10)

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        domain="[('type', '=', 'consu')]",
        check_company=False,
    )

    product_uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        required=True,
    )

    product_qty = fields.Float(
        string='Quantity',
        required=True,
        default=1.0,
        digits='Product Unit of Measure',
    )

    # Available quantity in the source warehouse (for reference)
    available_qty = fields.Float(
        string='Available Qty',
        compute='_compute_available_qty',
        digits='Product Unit of Measure',
        help="Quantity available in the source warehouse.",
    )

    company_id = fields.Many2one(
        related='request_id.company_id',
        string='Company',
        store=True,
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id

    @api.depends('product_id', 'request_id.dest_warehouse_id')
    def _compute_available_qty(self):
        for line in self:
            # the source warehouse may belong to another company: read it as superuser
            request = line.request_id.sudo()
            warehouse = request.dest_warehouse_id.sudo()
            if line.product_id and warehouse and warehouse.lot_stock_id:
                quants = self.env['stock.quant'].sudo().with_company(
                    request.dest_company_id
                )._gather(line.product_id, warehouse.lot_stock_id)
                line.available_qty = sum(quants.mapped('available_quantity'))
            else:
                line.available_qty = 0.0

    @api.constrains('product_qty')
    def _check_quantity(self):
        for line in self:
            if line.product_qty <= 0:
                raise ValidationError(_("Quantity must be greater than zero."))
