from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ConstructionProject(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.project'
    _description = 'Construction Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Project Name', required=True, tracking=True)
    reference = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    # Address
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Suite/Apt')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State/Province', domain="[('country_id', '=', country_id)]")
    zip = fields.Char(string='ZIP Code')
    country_id = fields.Many2one('res.country', string='Country')

    # Duration
    date_start = fields.Date(string='Start Date', tracking=True)
    date_end = fields.Date(string='End Date', tracking=True)

    # Location
    longitude = fields.Float(string='Longitude', digits=(16, 6))
    latitude = fields.Float(string='Latitude', digits=(16, 6))

    # Contact
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')

    active = fields.Boolean(string='Active', default=True)

    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('short_closed', 'Short Closed'),
    ], string='Status', default='draft', tracking=True)

    # Relational
    sub_project_ids = fields.One2many('el_construction.sub.project', 'project_id', string='Sub Projects')
    image_ids = fields.One2many('el_construction.project.image', 'project_id', string='Images')
    boq_ids = fields.One2many('el_construction.boq', 'project_id', string='BOQs')
    budget_ids = fields.One2many('el_construction.budget', 'project_id', string='Budgets')
    phase_ids = fields.One2many('el_construction.phase', 'project_id', string='Phases')
    work_order_ids = fields.One2many('el_construction.work.order', 'project_id', string='Work Orders')
    material_requisition_ids = fields.One2many('el_construction.material.requisition', 'project_id', string='Material Requisitions')
    task_ids = fields.One2many('el_construction.task', 'project_id', string='Tasks')
    extra_expense_ids = fields.One2many('el_construction.extra.expense', 'project_id', string='Extra Expenses')

    # Computed
    sub_project_count = fields.Integer(compute='_compute_counts', string='Sub Projects')
    budget_count = fields.Integer(compute='_compute_counts', string='Budgets')
    work_order_count = fields.Integer(compute='_compute_counts', string='Work Orders')
    mreq_count = fields.Integer(compute='_compute_counts', string='Material Requisitions')
    task_count = fields.Integer(compute='_compute_counts', string='Tasks')
    phase_count = fields.Integer(compute='_compute_counts', string='Phases')
    expense_count = fields.Integer(compute='_compute_counts', string='Expenses')

    # Permits
    permit_ids = fields.One2many('el_construction.permit', 'project_id', string='Permits & Approvals')
    quality_point_ids = fields.One2many('el_construction.quality.point', 'project_id', string='Quality Check Points')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('el_construction.project') or 'New'
        return super().create(vals_list)

    @api.depends('sub_project_ids', 'permit_ids', 'budget_ids', 'work_order_ids', 'material_requisition_ids', 'boq_ids', 'task_ids', 'phase_ids', 'extra_expense_ids')
    def _compute_counts(self):
        for rec in self:
            rec.sub_project_count = len(rec.sub_project_ids)
            rec.budget_count = len(rec.budget_ids)
            rec.work_order_count = len(rec.work_order_ids)
            rec.mreq_count = len(rec.material_requisition_ids)
            rec.task_count = len(rec.task_ids)
            rec.phase_count = len(rec.phase_ids)
            rec.expense_count = len(rec.extra_expense_ids)

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        return super().write(vals)

    def unlink(self):
        for rec in self:
            has_moves = any([
                rec.sub_project_ids,
                rec.permit_ids,
                self.env['el_construction.budget'].search_count([('project_id','=',rec.id)]),
                self.env['el_construction.work.order'].search_count([('project_id','=',rec.id)]),
                self.env['el_construction.material.requisition'].search_count([('project_id','=',rec.id)]),
                self.env['el_construction.boq'].search_count([('project_id','=',rec.id)]),
                self.env['purchase.order'].search_count([('project_id','=',rec.id)]) if 'project_id' in self.env['purchase.order']._fields else 0,
            ])
            if has_moves:
                rec.active = False
                continue
            super(ConstructionProject, rec).unlink()
        return True

    def action_archive(self):
        for project in self:
            if project.state not in ('completed', 'short_closed'):
                raise UserError(_('A Project can only be archived after it is Completed or Short Closed.'))
            blockers = project._closure_gate_messages()
            if blockers:
                raise UserError(_('The Project cannot be archived while closure blockers remain:\n• %s') % '\n• '.join(blockers))
        self.write({'active': False})
        return True

    def action_unarchive(self):
        self.write({'active': True})
        return True

    def action_start(self):
        return self._transition('in_progress', {'draft': {'in_progress'}})

    def action_complete(self):
        return self._transition('completed', {'in_progress': {'completed', 'short_closed'}})

    def action_short_close(self):
        return self._transition('short_closed', {'in_progress': {'completed', 'short_closed'}})

    def action_reset_draft(self):
        self._require_manager()
        return self._transition('draft', {'in_progress': {'draft'}}, manager=True)

    def action_view_sub_projects(self):
        return {
            'name': _('Sub Projects'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.sub.project',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_budgets(self):
        return {
            'name': _('Budgets'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.budget',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_work_orders(self):
        return {
            'name': _('Work Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.work.order',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_mreq(self):
        return {
            'name': _('Material Requisitions'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.material.requisition',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_tasks(self):
        return {
            'name': _('Tasks'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.task',
            'view_mode': 'list,gantt,kanban,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id, 'search_default_group_project': 1},
        }

    def action_view_task_planning(self):
        self.ensure_one()
        return {
            'name': _('Project Schedule'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.task',
            'view_mode': 'gantt',
            'view_id': self.env.ref('el_construction_management.view_construction_task_gantt').id,
            'domain': [('project_id', '=', self.id)],
            'context': {
                'default_project_id': self.id,
                'search_default_group_phase': 1,
            },
        }

    def action_view_phases(self):
        return {
            'name': _('Phases (WBS)'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.phase',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_expenses(self):
        return {
            'name': _('Extra Expenses'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.extra.expense',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    @api.constrains('company_id', 'warehouse_id')
    def _check_company_warehouse(self):
        for rec in self:
            if rec.warehouse_id and rec.warehouse_id.company_id and rec.warehouse_id.company_id != rec.company_id:
                raise ValidationError(_('Project warehouse company must match the Project company.'))

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError(_('End Date must be after Start Date.'))

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            self.state_id = self.env['res.country.state'].search(
                [('country_id', '=', self.country_id.id)], limit=1
            )
        else:
            self.state_id = False


class ConstructionProjectImage(models.Model):
    _name = 'el_construction.project.image'
    _description = 'Construction Project Image'

    project_id = fields.Many2one('el_construction.project', string='Project', required=True, ondelete='cascade')
    name = fields.Char(string='Description')
    image = fields.Binary(string='Image', attachment=True)

