from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ConstructionSubcontract(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.subcontract'
    _description = 'Construction Subcontracting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True)
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project')
    partner_id = fields.Many2one('res.partner', string='Subcontractor', required=True,
                                  domain="[('supplier_rank', '>', 0)]")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    date = fields.Date(string='Date', default=fields.Date.context_today)
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')

    work_description = fields.Text(string='Scope of Work')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    # Lines
    line_ids = fields.One2many('el_construction.subcontract.line', 'subcontract_id', string='Work Lines')

    # Consume Orders
    consume_order_ids = fields.One2many('el_construction.consume.order', 'subcontract_id', string='Consume Orders')
    consume_order_count = fields.Integer(compute='_compute_consume_count', string='Consume Orders')

    # RA Billing
    ra_billing_ids = fields.One2many('el_construction.ra.billing', 'subcontract_id', string='RA Billings')
    ra_billing_count = fields.Integer(compute='_compute_ra_count', string='RA Billings')

    # Totals
    contract_amount = fields.Float(string='Contract Amount', compute='_compute_total', store=True)
    billed_amount = fields.Float(string='Billed Amount', compute='_compute_billed_amount')
    remaining_amount = fields.Float(string='Remaining Contract', compute='_compute_billed_amount')
    vendor_bill_ids = fields.One2many('account.move', 'construction_subcontract_id', string='Vendor Bills')

    # Work Completion
    completion_certificate = fields.Binary(string='Completion Certificate', attachment=True)
    completion_certificate_name = fields.Char(string='Certificate File Name')
    completion_date = fields.Date(string='Completion Date')
    completion_notes = fields.Text(string='Completion Notes')

    notes = fields.Text(string='Notes')

    @api.constrains('project_id', 'sub_project_id', 'company_id')
    def _check_consistency(self):
        for rec in self:
            if rec.project_id and rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('Subcontract company must match the Project company.'))
            if rec.sub_project_id and (rec.sub_project_id.project_id != rec.project_id or rec.sub_project_id.company_id != rec.company_id):
                raise ValidationError(_('Sub Project must belong to the same Project and Company.'))

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError(_('End Date must be after Start Date.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.subcontract') or 'New'
        return super().create(vals_list)

    @api.depends('line_ids.amount')
    def _compute_total(self):
        for rec in self:
            rec.contract_amount = sum(rec.line_ids.mapped('amount'))

    @api.depends('contract_amount', 'ra_billing_ids.state', 'ra_billing_ids.total_amount')
    def _compute_billed_amount(self):
        for rec in self:
            rec.billed_amount = sum(rec.ra_billing_ids.filtered(lambda b: b.state == 'approved').mapped('total_amount'))
            rec.remaining_amount = rec.contract_amount - rec.billed_amount

    @api.depends('consume_order_ids')
    def _compute_consume_count(self):
        for rec in self:
            rec.consume_order_count = len(rec.consume_order_ids)

    @api.depends('ra_billing_ids')
    def _compute_ra_count(self):
        for rec in self:
            rec.ra_billing_count = len(rec.ra_billing_ids)

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        return super().write(vals)

    def action_confirm(self):
        if not self.line_ids:
            raise UserError(_('A subcontract must contain at least one work line.'))
        return self._transition('confirmed', {'draft': {'confirmed'}})

    def action_start(self):
        return self._transition('in_progress', {'confirmed': {'in_progress'}})

    def action_complete(self):
        if self.billed_amount > self.contract_amount:
            raise UserError(_('Billed amount cannot exceed the contract amount.'))
        return self._transition('completed', {'in_progress': {'completed'}}, manager=True) and self.write({'completion_date': fields.Date.context_today(self)})

    def action_cancel(self):
        return self._transition('cancelled', {'draft': {'cancelled'}, 'confirmed': {'cancelled'}, 'in_progress': {'cancelled'}}, manager=True)

    def action_reset_draft(self):
        return self._transition('draft', {'cancelled': {'draft'}}, manager=True)

    def action_view_consume_orders(self):
        return {
            'name': _('Consume Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.consume.order',
            'view_mode': 'list,form',
            'domain': [('subcontract_id', '=', self.id)],
            'context': {'default_subcontract_id': self.id},
        }

    def action_view_ra_billings(self):
        return {
            'name': _('RA Billings'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.ra.billing',
            'view_mode': 'list,form',
            'domain': [('subcontract_id', '=', self.id)],
            'context': {'default_subcontract_id': self.id},
        }

    def action_create_bill(self):
        """Create one vendor bill from subcontract."""
        if self.state not in ('in_progress', 'completed'):
            raise UserError(_('Vendor bills can only be created for an active or completed subcontract.'))
        self._lock_records()
        self.invalidate_recordset(['vendor_bill_ids'])
        existing = self.vendor_bill_ids.filtered(lambda m: m.state != 'cancel')
        if existing:
            raise UserError(_('A vendor bill already exists for this subcontract.'))
        if not self.line_ids:
            raise UserError(_('Cannot create a vendor bill without subcontract lines.'))
        missing_products = self.line_ids.filtered(lambda line: not line.product_id) if 'product_id' in self.env['el_construction.subcontract.line']._fields else self.env['el_construction.subcontract.line']
        if missing_products:
            raise UserError(_('Each subcontract line must have a Product before creating a Vendor Bill so Odoo can determine the expense account and taxes.'))
        invoice = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.partner_id.id,
            'invoice_origin': self.name,
            'construction_subcontract_id': self.id,
            'invoice_line_ids': [(0, 0, {
                'name': line.description or line.work_description,
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'product_uom_id': line.uom_id.id or line.product_id.uom_id.id,
                'price_unit': line.rate,
            }) for line in self.line_ids],
        })
        return {
            'name': _('Vendor Bill'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }


class ConstructionSubcontractLine(models.Model):
    _name = 'el_construction.subcontract.line'
    _description = 'Subcontract Line'

    subcontract_id = fields.Many2one('el_construction.subcontract', string='Subcontract', required=True, ondelete='cascade')
    work_description = fields.Char(string='Work Description', required=True)
    description = fields.Char(string='Details')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    rate = fields.Float(string='Rate')
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)


    @api.model_create_multi
    def create(self, vals_list):
        subs = self.env['el_construction.subcontract'].browse([v.get('subcontract_id') for v in vals_list if v.get('subcontract_id')])
        if any(sub.state not in ('draft', 'cancelled') for sub in subs):
            raise UserError(_('Subcontract lines can only be created while the subcontract is Draft or Cancelled.'))
        return super().create(vals_list)

    @api.depends('quantity', 'rate')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.rate

    @api.constrains('quantity', 'rate')
    def _check_values(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_('Subcontract quantity must be greater than zero.'))
            if line.rate < 0:
                raise ValidationError(_('Subcontract rate cannot be negative.'))
            if line.product_id and line.uom_id and line.product_id.uom_id and not line.uom_id._has_common_reference(line.product_id.uom_id):
                raise ValidationError(_('Subcontract Unit of Measure must use the same category as the Product.'))

    def write(self, vals):
        for line in self:
            if line.subcontract_id.state not in ('draft', 'cancelled'):
                raise UserError(_('Subcontract lines can only be changed while the subcontract is Draft or Cancelled.'))
        return super().write(vals)

    def unlink(self):
        for line in self:
            if line.subcontract_id.state not in ('draft', 'cancelled'):
                raise UserError(_('Subcontract lines can only be deleted while the subcontract is Draft or Cancelled.'))
        return super().unlink()
