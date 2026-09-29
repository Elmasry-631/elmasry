# -*- coding: utf-8 -*-

from odoo import Command, api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ReturnInterCompanyTransfer(models.Model):
    _name = 'return.inter.company.transfer'
    _description = 'Return Inter Company Transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Reference',
        default=lambda self: _('New'),
        readonly=True,
        required=True,
        copy=False,
    )
    source_ict_id = fields.Many2one(
        'stock.inter.company.transfer',
        string='Original Transfer',
        readonly=True,
        required=True,
    )
    source_company_id = fields.Many2one('res.company', string='Source Company', required=True)
    dest_company_id = fields.Many2one('res.company', string='Destination Company', required=True)
    from_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='From Warehouse',
        required=True,
        domain="[('company_id', '=', source_company_id)]",
    )
    to_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='To Warehouse',
        required=True,
        domain="[('company_id', '=', dest_company_id)]",
    )
    state = fields.Selection(
        [('draft', 'Draft'), ('process', 'Processed'), ('cancel', 'Cancelled')],
        default='draft',
        readonly=True,
        tracking=True,
    )
    sale_order_id = fields.Many2one('sale.order', string='Sales Order', readonly=True)
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', readonly=True)
    delivery_picking_id = fields.Many2one('stock.picking', string='Delivery Order', readonly=True)
    receipt_picking_id = fields.Many2one('stock.picking', string='Incoming Shipment', readonly=True)
    customer_invoice_id = fields.Many2one('account.move', string='Customer Credit Note', readonly=True)
    vendor_bill_id = fields.Many2one('account.move', string='Vendor Refund', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    date = fields.Date(default=fields.Date.context_today, required=True)
    return_line_ids = fields.One2many(
        'return.inter.company.transfer.line',
        'transfer_id',
        string='Return Lines',
        copy=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Assign a sequence to return transactions."""
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('return.inter.company.transfer') or _('New')
        return super().create(vals_list)

    @api.constrains('source_company_id', 'dest_company_id', 'from_warehouse_id', 'to_warehouse_id')
    def _check_transfer_companies(self):
        """Validate company and warehouse consistency."""
        for transfer in self:
            if transfer.source_company_id == transfer.dest_company_id:
                raise ValidationError(_('Source and destination companies must be different.'))
            if transfer.from_warehouse_id.company_id != transfer.source_company_id:
                raise ValidationError(_('The source warehouse must belong to the source company.'))
            if transfer.to_warehouse_id.company_id != transfer.dest_company_id:
                raise ValidationError(_('The destination warehouse must belong to the destination company.'))

    def action_process(self):
        """Process the return by creating reversed commercial documents and refund moves."""
        for transfer in self:
            if transfer.state != 'draft':
                continue
            if not transfer.return_line_ids:
                raise UserError(_('Add at least one return line before processing.'))
            transfer._create_reversed_orders()
            transfer._create_refund_moves()
            transfer.write({'state': 'process'})
        return True

    def action_cancel(self):
        """Cancel the return transaction."""
        self.write({'state': 'cancel'})
        return True

    def _create_reversed_orders(self):
        """Create a sale order and purchase order for visibility of the reversed flow."""
        self.ensure_one()
        allowed_companies = (self.source_company_id | self.dest_company_id).ids
        sale_order = self.env['sale.order'].with_context(
            allowed_company_ids=allowed_companies,
            skip_inter_company_transfer=True,
        ).with_company(self.source_company_id).sudo().create({
            'partner_id': self.dest_company_id.partner_id.id,
            'company_id': self.source_company_id.id,
            'warehouse_id': self.from_warehouse_id.id,
            'origin': self.name,
            'client_order_ref': self.name,
            'order_line': [
                Command.create({
                    'product_id': line.product_id.id,
                    'name': line.product_id.get_product_multiline_description_sale() or line.product_id.display_name,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.uom_id.id,
                    'price_unit': line.price_unit,
                })
                for line in self.return_line_ids
            ],
        })
        purchase_order = self.env['purchase.order'].with_context(
            allowed_company_ids=allowed_companies,
            skip_inter_company_transfer=True,
        ).with_company(self.dest_company_id).sudo().create({
            'partner_id': self.source_company_id.partner_id.id,
            'company_id': self.dest_company_id.id,
            'picking_type_id': self.to_warehouse_id.in_type_id.id,
            'origin': self.name,
            'order_line': [
                Command.create({
                    'product_id': line.product_id.id,
                    'name': line.product_id.display_name,
                    'product_qty': line.quantity,
                    'product_uom_id': line.uom_id.id,
                    'price_unit': line.price_unit,
                    'date_planned': fields.Datetime.now(),
                })
                for line in self.return_line_ids
            ],
        })
        self.write({
            'sale_order_id': sale_order.id,
            'purchase_order_id': purchase_order.id,
        })

    def _create_refund_moves(self):
        """Create the original seller credit note and original buyer vendor refund."""
        self.ensure_one()
        original = self.source_ict_id
        allowed_companies = (original.source_company_id | original.dest_company_id).ids
        invoice_lines = [
            Command.create({
                'product_id': line.product_id.id,
                'name': line.product_id.display_name,
                'quantity': line.quantity,
                'product_uom_id': line.uom_id.id,
                'price_unit': line.price_unit,
            })
            for line in self.return_line_ids
        ]
        credit_note = self.env['account.move'].with_context(
            default_move_type='out_refund',
            allowed_company_ids=allowed_companies,
        ).with_company(original.source_company_id).sudo().create({
            'move_type': 'out_refund',
            'partner_id': original.dest_company_id.partner_id.id,
            'company_id': original.source_company_id.id,
            'invoice_origin': self.name,
            'invoice_line_ids': invoice_lines,
        })
        vendor_refund = self.env['account.move'].with_context(
            default_move_type='in_refund',
            allowed_company_ids=allowed_companies,
        ).with_company(original.dest_company_id).sudo().create({
            'move_type': 'in_refund',
            'partner_id': original.source_company_id.partner_id.id,
            'company_id': original.dest_company_id.id,
            'invoice_origin': self.name,
            'invoice_line_ids': invoice_lines,
        })
        self.write({
            'customer_invoice_id': credit_note.id,
            'vendor_bill_id': vendor_refund.id,
        })

    def _action_open_record(self, record):
        """Return a form action for a linked singleton record."""
        self.ensure_one()
        record.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': record._name,
            'view_mode': 'form',
            'res_id': record.id,
        }

    def action_view_sale_order(self):
        return self._action_open_record(self.sale_order_id)

    def action_view_purchase_order(self):
        return self._action_open_record(self.purchase_order_id)

    def action_view_customer_invoice(self):
        return self._action_open_record(self.customer_invoice_id)

    def action_view_vendor_bill(self):
        return self._action_open_record(self.vendor_bill_id)


class ReturnInterCompanyTransferLine(models.Model):
    _name = 'return.inter.company.transfer.line'
    _description = 'Return Inter Company Transfer Line'
    _order = 'id'

    transfer_id = fields.Many2one(
        'return.inter.company.transfer',
        string='Return Transfer',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    price_unit = fields.Float(string='Unit Price', required=True)
    company_id = fields.Many2one('res.company', related='transfer_id.company_id', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Default UoM and price from product."""
        if self.product_id:
            self.uom_id = self.product_id.uom_id
            self.price_unit = self.product_id.lst_price
