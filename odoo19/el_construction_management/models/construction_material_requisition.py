from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, AccessError


class ConstructionMaterialRequisition(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.material.requisition'
    _description = 'Material Requisition'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True)
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project')
    work_order_id = fields.Many2one('el_construction.work.order', string='Work Order')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    date = fields.Date(string='Date', default=fields.Date.context_today)
    required_date = fields.Date(string='Required Date')
    requested_by = fields.Many2one('hr.employee', string='Requested By')
    approved_by = fields.Many2one('res.users', string='Approved By')
    department_id = fields.Many2one('hr.department', string='Department')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('under_approval', 'Under Approval'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('ready', 'Ready for Delivery'),
        ('withdrawal', 'Withdrawal'),
        ('done', 'Done'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    line_ids = fields.One2many('el_construction.material.requisition.line', 'requisition_id',
                                string='Requisition Lines')

    @api.constrains('project_id', 'sub_project_id', 'work_order_id', 'warehouse_id', 'company_id')
    def _check_consistency(self):
        for rec in self:
            if rec.project_id and rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('Requisition company must match the Project company.'))
            if rec.sub_project_id and (rec.sub_project_id.project_id != rec.project_id or rec.sub_project_id.company_id != rec.company_id):
                raise ValidationError(_('Sub Project must belong to the same Project and Company.'))
            if rec.work_order_id and (rec.work_order_id.project_id != rec.project_id or rec.work_order_id.company_id != rec.company_id):
                raise ValidationError(_('Work Order must belong to the same Project and Company.'))
            if rec.warehouse_id and rec.warehouse_id.company_id and rec.warehouse_id.company_id != rec.company_id:
                raise ValidationError(_('Warehouse company must match the Requisition company.'))

    notes = fields.Text(string='Notes')
    rejection_reason = fields.Text(string='Rejection Reason')

    # Purchase / Transfer counts
    purchase_order_count = fields.Integer(compute='_compute_po_count', string='Purchase Orders')
    purchase_order_ids = fields.Many2many('purchase.order', string='Purchase Orders',
                                          compute='_compute_po_count', store=False)

    # Explicit source links (do not rely on origin text matching).
    purchase_order_link_ids = fields.One2many('purchase.order', 'material_requisition_id', string='Linked Purchase Orders')
    picking_link_ids = fields.One2many('stock.picking', 'material_requisition_id', string='Linked Transfers')
    internal_transfer_count = fields.Integer(compute='_compute_transfer_count', string='Internal Transfers')
    picking_ids = fields.Many2many('stock.picking', string='Internal Transfers',
                                    compute='_compute_transfer_count', store=False)

    total_amount = fields.Float(string='Total Amount', compute='_compute_total', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.material.requisition') or 'New'
        return super().create(vals_list)

    @api.depends('line_ids.amount')
    def _compute_total(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('amount'))

    @api.depends('purchase_order_link_ids')
    def _compute_po_count(self):
        for rec in self:
            orders = rec.purchase_order_link_ids
            rec.purchase_order_ids = orders
            rec.purchase_order_count = len(orders)

    @api.depends('picking_link_ids')
    def _compute_transfer_count(self):
        for rec in self:
            pickings = rec.picking_link_ids
            rec.picking_ids = pickings
            rec.internal_transfer_count = len(pickings)

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        return super().write(vals)

    def action_submit_approval(self):
        return self._transition('under_approval', {'draft': {'under_approval'}})

    def action_approve(self):
        self._require_manager()
        return self._transition('approved', {'under_approval': {'approved'}}, manager=True) and self.write({'approved_by': self.env.uid})

    def action_in_progress(self):
        return self._transition('in_progress', {'approved': {'in_progress'}})

    def action_ready(self):
        return self._transition('ready', {'in_progress': {'ready'}})

    def action_withdrawal(self):
        return self._transition('withdrawal', {'ready': {'withdrawal'}})

    def action_done(self):
        self._lock_records()
        self.invalidate_recordset(['purchase_order_link_ids', 'picking_link_ids'])
        # الصح: اسمح بـ Done لو الفاتورة Posted حتى لو PO لسه purchase (مخصوم من Budget أوتوماتيك)
        def _po_blocking(po):
            if po.state in ('done', 'cancel', 'purchase'):
                # لو له Bill Posted اعتبره منتهي للـ MReq
                if po.invoice_ids.filtered(lambda m: m.state == 'posted' and m.move_type == 'in_invoice'):
                    return False
            return po.state not in ('done', 'cancel')
        if self.purchase_order_link_ids and any(_po_blocking(po) for po in self.purchase_order_link_ids):
            raise UserError(_('The requisition cannot be marked Done while linked Purchase Orders are not Done/Cancelled (or billed). Confirm/Invoice the PO first.'))
        if self.picking_link_ids and any(p.state not in ('done', 'cancel') for p in self.picking_link_ids):
            raise UserError(_('The requisition cannot be marked Done while linked transfers are not Done or Cancelled.'))
        return self._transition('done', {'withdrawal': {'done'}}, manager=True)

    def action_reject(self):
        return self._transition('rejected', {'under_approval': {'rejected'}}, manager=True)

    def action_cancel(self):
        return self._transition('cancelled', {'draft': {'cancelled'}, 'under_approval': {'cancelled'}, 'approved': {'cancelled'}}, manager=True)

    def action_reset_draft(self):
        return self._transition('draft', {'rejected': {'draft'}, 'cancelled': {'draft'}}, manager=True)

    def action_create_purchase_order(self):
        """Create purchase order from material requisition lines"""
        if self.state != 'approved':
            raise UserError(_('Purchase Orders can only be created from an Approved requisition.'))
        self._lock_records()
        self.invalidate_recordset(['purchase_order_link_ids'])
        if self.purchase_order_link_ids:
            raise UserError(_('Purchase Orders have already been created for this requisition.'))
        if not self.line_ids:
            raise UserError(_('Please add requisition lines first.'))

        missing_vendor_lines = self.line_ids.filtered(lambda l: not l.vendor_id)
        if missing_vendor_lines:
            raise UserError(
                _('Every Material Requisition line must have a Vendor before creating Purchase Orders. ' 
                  'Missing vendor on line(s): %s') %
                ', '.join(missing_vendor_lines.mapped('display_name'))
            )

        vendor_lines = {}
        for line in self.line_ids:
            vendor_lines.setdefault(line.vendor_id.id, []).append(line)

        orders = self.env['purchase.order']
        for vendor_id, lines in vendor_lines.items():
            po = self.env['purchase.order'].create({
                'partner_id': vendor_id,
                'origin': self.name,
                'material_requisition_id': self.id,
                'company_id': self.company_id.id,
            })
            for line in lines:
                self.env['purchase.order.line'].create({
                    'order_id': po.id,
                    'product_id': line.product_id.id,
                    'name': line.description or line.product_id.name,
                    'product_qty': line.quantity,
                    'product_uom_id': line.uom_id.id or line.product_id.uom_id.id,
                    'price_unit': line.unit_price,
                    'material_requisition_line_id': line.id,
                })
            orders |= po

        self.action_in_progress()
        if len(orders) == 1:
            return {
                'name': _('Purchase Order'),
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.order',
                'view_mode': 'form',
                'res_id': orders.id,
            }
        return {
            'name': _('Purchase Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', orders.ids)],
        }

    def action_create_internal_transfer(self):
        """Create internal transfer from material requisition"""
        if self.state != 'approved':
            raise UserError(_('Internal Transfers can only be created from an Approved requisition.'))
        self._lock_records()
        self.invalidate_recordset(['picking_link_ids'])
        if self.picking_link_ids:
            raise UserError(_('An Internal Transfer has already been created for this requisition.'))
        if not self.warehouse_id:
            raise UserError(_('Please select a warehouse.'))
        if self.warehouse_id.company_id and self.warehouse_id.company_id != self.company_id:
            raise ValidationError(_('Warehouse company must match the requisition company.'))

        picking_type = self.env['stock.picking.type'].search([
            ('warehouse_id', '=', self.warehouse_id.id),
            ('code', '=', 'internal'),
        ], limit=1)

        if not picking_type:
            raise UserError(_('No internal transfer type found for the selected warehouse.'))

        picking = self.env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'origin': self.name,
            'material_requisition_id': self.id,
            'company_id': self.company_id.id,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': picking_type.default_location_dest_id.id,
        })

        for line in self.line_ids:
            self.env['stock.move'].create({
                'name': line.description or line.product_id.name,
                'picking_id': picking.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'product_uom': line.uom_id.id or line.product_id.uom_id.id,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': picking_type.default_location_dest_id.id,
                'material_requisition_line_id': line.id,
            })

        self.action_in_progress()
        return {
            'name': _('Internal Transfer'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'res_id': picking.id,
        }

    def action_view_purchase_orders(self):
        return {
            'name': _('Purchase Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('material_requisition_id', '=', self.id)],
        }

    def action_view_transfers(self):
        return {
            'name': _('Internal Transfers'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'list,form',
            'domain': [('material_requisition_id', '=', self.id)],
        }


class ConstructionMaterialRequisitionLine(models.Model):
    _name = 'el_construction.material.requisition.line'
    _description = 'Material Requisition Line'

    requisition_id = fields.Many2one('el_construction.material.requisition', string='Requisition', required=True, ondelete='cascade', index=True)
    purchase_order_line_ids = fields.One2many('purchase.order.line', 'material_requisition_line_id', string='Purchase Order Lines')
    stock_move_ids = fields.One2many('stock.move', 'material_requisition_line_id', string='Stock Moves')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', domain="[('id', 'in', vendor_domain_ids)]")
    vendor_domain_ids = fields.Many2many('res.partner', compute='_compute_vendor_domain', string='Available Vendors', readonly=True)
    notes = fields.Char(string='Notes')

    def write(self, vals):
        for line in self:
            if line.requisition_id.state not in ('draft', 'rejected'):
                raise UserError(_('Requisition lines can only be changed while the requisition is Draft or Rejected.'))
        return super().write(vals)

    def unlink(self):
        for line in self:
            if line.requisition_id.state not in ('draft', 'rejected'):
                raise UserError(_('Requisition lines can only be deleted while the requisition is Draft or Rejected.'))
        return super().unlink()

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.unit_price

    @api.model_create_multi
    def create(self, vals_list):
        reqs = self.env['el_construction.material.requisition'].browse([v.get('requisition_id') for v in vals_list if v.get('requisition_id')])
        if any(req.state not in ('draft', 'rejected') for req in reqs):
            raise UserError(_('Requisition lines can only be created while the requisition is Draft or Rejected.'))
        return super().create(vals_list)

    @api.constrains('quantity', 'unit_price', 'uom_id', 'product_id')
    def _check_values(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_('Requisition quantity must be greater than zero.'))
            if line.unit_price < 0:
                raise ValidationError(_('Unit price cannot be negative.'))
            if line.uom_id and line.product_id.uom_id and not line.uom_id._has_common_reference(line.product_id.uom_id):
                raise ValidationError(_('Unit of Measure must use the same category as the Product.'))

    @api.depends('product_id')
    def _compute_vendor_domain(self):
        for line in self:
            sellers = line.product_id.seller_ids.filtered(lambda s: s.partner_id.active) if line.product_id else self.env['product.supplierinfo']
            line.vendor_domain_ids = sellers.mapped('partner_id')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_id.id
            self.unit_price = self.product_id.standard_price
            seller = self.product_id.seller_ids.filtered(lambda s: s.partner_id.active)[:1]
            self.vendor_id = seller.partner_id if seller else False
        else:
            self.vendor_id = False
