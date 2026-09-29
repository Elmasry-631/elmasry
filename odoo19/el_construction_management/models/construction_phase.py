from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ConstructionPhase(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.phase'
    _description = 'Construction Phase / Work Breakdown Structure'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    title = fields.Char(string='Phase Title', required=True)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True)
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    sequence = fields.Integer(string='Sequence', default=10)

    # Hierarchy
    parent_id = fields.Many2one('el_construction.phase', string='Parent Phase')
    child_ids = fields.One2many('el_construction.phase', 'parent_id', string='Child Phases')

    # Duration
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')

    # Costing
    material_cost = fields.Float(string='Material Cost')
    equipment_cost = fields.Float(string='Equipment Cost')
    labour_cost = fields.Float(string='Labour Cost')
    overhead_cost = fields.Float(string='Overhead Cost')
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True)

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ], string='Status', default='draft', tracking=True)

    # Work Orders
    work_order_ids = fields.One2many('el_construction.work.order', 'phase_id', string='Work Orders')
    work_order_count = fields.Integer(compute='_compute_work_order_count', string='Work Orders')

    # Phase Entries
    entry_ids = fields.One2many('el_construction.phase.entry', 'phase_id', string='Phase Entries')

    description = fields.Text(string='Description')
    progress = fields.Float(string='Progress (%)', compute='_compute_progress', store=True)

    @api.constrains('material_cost', 'equipment_cost', 'labour_cost', 'overhead_cost')
    def _check_costs(self):
        for rec in self:
            if min(rec.material_cost, rec.equipment_cost, rec.labour_cost, rec.overhead_cost) < 0:
                raise ValidationError(_('Phase costs cannot be negative.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.phase') or 'New'
        return super().create(vals_list)

    @api.constrains('project_id', 'sub_project_id', 'parent_id', 'company_id')
    def _check_hierarchy_consistency(self):
        for rec in self:
            if rec.project_id and rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('Phase company must match the Project company.'))
            if rec.sub_project_id and rec.sub_project_id.project_id != rec.project_id:
                raise ValidationError(_('Phase Sub Project must belong to the selected Project.'))
            if rec.sub_project_id and rec.sub_project_id.company_id != rec.company_id:
                raise ValidationError(_('Phase company must match the Sub Project company.'))
            if rec.parent_id:
                if rec.parent_id == rec or rec.parent_id.project_id != rec.project_id or rec.parent_id.company_id != rec.company_id:
                    raise ValidationError(_('Parent Phase must belong to the same Project and Company and cannot be itself.'))
                ancestor = rec.parent_id
                seen = {rec.id}
                while ancestor:
                    if ancestor.id in seen:
                        raise ValidationError(_('Phase hierarchy cannot contain circular parent relationships.'))
                    seen.add(ancestor.id)
                    ancestor = ancestor.parent_id

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError(_('End Date must be after Start Date.'))

    @api.depends('material_cost', 'equipment_cost', 'labour_cost', 'overhead_cost')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.material_cost + rec.equipment_cost + rec.labour_cost + rec.overhead_cost

    @api.depends('work_order_ids.state', 'child_ids.progress')
    def _compute_progress(self):
        for rec in self:
            if rec.child_ids:
                child_progress = rec.child_ids.mapped('progress')
                rec.progress = sum(child_progress) / len(child_progress) if child_progress else 0.0
            else:
                valid_orders = rec.work_order_ids.filtered(lambda wo: wo.state not in ('draft', 'cancelled'))
                if valid_orders:
                    done_count = len(valid_orders.filtered(lambda wo: wo.state == 'done'))
                    rec.progress = (done_count / len(valid_orders)) * 100
                else:
                    rec.progress = 0.0

    @api.depends('work_order_ids')
    def _compute_work_order_count(self):
        for rec in self:
            rec.work_order_count = len(rec.work_order_ids)

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        return super().write(vals)

    def action_start(self):
        return self._transition('in_progress', {'draft': {'in_progress'}, 'on_hold': {'in_progress'}})

    def action_complete(self):
        for phase in self:
            open_children = phase.child_ids.filtered(lambda child: child.state not in ('completed',))
            if open_children:
                raise UserError(_('Phase cannot be completed while child phases are still open: %s') % ', '.join(open_children.mapped('title')))
            open_orders = phase.work_order_ids.filtered(lambda wo: wo.state not in ('done', 'cancelled'))
            if open_orders:
                raise UserError(_('Phase cannot be completed while Work Orders are still open: %s') % ', '.join(open_orders.mapped('name')))
        return self._transition('completed', {'in_progress': {'completed'}})

    def action_hold(self):
        return self._transition('on_hold', {'in_progress': {'on_hold'}})

    def action_reset_draft(self):
        return self._transition('draft', {'on_hold': {'draft'}}, manager=True)

    def action_view_work_orders(self):
        return {
            'name': _('Work Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.work.order',
            'view_mode': 'list,form',
            'domain': [('phase_id', '=', self.id)],
            'context': {
                'default_phase_id': self.id,
                'default_project_id': self.project_id.id,
                'default_sub_project_id': self.sub_project_id.id,
            },
        }


class ConstructionPhaseEntry(models.Model):
    _name = 'el_construction.phase.entry'
    _description = 'Phase Entry'

    phase_id = fields.Many2one('el_construction.phase', string='Phase', required=True, ondelete='cascade')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    description = fields.Text(string='Description')
    entry_type = fields.Selection([
        ('material', 'Material'),
        ('equipment', 'Equipment'),
        ('labour', 'Labour'),
        ('overhead', 'Overhead'),
        ('other', 'Other'),
    ], string='Type', default='material')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)

    @api.constrains('quantity', 'unit_price')
    def _check_values(self):
        for entry in self:
            if entry.quantity < 0 or entry.unit_price < 0:
                raise ValidationError(_('Phase entry quantity and unit price cannot be negative.'))

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for entry in self:
            entry.amount = entry.quantity * entry.unit_price
