from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ConstructionWorkOrder(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.work.order'
    _description = 'Construction Work Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True)
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project')
    phase_id = fields.Many2one('el_construction.phase', string='Phase')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    date = fields.Date(string='Date', default=fields.Date.context_today)
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')

    responsible_id = fields.Many2one('hr.employee', string='Responsible')
    description = fields.Text(string='Description')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    # Cost Lines
    material_line_ids = fields.One2many('el_construction.work.order.line', 'work_order_id',
                                         string='Material Lines', domain=[('line_type', '=', 'material')])
    equipment_line_ids = fields.One2many('el_construction.work.order.line', 'work_order_id',
                                          string='Equipment Lines', domain=[('line_type', '=', 'equipment')])
    labour_line_ids = fields.One2many('el_construction.work.order.line', 'work_order_id',
                                       string='Labour Lines', domain=[('line_type', '=', 'labour')])
    overhead_line_ids = fields.One2many('el_construction.work.order.line', 'work_order_id',
                                         string='Overhead Lines', domain=[('line_type', '=', 'overhead')])
    other_line_ids = fields.One2many('el_construction.work.order.line', 'work_order_id',
                                     string='Other Lines', domain=[('line_type', '=', 'other')])

    # Totals
    material_total = fields.Float(string='Material Total', compute='_compute_totals', store=True)
    equipment_total = fields.Float(string='Equipment Total', compute='_compute_totals', store=True)
    labour_total = fields.Float(string='Labour Total', compute='_compute_totals', store=True)
    overhead_total = fields.Float(string='Overhead Total', compute='_compute_totals', store=True)
    other_total = fields.Float(string='Other Total', compute='_compute_totals', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_totals', store=True)

    @api.constrains('project_id', 'sub_project_id', 'phase_id', 'company_id')
    def _check_consistency(self):
        for rec in self:
            if rec.sub_project_id and (rec.sub_project_id.project_id != rec.project_id or rec.sub_project_id.company_id != rec.company_id):
                raise ValidationError(_('Sub Project must belong to the same Project and Company.'))
            if rec.phase_id and (rec.phase_id.project_id != rec.project_id or rec.phase_id.company_id != rec.company_id):
                raise ValidationError(_('Phase must belong to the same Project and Company.'))

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError(_('End Date must be after Start Date.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.work.order') or 'New'
        return super().create(vals_list)

    @api.depends('material_line_ids.amount', 'equipment_line_ids.amount',
                 'labour_line_ids.amount', 'overhead_line_ids.amount', 'other_line_ids.amount')
    def _compute_totals(self):
        for rec in self:
            all_lines = rec.material_line_ids | rec.equipment_line_ids | rec.labour_line_ids | rec.overhead_line_ids | rec.other_line_ids
            rec.material_total = sum(l.amount for l in all_lines if l.line_type == 'material')
            rec.equipment_total = sum(l.amount for l in all_lines if l.line_type == 'equipment')
            rec.labour_total = sum(l.amount for l in all_lines if l.line_type == 'labour')
            rec.overhead_total = sum(l.amount for l in all_lines if l.line_type == 'overhead')
            rec.other_total = sum(l.amount for l in all_lines if l.line_type == 'other')
            rec.total_amount = rec.material_total + rec.equipment_total + rec.labour_total + rec.overhead_total + rec.other_total

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        return super().write(vals)

    def action_confirm(self):
        return self._transition('confirmed', {'draft': {'confirmed'}})

    def action_start(self):
        for work_order in self:
            pending_permits = self.env['el_construction.permit'].search_count([
                ('project_id', '=', work_order.project_id.id),
                ('is_required_for_execution', '=', True),
                ('state', '!=', 'approved'),
            ])
            if pending_permits:
                raise UserError(_('This Work Order cannot start while required Project Permits are not Approved.'))
        return self._transition('in_progress', {'confirmed': {'in_progress'}})

    def action_done(self):
        for work_order in self:
            if self.env['el_construction.quality.check'].search_count([
                ('work_order_id', '=', work_order.id),
                ('state', 'in', ('fail', 'conditional', 'in_progress', 'recheck')),
            ]):
                raise UserError(_('A Work Order cannot be completed while a related Quality Check is failed, conditional, or still in progress.'))
            open_mreqs = self.env['el_construction.material.requisition'].search([
                ('work_order_id', '=', work_order.id),
                ('state', 'not in', ('done', 'cancelled', 'withdrawal', 'rejected')),
            ])
            if open_mreqs:
                raise UserError(_('A Work Order cannot be completed while Material Requisitions are open: %s') % ', '.join(open_mreqs.mapped('name')))
        return self._transition('done', {'in_progress': {'done'}}, manager=True)

    def action_cancel(self):
        return self._transition('cancelled', {'draft': {'cancelled'}, 'confirmed': {'cancelled'}, 'in_progress': {'cancelled'}}, manager=True)

    def action_reset_draft(self):
        return self._transition('draft', {'cancelled': {'draft'}}, manager=True)


class ConstructionWorkOrderLine(models.Model):
    _name = 'el_construction.work.order.line'
    _description = 'Work Order Line'

    work_order_id = fields.Many2one('el_construction.work.order', string='Work Order', required=True, ondelete='cascade')
    line_type = fields.Selection([
        ('material', 'Material'),
        ('equipment', 'Equipment'),
        ('labour', 'Labour'),
        ('overhead', 'Overhead'),
        ('other', 'Other'),
    ], string='Type', required=True, default='material')

    product_id = fields.Many2one('product.product', string='Product')
    budget_line_id = fields.Many2one(
        'el_construction.budget.line', string='Budget Line', ondelete='set null', index=True
    )
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)

    @api.constrains('work_order_id', 'budget_line_id', 'product_id')
    def _check_budget_line_consistency(self):
        for line in self:
            if not line.work_order_id or not line.budget_line_id:
                continue
            budget = line.budget_line_id.budget_id
            if budget.project_id != line.work_order_id.project_id or budget.sub_project_id != line.work_order_id.sub_project_id:
                raise ValidationError(_('Budget Line must belong to the Work Order Project and Sub Project.'))
            if budget.company_id != line.work_order_id.company_id:
                raise ValidationError(_('Budget Line company must match the Work Order company.'))
            if line.product_id and line.budget_line_id.product_id and line.product_id != line.budget_line_id.product_id:
                raise ValidationError(_('Work Order Product must match the Budget Line Product.'))

    @api.onchange('product_id', 'work_order_id')
    def _onchange_budget_line_id(self):
        for line in self:
            if not line.work_order_id:
                line.budget_line_id = False
                continue
            domain = [('project_id', '=', line.work_order_id.project_id.id)]
            if line.work_order_id.sub_project_id:
                domain.append(('sub_project_id', '=', line.work_order_id.sub_project_id.id))
            if line.product_id:
                domain.append(('product_id', '=', line.product_id.id))
            candidates = self.env['el_construction.budget.line'].search(domain)
            line.budget_line_id = candidates[:1] if len(candidates) == 1 else False

    @api.model_create_multi
    def create(self, vals_list):
        orders = self.env['el_construction.work.order'].browse([v.get('work_order_id') for v in vals_list if v.get('work_order_id')])
        if any(order.state not in ('draft', 'cancelled') for order in orders):
            raise UserError(_('Work Order lines can only be created while the Work Order is Draft or Cancelled.'))
        return super().create(vals_list)

    @api.constrains('quantity', 'unit_price', 'uom_id', 'product_id')
    def _check_values(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_('Work Order quantity must be greater than zero.'))
            if line.unit_price < 0:
                raise ValidationError(_('Work Order unit price cannot be negative.'))
            if line.product_id and line.uom_id and line.product_id.uom_id and not line.uom_id._has_common_reference(line.product_id.uom_id):
                raise ValidationError(_('Work Order Unit of Measure must use the same category as the Product.'))

    def write(self, vals):
        for line in self:
            if line.work_order_id.state not in ('draft', 'cancelled'):
                raise UserError(_('Work Order lines can only be changed while the Work Order is Draft or Cancelled.'))
        return super().write(vals)

    def unlink(self):
        for line in self:
            if line.work_order_id.state not in ('draft', 'cancelled'):
                raise UserError(_('Work Order lines can only be deleted while the Work Order is Draft or Cancelled.'))
        return super().unlink()

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_id.id
            self.unit_price = self.product_id.standard_price
