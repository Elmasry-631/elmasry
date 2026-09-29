from .workflow_mixin import ConstructionWorkflowMixin
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ConstructionBudget(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.budget'
    _description = 'Construction Budget'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True, index=True)
    sub_project_id = fields.Many2one(
        'el_construction.sub.project', string='Sub Project', index=True,
    )
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env.company, index=True,
    )
    date = fields.Date(string='Date', default=fields.Date.context_today)
    notes = fields.Text(string='Notes')

    budget_method = fields.Selection([
        ('project', 'Project Total'),
        ('lines', 'Budget Lines'),
        ('hybrid', 'Project Total + Budget Lines'),
    ], string='Budget Method', default='lines', required=True, tracking=True)
    project_budget_amount = fields.Float(
        string='Project Budget', default=0.0,
        help='Overall approved budget for the selected project/sub-project. '
             'Required for Project Total and Project Total + Budget Lines methods.',
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    line_ids = fields.One2many('el_construction.budget.line', 'budget_id', string='Budget Lines')

    total_planned = fields.Float(string='Total Planned', compute='_compute_totals')
    allocated_amount = fields.Float(string='Allocated to Lines', compute='_compute_totals')
    unallocated_amount = fields.Float(string='Unallocated', compute='_compute_totals')
    allocation_percentage = fields.Float(string='Allocation (%)', compute='_compute_totals')
    total_actual = fields.Float(string='Total Actual', compute='_compute_totals')
    total_variance = fields.Float(string='Total Variance', compute='_compute_totals')

    _project_sub_project_company_uniq = models.Constraint(
        'UNIQUE(project_id, sub_project_id, company_id)',
        'Only one budget is allowed per Project, Sub Project and Company.',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.budget') or 'New'
            vals.setdefault('company_id', self.env.company.id)
        records = super().create(vals_list)
        records._check_company_consistency()
        return records

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        if any(key in vals for key in ('project_id', 'sub_project_id', 'company_id', 'budget_method', 'project_budget_amount')):
            for record in self:
                if record.state not in ('draft', 'confirmed'):
                    raise UserError(_('Approved or completed budgets cannot change their structure or project budget.'))
        result = super().write(vals)
        self._check_company_consistency()
        return result

    def _check_company_consistency(self):
        for rec in self:
            if rec.project_id and rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('Budget company must match the project company.'))
            if rec.sub_project_id and rec.sub_project_id.project_id != rec.project_id:
                raise ValidationError(_('Sub Project must belong to the selected Project.'))
            if rec.sub_project_id and rec.sub_project_id.company_id != rec.company_id:
                raise ValidationError(_('Budget company must match the sub-project company.'))

    def _check_structure(self):
        for record in self:
            if record.project_budget_amount < 0:
                raise ValidationError(_('Project Budget cannot be negative.'))
            if record.budget_method == 'project' and record.line_ids:
                raise ValidationError(_('Project Total budgets cannot contain Budget Lines.'))
            if record.budget_method == 'lines' and record.project_budget_amount:
                raise ValidationError(_('Budget Lines method must not have a separate Project Budget amount.'))
            if record.budget_method in ('project', 'hybrid') and not record.project_budget_amount:
                raise ValidationError(_('Project Budget amount must be greater than zero for this Budget Method.'))
            if record.budget_method == 'hybrid':
                allocated = sum(record.line_ids.mapped('planned_amount'))
                if allocated > record.project_budget_amount:
                    raise ValidationError(_(
                        'Allocated Budget Lines (%(allocated).2f) cannot exceed the Project Budget (%(total).2f).',
                        allocated=allocated, total=record.project_budget_amount,
                    ))

    def _check_transition(self, new_state):
        allowed = {
            'draft': {'confirmed', 'cancelled'},
            'confirmed': {'approved', 'draft', 'cancelled'},
            'approved': {'done', 'cancelled'},
            'done': set(),
            'cancelled': {'draft'},
        }
        for record in self:
            if new_state != record.state and new_state not in allowed.get(record.state, set()):
                raise UserError(_(
                    'Invalid Budget transition: %(old)s → %(new)s.',
                    old=record.state,
                    new=new_state,
                ))

    def _check_editable(self):
        for record in self:
            if record.state not in ('draft', 'confirmed'):
                raise UserError(_('Budget lines can only be changed while the budget is Draft or Confirmed.'))

    def action_confirm(self):
        self._check_structure()
        self._check_transition('confirmed')
        return self._transition('confirmed', {'draft': {'confirmed', 'cancelled'}, 'confirmed': {'confirmed'}})

    def action_approve(self):
        self._check_structure()
        self._check_transition('approved')
        return self._transition('approved', {'confirmed': {'approved'}}, manager=True)

    def action_done(self):
        self._check_structure()
        self._check_transition('done')
        return self._transition('done', {'approved': {'done'}}, manager=True)

    def action_cancel(self):
        for record in self:
            if record.state == 'done':
                raise UserError(_('A completed budget cannot be cancelled.'))
        return self._transition('cancelled', {
            'draft': {'cancelled'}, 'confirmed': {'cancelled'}, 'approved': {'cancelled'}
        }, manager=True)

    def action_reset_draft(self):
        self._check_transition('draft')
        return self._transition('draft', {'confirmed': {'draft'}, 'cancelled': {'draft'}}, manager=True)

    @api.depends('budget_method', 'project_budget_amount', 'line_ids.planned_amount', 'line_ids.actual_amount')
    def _compute_totals(self):
        for rec in self:
            allocated = sum(rec.line_ids.mapped('planned_amount'))
            if rec.budget_method in ('project', 'hybrid'):
                planned = rec.project_budget_amount
            else:
                planned = allocated
            rec.total_planned = planned
            rec.allocated_amount = allocated
            rec.unallocated_amount = max(planned - allocated, 0.0)
            rec.allocation_percentage = (allocated / planned * 100.0) if planned else 0.0
            rec.total_actual = sum(rec.line_ids.mapped('actual_amount'))
            rec.total_variance = planned - rec.total_actual

    @api.constrains('budget_method', 'project_budget_amount', 'line_ids')
    def _check_budget_structure(self):
        self._check_structure()

    def action_recompute_actual(self):
        """Force a fresh read of all explicit cost allocations."""
        self.invalidate_recordset(['total_actual', 'total_variance'])
        self._compute_totals()
        return True
