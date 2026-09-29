from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ConstructionProgressBilling(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.progress.billing'
    _description = 'Progress Billing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Milestone Name', required=True)
    reference = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True)
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    date = fields.Date(string='Date', default=fields.Date.context_today)

    # Customer
    partner_id = fields.Many2one('res.partner', string='Customer')
    invoice_type = fields.Selection([
        ('type_wise', 'Type Wise Invoice'),
        ('single', 'Single Invoice'),
    ], string='Invoice Type', default='single')

    # Phase & Work Order
    phase_id = fields.Many2one('el_construction.phase', string='Phase')
    work_order_id = fields.Many2one('el_construction.work.order', string='Work Order')

    # Include options
    include_material = fields.Boolean(string='Material Lines', default=True)
    include_equipment = fields.Boolean(string='Equipment Lines', default=True)
    include_labour = fields.Boolean(string='Labour Lines', default=True)
    include_overhead = fields.Boolean(string='Overhead Lines', default=True)
    include_other = fields.Boolean(string='Other Lines', default=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], string='Status', default='draft', tracking=True)

    # Billing Lines
    material_line_ids = fields.One2many('el_construction.progress.billing.line', 'billing_id',
                                         string='Material Lines', domain=[('line_type', '=', 'material')])
    equipment_line_ids = fields.One2many('el_construction.progress.billing.line', 'billing_id',
                                          string='Equipment Lines', domain=[('line_type', '=', 'equipment')])
    labour_line_ids = fields.One2many('el_construction.progress.billing.line', 'billing_id',
                                       string='Labour Lines', domain=[('line_type', '=', 'labour')])
    overhead_line_ids = fields.One2many('el_construction.progress.billing.line', 'billing_id',
                                         string='Overhead Lines', domain=[('line_type', '=', 'overhead')])
    other_line_ids = fields.One2many('el_construction.progress.billing.line', 'billing_id',
                                      string='Other Lines', domain=[('line_type', '=', 'other')])

    # Totals
    material_total = fields.Float(string='Material Total', compute='_compute_totals', store=True)
    equipment_total = fields.Float(string='Equipment Total', compute='_compute_totals', store=True)
    labour_total = fields.Float(string='Labour Total', compute='_compute_totals', store=True)
    overhead_total = fields.Float(string='Overhead Total', compute='_compute_totals', store=True)
    other_total = fields.Float(string='Other Total', compute='_compute_totals', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_totals', store=True)

    # Invoices
    invoice_ids = fields.Many2many('account.move', string='Invoices', compute='_compute_invoice_links', store=False)
    invoice_link_ids = fields.One2many('account.move', 'construction_progress_billing_id', string='Linked Invoices')
    invoice_count = fields.Integer(compute='_compute_invoice_links', string='Invoices')

    notes = fields.Text(string='Notes')

    @api.constrains('project_id', 'sub_project_id', 'phase_id', 'work_order_id', 'company_id')
    def _check_context(self):
        for rec in self:
            if rec.project_id and rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('Billing company must match the Project company.'))
            if rec.sub_project_id and (rec.sub_project_id.project_id != rec.project_id or rec.sub_project_id.company_id != rec.company_id):
                raise ValidationError(_('Sub Project must belong to the same Project and Company.'))
            if rec.phase_id and (rec.phase_id.project_id != rec.project_id or rec.phase_id.company_id != rec.company_id):
                raise ValidationError(_('Phase must belong to the same Project and Company.'))
            if rec.work_order_id and (rec.work_order_id.project_id != rec.project_id or rec.work_order_id.company_id != rec.company_id):
                raise ValidationError(_('Work Order must belong to the same Project and Company.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('el_construction.progress.billing') or 'New'
        return super().create(vals_list)

    @api.depends('material_line_ids.total_amount', 'equipment_line_ids.total_amount',
                 'labour_line_ids.total_amount', 'overhead_line_ids.total_amount',
                 'other_line_ids.total_amount')
    def _compute_totals(self):
        for rec in self:
            all_lines = rec.material_line_ids | rec.equipment_line_ids | rec.labour_line_ids | rec.overhead_line_ids | rec.other_line_ids
            rec.material_total = sum(l.total_amount for l in all_lines if l.line_type == 'material')
            rec.equipment_total = sum(l.total_amount for l in all_lines if l.line_type == 'equipment')
            rec.labour_total = sum(l.total_amount for l in all_lines if l.line_type == 'labour')
            rec.overhead_total = sum(l.total_amount for l in all_lines if l.line_type == 'overhead')
            rec.other_total = sum(l.total_amount for l in all_lines if l.line_type == 'other')
            rec.total_amount = (rec.material_total + rec.equipment_total + rec.labour_total +
                                rec.overhead_total + rec.other_total)

    @api.depends('invoice_link_ids')
    def _compute_invoice_links(self):
        for rec in self:
            rec.invoice_ids = rec.invoice_link_ids
            rec.invoice_count = len(rec.invoice_link_ids)

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        protected = {
            'project_id', 'sub_project_id', 'partner_id', 'phase_id', 'work_order_id',
            'line_ids', 'include_material', 'include_equipment', 'include_labour',
            'include_overhead', 'include_other',
        }
        if protected.intersection(vals):
            for record in self:
                if record.state != 'draft':
                    raise UserError(_('Only Draft Progress Billings can be edited.'))
        return super().write(vals)

    def action_load_work_order_lines(self):
        """Load lines from the selected work order."""
        if self.state != 'draft':
            raise UserError(_('Billing lines can only be loaded while the billing is Draft.'))
        if not self.work_order_id:
            raise UserError(_('Please select a Work Order first.'))

        wo = self.work_order_id
        lines_to_create = []

        if self.include_material:
            for line in wo.material_line_ids:
                lines_to_create.append((0, 0, {
                    'billing_id': self.id,
                    'line_type': 'material',
                    'product_id': line.product_id.id,
                    'description': line.description,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id,
                    'unit_price': line.unit_price,
                }))

        if self.include_equipment:
            for line in wo.equipment_line_ids:
                lines_to_create.append((0, 0, {
                    'billing_id': self.id,
                    'line_type': 'equipment',
                    'product_id': line.product_id.id,
                    'description': line.description,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id,
                    'unit_price': line.unit_price,
                }))

        if self.include_labour:
            for line in wo.labour_line_ids:
                lines_to_create.append((0, 0, {
                    'billing_id': self.id,
                    'line_type': 'labour',
                    'product_id': line.product_id.id,
                    'description': line.description,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id,
                    'unit_price': line.unit_price,
                }))

        if self.include_overhead:
            for line in wo.overhead_line_ids:
                lines_to_create.append((0, 0, {
                    'billing_id': self.id,
                    'line_type': 'overhead',
                    'product_id': line.product_id.id,
                    'description': line.description,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id,
                    'unit_price': line.unit_price,
                }))

        if self.include_other:
            for line in self.env['el_construction.work.order.line'].search([('work_order_id', '=', wo.id), ('line_type', '=', 'other')]):
                lines_to_create.append((0, 0, {
                    'billing_id': self.id,
                    'line_type': 'other',
                    'product_id': line.product_id.id,
                    'description': line.description,
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id,
                    'unit_price': line.unit_price,
                }))

        # Loading is a full refresh: always remove the current snapshot first.
        self.env['el_construction.progress.billing.line'].search([('billing_id', '=', self.id)]).unlink()
        for line_vals in lines_to_create:
            self.env['el_construction.progress.billing.line'].create(line_vals[2])

    def action_start(self):
        return self._transition('in_progress', {'draft': {'in_progress'}})

    def action_complete(self):
        for rec in self:
            rec._lock_records()
            rec.invalidate_recordset(['state', 'invoice_link_ids'])
            if rec.state != 'in_progress':
                raise UserError(_('Only In Progress Progress Billings can be completed.'))
            invoices = rec.invoice_link_ids
            if not invoices:
                raise UserError(_('A Progress Billing must be invoiced before it can be completed.'))
            if any(invoice.state == 'cancel' for invoice in invoices):
                raise UserError(_('A Progress Billing cannot be completed while any linked invoice is Cancelled.'))
        return self._transition('completed', {'in_progress': {'completed'}}, manager=True)

    def action_reset_draft(self):
        return self._transition('draft', {'in_progress': {'draft'}}, manager=True)

    def action_create_invoice(self):
        """Create customer invoice from progress billing"""
        if self.state != 'in_progress':
            raise UserError(_('An invoice can only be created while the Progress Billing is In Progress.'))
        self._lock_records()
        self.invalidate_recordset(['invoice_link_ids'])
        if self.invoice_link_ids.filtered(lambda m: m.state != 'cancel'):
            raise UserError(_('An invoice already exists for this Progress Billing.'))
        if not self.partner_id:
            raise UserError(_('Please select a Customer.'))

        invoice_lines = []
        all_lines = self.env['el_construction.progress.billing.line'].search([('billing_id', '=', self.id)])
        for line in all_lines:
            invoice_lines.append((0, 0, {
                'name': line.description or line.product_id.name or 'Billing Line',
                'product_id': line.product_id.id if line.product_id else False,
                'quantity': line.quantity,
                'price_unit': line.unit_price,
                'tax_ids': [(6, 0, line.tax_ids.ids)] if line.tax_ids else [],
            }))

        if not invoice_lines:
            raise UserError(_('No billing lines to invoice.'))
        if all_lines.filtered(lambda line: not line.product_id):
            raise UserError(_('Each Progress Billing line must have a Product before invoicing so Odoo can determine the income account and taxes.'))

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_origin': self.reference,
            'construction_progress_billing_id': self.id,
            'invoice_line_ids': invoice_lines,
        })

        return {
            'name': _('Invoice'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }

    def action_view_invoices(self):
        return {
            'name': _('Invoices'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
        }
