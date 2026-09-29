# -*- coding: utf-8 -*-

from odoo import Command, api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class StockInterCompanyTransfer(models.Model):
    _name = 'stock.inter.company.transfer'
    _description = 'Stock Inter Company Transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Reference',
        default=lambda self: _('New'),
        readonly=True,
        required=True,
        copy=False,
    )
    source_company_id = fields.Many2one('res.company', string='Source Company', required=True, tracking=True)
    dest_company_id = fields.Many2one('res.company', string='Destination Company', required=True, tracking=True)
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
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')],
        string='Status',
        default='draft',
        readonly=True,
        tracking=True,
    )
    sale_order_id = fields.Many2one('sale.order', string='Sales Order', readonly=True)
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', readonly=True)
    delivery_picking_id = fields.Many2one('stock.picking', string='Delivery Order', readonly=True)
    receipt_picking_id = fields.Many2one('stock.picking', string='Incoming Shipment', readonly=True)
    customer_invoice_id = fields.Many2one(
        'account.move',
        string='Customer Invoice',
        readonly=True,
        domain="[('move_type', 'in', ('out_invoice', 'out_refund'))]",
    )
    vendor_bill_id = fields.Many2one(
        'account.move',
        string='Vendor Bill',
        readonly=True,
        domain="[('move_type', 'in', ('in_invoice', 'in_refund'))]",
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    date = fields.Date(default=fields.Date.context_today, required=True)
    config_id = fields.Many2one('inter.company.config', string='InterCompany Config')
    transfer_line_ids = fields.One2many(
        'stock.inter.company.transfer.line',
        'transfer_id',
        string='Transfer Lines',
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
        """Assign a sequence and infer companies from warehouses on manual records."""
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('stock.inter.company.transfer') or _('New')
            from_wh = self.env['stock.warehouse'].browse(vals.get('from_warehouse_id'))
            to_wh = self.env['stock.warehouse'].browse(vals.get('to_warehouse_id'))
            if from_wh:
                vals.setdefault('source_company_id', from_wh.company_id.id)
                vals.setdefault('company_id', from_wh.company_id.id)
            if to_wh:
                vals.setdefault('dest_company_id', to_wh.company_id.id)
        return super().create(vals_list)

    @api.onchange('from_warehouse_id')
    def _onchange_from_warehouse_id(self):
        """Keep the source company synchronized with the selected source warehouse."""
        if self.from_warehouse_id:
            self.source_company_id = self.from_warehouse_id.company_id
            self.company_id = self.from_warehouse_id.company_id

    @api.onchange('to_warehouse_id')
    def _onchange_to_warehouse_id(self):
        """Keep the destination company synchronized with the selected destination warehouse."""
        if self.to_warehouse_id:
            self.dest_company_id = self.to_warehouse_id.company_id

    @api.constrains('source_company_id', 'dest_company_id', 'from_warehouse_id', 'to_warehouse_id')
    def _check_transfer_companies(self):
        """Validate company and warehouse consistency for the transfer."""
        for transfer in self:
            if transfer.source_company_id == transfer.dest_company_id:
                raise ValidationError(_('Source and destination companies must be different.'))
            if transfer.from_warehouse_id.company_id != transfer.source_company_id:
                raise ValidationError(_('The source warehouse must belong to the source company.'))
            if transfer.to_warehouse_id.company_id != transfer.dest_company_id:
                raise ValidationError(_('The destination warehouse must belong to the destination company.'))

    def action_process(self):
        """Process a draft manual inter-company transfer."""
        for transfer in self:
            if transfer.state != 'draft':
                continue
            if not transfer.transfer_line_ids:
                raise UserError(_('Add at least one transfer line before processing.'))
            config = transfer.config_id or transfer._get_config()
            transfer.config_id = config
            transfer.write({'state': 'confirmed'})
            transfer._create_documents_from_manual()
            transfer._finalize_generated_documents()
            transfer.write({'state': 'done'})
        return True

    def action_cancel(self):
        """Cancel the transaction record."""
        self.write({'state': 'cancel'})
        return True

    def action_reverse(self):
        """Create a draft return transaction with reversed source/destination data."""
        self.ensure_one()
        return_transfer = self.env['return.inter.company.transfer'].create({
            'source_ict_id': self.id,
            'source_company_id': self.dest_company_id.id,
            'dest_company_id': self.source_company_id.id,
            'from_warehouse_id': self.to_warehouse_id.id,
            'to_warehouse_id': self.from_warehouse_id.id,
            'partner_id': self.source_company_id.partner_id.id,
            'company_id': self.dest_company_id.id,
            'return_line_ids': [
                Command.create({
                    'product_id': line.product_id.id,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id,
                    'price_unit': line.price_unit,
                })
                for line in self.transfer_line_ids
            ],
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'return.inter.company.transfer',
            'view_mode': 'form',
            'res_id': return_transfer.id,
        }

    @api.model
    def create_from_sale_order(self, order, config):
        """Create and process an inter-company transaction from a sale order."""
        transfer = self.with_context(allowed_company_ids=(config.source_company_id | config.dest_company_id).ids).sudo().create({
            'source_company_id': config.source_company_id.id,
            'dest_company_id': config.dest_company_id.id,
            'from_warehouse_id': config.source_company_id.inter_company_warehouse_id.id,
            'to_warehouse_id': config.dest_company_id.inter_company_warehouse_id.id,
            'partner_id': order.partner_id.id,
            'sale_order_id': order.id,
            'company_id': order.company_id.id,
            'config_id': config.id,
            'transfer_line_ids': self._line_commands_from_sale(order),
        })
        order.sudo().inter_company_transfer_id = transfer
        transfer.write({'state': 'confirmed'})
        transfer._create_purchase_order_from_sale(order)
        transfer._refresh_document_links()
        transfer._finalize_generated_documents()
        transfer.write({'state': 'done'})
        return transfer

    @api.model
    def create_from_purchase_order(self, order, config):
        """Create and process an inter-company transaction from a purchase order."""
        transfer = self.with_context(allowed_company_ids=(config.source_company_id | config.dest_company_id).ids).sudo().create({
            'source_company_id': config.source_company_id.id,
            'dest_company_id': config.dest_company_id.id,
            'from_warehouse_id': config.source_company_id.inter_company_warehouse_id.id,
            'to_warehouse_id': config.dest_company_id.inter_company_warehouse_id.id,
            'partner_id': order.partner_id.id,
            'purchase_order_id': order.id,
            'company_id': config.source_company_id.id,
            'config_id': config.id,
            'transfer_line_ids': self._line_commands_from_purchase(order),
        })
        order.sudo().inter_company_transfer_id = transfer
        transfer.write({'state': 'confirmed'})
        transfer._create_sale_order_from_purchase(order)
        transfer._refresh_document_links()
        transfer._finalize_generated_documents()
        transfer.write({'state': 'done'})
        return transfer

    @api.model
    def _line_commands_from_sale(self, order):
        """Prepare transaction line commands from sale order lines."""
        return [
            Command.create({
                'product_id': line.product_id.id,
                'quantity': line.product_uom_qty,
                'uom_id': line.product_uom.id,
                'price_unit': line.price_unit,
            })
            for line in order.order_line.filtered(lambda l: not l.display_type and l.product_id)
        ]

    @api.model
    def _line_commands_from_purchase(self, order):
        """Prepare transaction line commands from purchase order lines."""
        return [
            Command.create({
                'product_id': line.product_id.id,
                'quantity': line.product_qty,
                'uom_id': line.product_uom_id.id,
                'price_unit': line.price_unit,
            })
            for line in order.order_line.filtered(lambda l: not l.display_type and l.product_id)
        ]

    def _get_config(self):
        """Return the active configuration for this transfer's company pair."""
        self.ensure_one()
        config = self.env['inter.company.config'].search([
            ('source_company_id', '=', self.source_company_id.id),
            ('dest_company_id', '=', self.dest_company_id.id),
            ('active', '=', True),
        ], limit=1)
        if not config:
            raise UserError(_('No inter-company rule is configured for %s -> %s.') % (
                self.source_company_id.display_name,
                self.dest_company_id.display_name,
            ))
        return config

    def _create_documents_from_manual(self):
        """Create both sale and purchase documents for a manual transfer."""
        self.ensure_one()
        sale_order = self._create_sale_order()
        purchase_order = self._create_purchase_order()
        self.write({
            'sale_order_id': sale_order.id,
            'purchase_order_id': purchase_order.id,
        })
        sale_order.with_context(skip_inter_company_transfer=True).action_confirm()
        purchase_order.with_context(skip_inter_company_transfer=True).button_confirm()
        sale_order.sudo().inter_company_transfer_id = self
        purchase_order.sudo().inter_company_transfer_id = self
        self._refresh_document_links()

    def _create_purchase_order_from_sale(self, source_sale_order):
        """Create and confirm the destination purchase order for a source sale order."""
        self.ensure_one()
        purchase_order = self._create_purchase_order(origin=source_sale_order.name)
        self.purchase_order_id = purchase_order
        purchase_order.sudo().inter_company_transfer_id = self
        purchase_order.with_context(skip_inter_company_transfer=True).button_confirm()

    def _create_sale_order_from_purchase(self, source_purchase_order):
        """Create and confirm the source sale order for a destination purchase order."""
        self.ensure_one()
        sale_order = self._create_sale_order(origin=source_purchase_order.name)
        self.sale_order_id = sale_order
        sale_order.sudo().inter_company_transfer_id = self
        sale_order.with_context(skip_inter_company_transfer=True).action_confirm()

    def _create_sale_order(self, origin=False):
        """Create the source-company sale order represented by this transfer."""
        self.ensure_one()
        SaleOrder = self.env['sale.order'].with_company(self.source_company_id).with_context(
            allowed_company_ids=(self.source_company_id | self.dest_company_id).ids,
            skip_inter_company_transfer=True,
        ).sudo()
        return SaleOrder.create({
            'partner_id': self.dest_company_id.partner_id.id,
            'company_id': self.source_company_id.id,
            'warehouse_id': self.from_warehouse_id.id,
            'origin': origin or self.name,
            'client_order_ref': self.name,
            'order_line': [
                Command.create({
                    'product_id': line.product_id.id,
                    'name': line.product_id.get_product_multiline_description_sale() or line.product_id.display_name,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.uom_id.id,
                    'price_unit': line.price_unit,
                })
                for line in self.transfer_line_ids
            ],
        })

    def _create_purchase_order(self, origin=False):
        """Create the destination-company purchase order represented by this transfer."""
        self.ensure_one()
        PurchaseOrder = self.env['purchase.order'].with_company(self.dest_company_id).with_context(
            allowed_company_ids=(self.source_company_id | self.dest_company_id).ids,
            skip_inter_company_transfer=True,
        ).sudo()
        planned_date = fields.Datetime.now()
        return PurchaseOrder.create({
            'partner_id': self.source_company_id.partner_id.id,
            'company_id': self.dest_company_id.id,
            'picking_type_id': self.to_warehouse_id.in_type_id.id,
            'origin': origin or self.name,
            'order_line': [
                Command.create({
                    'product_id': line.product_id.id,
                    'name': line.product_id.display_name,
                    'product_qty': line.quantity,
                    'product_uom_id': line.uom_id.id,
                    'price_unit': line.price_unit,
                    'date_planned': planned_date,
                })
                for line in self.transfer_line_ids
            ],
        })

    def _refresh_document_links(self):
        """Update picking and accounting links from generated SO/PO documents."""
        for transfer in self:
            sale_pickings = transfer.sale_order_id.picking_ids.filtered(lambda p: p.state != 'cancel')
            purchase_pickings = transfer.purchase_order_id.picking_ids.filtered(lambda p: p.state != 'cancel')
            vals = {}
            if sale_pickings:
                vals['delivery_picking_id'] = sale_pickings[:1].id
                sale_pickings.sudo().inter_company_transfer_id = transfer
            if purchase_pickings:
                vals['receipt_picking_id'] = purchase_pickings[:1].id
                purchase_pickings.sudo().inter_company_transfer_id = transfer
            if transfer.sale_order_id.invoice_ids:
                vals['customer_invoice_id'] = transfer.sale_order_id.invoice_ids.filtered(
                    lambda m: m.move_type in ('out_invoice', 'out_refund')
                )[:1].id
            if transfer.purchase_order_id.invoice_ids:
                vals['vendor_bill_id'] = transfer.purchase_order_id.invoice_ids.filtered(
                    lambda m: m.move_type in ('in_invoice', 'in_refund')
                )[:1].id
            if vals:
                transfer.sudo().write(vals)
            (transfer.customer_invoice_id | transfer.vendor_bill_id).sudo().inter_company_transfer_id = transfer

    def _finalize_generated_documents(self):
        """Run optional picking validation and invoice creation/posting."""
        for transfer in self:
            config = transfer.config_id or transfer._get_config()
            pickings = transfer.delivery_picking_id | transfer.receipt_picking_id
            if config.auto_validate_picking:
                transfer._validate_pickings(pickings)
            if config.auto_create_invoice:
                transfer._create_invoices()
            if config.auto_validate_invoice:
                invoices = transfer.customer_invoice_id | transfer.vendor_bill_id
                invoices.filtered(lambda move: move.state == 'draft').with_context(
                    allowed_company_ids=(transfer.source_company_id | transfer.dest_company_id).ids,
                ).sudo().action_post()

    def _validate_pickings(self, pickings):
        """Validate generated pickings with done quantities set to demanded quantities."""
        for picking in pickings.filtered(lambda p: p.state not in ('done', 'cancel')):
            picking = picking.with_company(picking.company_id).sudo()
            picking.action_confirm()
            picking.action_assign()
            for move in picking.move_ids.filtered(lambda m: m.state not in ('done', 'cancel')):
                if not move.quantity:
                    move.quantity = move.product_uom_qty
            result = picking.with_context(skip_sanity_check=True, cancel_backorder=True).button_validate()
            if isinstance(result, dict):
                raise UserError(_('Picking %s needs manual validation before the inter-company transaction can finish.') % picking.display_name)
        self._refresh_document_links()

    def _create_invoices(self):
        """Create customer invoice and vendor bill for generated sale/purchase documents."""
        self.ensure_one()
        allowed_companies = (self.source_company_id | self.dest_company_id).ids
        if self.sale_order_id and not self.customer_invoice_id:
            invoice = self.sale_order_id.with_context(
                allowed_company_ids=allowed_companies,
            ).with_company(self.source_company_id).sudo()._create_invoices(final=True)
            invoice.sudo().inter_company_transfer_id = self
            self.customer_invoice_id = invoice[:1]
        if self.purchase_order_id and not self.vendor_bill_id:
            before = self.purchase_order_id.invoice_ids
            self.purchase_order_id.with_context(
                allowed_company_ids=allowed_companies,
            ).with_company(self.dest_company_id).sudo().action_create_invoice()
            invoice = (self.purchase_order_id.invoice_ids - before) or self.purchase_order_id.invoice_ids[:1]
            invoice.sudo().inter_company_transfer_id = self
            self.vendor_bill_id = invoice[:1]

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

    def action_view_delivery_picking(self):
        return self._action_open_record(self.delivery_picking_id)

    def action_view_receipt_picking(self):
        return self._action_open_record(self.receipt_picking_id)

    def action_view_customer_invoice(self):
        return self._action_open_record(self.customer_invoice_id)

    def action_view_vendor_bill(self):
        return self._action_open_record(self.vendor_bill_id)


class StockInterCompanyTransferLine(models.Model):
    _name = 'stock.inter.company.transfer.line'
    _description = 'Stock Inter Company Transfer Line'
    _order = 'id'

    transfer_id = fields.Many2one(
        'stock.inter.company.transfer',
        string='Transfer',
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
        """Default the UoM and price from the selected product."""
        if self.product_id:
            self.uom_id = self.product_id.uom_id
            self.price_unit = self.product_id.lst_price
