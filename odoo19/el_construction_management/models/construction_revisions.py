from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

from .workflow_mixin import ConstructionWorkflowMixin


class ConstructionBOQRevision(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.boq.revision'
    _description = 'Construction BOQ Revision'
    _order = 'revision_no desc'

    name = fields.Char(required=True)
    boq_id = fields.Many2one('el_construction.boq', required=True, ondelete='cascade')
    project_id = fields.Many2one(related='boq_id.project_id', store=True, index=True)
    company_id = fields.Many2one(related='boq_id.company_id', store=True, index=True)
    revision_no = fields.Integer(required=True, default=1)
    state = fields.Selection([('draft','Draft'),('approved','Approved'),('cancelled','Cancelled')], default='draft')
    reason = fields.Text(required=True)
    line_ids = fields.One2many('el_construction.boq.revision.line', 'revision_id')
    approved_by = fields.Many2one('res.users', readonly=True)
    approved_on = fields.Datetime(readonly=True)

    _boq_revision_unique = models.Constraint(

        'unique(boq_id, revision_no)',

        'BOQ revision number must be unique per BOQ.',

    )
    def write(self, vals):
        for rec in self:
            if rec.state in ('approved', 'cancelled') and set(vals) - {'message_follower_ids'}:
                raise UserError(_('Finalized BOQ revisions cannot be modified.'))
        return super().write(vals)

    def action_approve(self):
        if not self.env.user.has_group('el_construction_management.group_construction_manager'):
            raise UserError(_('Only Construction Managers can approve BOQ revisions.'))
        for rec in self:
            if not rec.line_ids:
                raise UserError(_('A BOQ revision must contain at least one line.'))
        self.write({'approved_by': self.env.user.id, 'approved_on': fields.Datetime.now()})
        self._transition('approved', {'draft': {'approved'}}, manager=True)

    def action_cancel(self):
        return self._transition('cancelled', {'draft': {'cancelled'}}, manager=True)


class ConstructionBOQRevisionLine(models.Model):
    _name = 'el_construction.boq.revision.line'
    _description = 'Construction BOQ Revision Line'

    revision_id = fields.Many2one('el_construction.boq.revision', required=True, ondelete='cascade')
    source_line_id = fields.Many2one('el_construction.boq.line', ondelete='set null')
    description = fields.Char(required=True)
    quantity = fields.Float()
    unit_price = fields.Float()
    amount = fields.Float(compute='_compute_amount', store=True)

    @api.depends('quantity','unit_price')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.quantity * rec.unit_price

    @api.model_create_multi
    def create(self, vals_list):
        revisions = self.env['el_construction.boq.revision'].browse([v.get('revision_id') for v in vals_list if v.get('revision_id')])
        if any(rec.state != 'draft' for rec in revisions):
            raise UserError(_('BOQ revision lines can only be created while the revision is Draft.'))
        return super().create(vals_list)

    @api.constrains('revision_id', 'source_line_id')
    def _check_context(self):
        for rec in self:
            if rec.source_line_id and rec.source_line_id.boq_id != rec.revision_id.boq_id:
                raise ValidationError(_('Source BOQ Line must belong to the revision BOQ.'))

    def write(self, vals):
        for rec in self:
            if rec.revision_id.state != 'draft':
                raise UserError(_('BOQ revision lines can only be changed while the revision is Draft.'))
        return super().write(vals)

    def unlink(self):
        if any(r.revision_id.state != 'draft' for r in self):
            raise UserError(_('BOQ revision lines can only be deleted while the revision is Draft.'))
        return super().unlink()

class ConstructionBudgetRevision(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.budget.revision'
    _description = 'Construction Budget Revision'
    _order = 'revision_no desc'

    name = fields.Char(required=True)
    budget_id = fields.Many2one('el_construction.budget', required=True, ondelete='cascade')
    project_id = fields.Many2one(related='budget_id.project_id', store=True, index=True)
    company_id = fields.Many2one(related='budget_id.company_id', store=True, index=True)
    revision_no = fields.Integer(default=1, required=True)
    state = fields.Selection([('draft','Draft'),('approved','Approved'),('cancelled','Cancelled')], default='draft')
    reason = fields.Text(required=True)
    total_amount = fields.Monetary(compute='_compute_total', store=True, currency_field='currency_id')
    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    line_ids = fields.One2many('el_construction.budget.revision.line','revision_id')
    _budget_revision_unique = models.Constraint(
        'unique(budget_id, revision_no)',
        'Budget revision number must be unique per Budget.',
    )
    @api.depends('line_ids.amount')
    def _compute_total(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('amount'))

    def write(self, vals):
        for rec in self:
            if rec.state in ('approved', 'cancelled') and set(vals) - {'message_follower_ids'}:
                raise UserError(_('Finalized Budget revisions cannot be modified.'))
        return super().write(vals)

    def action_approve(self):
        if not self.env.user.has_group('el_construction_management.group_construction_manager'):
            raise UserError(_('Only Construction Managers can approve Budget revisions.'))
        for rec in self:
            if not rec.line_ids:
                raise UserError(_('A Budget revision must contain at least one line.'))
        self._transition('approved', {'draft': {'approved'}}, manager=True)

    def action_cancel(self):
        return self._transition('cancelled', {'draft': {'cancelled'}}, manager=True)


class ConstructionBudgetRevisionLine(models.Model):
    _name = 'el_construction.budget.revision.line'
    _description = 'Construction Budget Revision Line'

    revision_id = fields.Many2one('el_construction.budget.revision', required=True, ondelete='cascade')
    source_line_id = fields.Many2one('el_construction.budget.line', ondelete='set null')
    description = fields.Char(required=True)
    quantity = fields.Float()
    unit_price = fields.Float()
    amount = fields.Monetary(compute='_compute_amount', store=True, currency_field='currency_id')
    currency_id = fields.Many2one(related='revision_id.currency_id', store=True)

    @api.depends('quantity','unit_price')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.quantity * rec.unit_price

    @api.model_create_multi
    def create(self, vals_list):
        revisions = self.env['el_construction.budget.revision'].browse([v.get('revision_id') for v in vals_list if v.get('revision_id')])
        if any(rec.state != 'draft' for rec in revisions):
            raise UserError(_('Budget revision lines can only be created while the revision is Draft.'))
        return super().create(vals_list)

    @api.constrains('revision_id', 'source_line_id')
    def _check_context(self):
        for rec in self:
            if rec.source_line_id and rec.source_line_id.budget_id != rec.revision_id.budget_id:
                raise ValidationError(_('Source Budget Line must belong to the revision Budget.'))

    def write(self, vals):
        for rec in self:
            if rec.revision_id.state != 'draft':
                raise UserError(_('Budget revision lines can only be changed while the revision is Draft.'))
        return super().write(vals)

    def unlink(self):
        if any(r.revision_id.state != 'draft' for r in self):
            raise UserError(_('Budget revision lines can only be deleted while the revision is Draft.'))
        return super().unlink()

class ConstructionTaskBaselineRevision(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.task.baseline.revision'
    _description = 'Construction Task Baseline Revision'
    _order = 'revision_no desc'

    name = fields.Char(required=True)
    project_id = fields.Many2one('el_construction.project', required=True, ondelete='cascade')
    company_id = fields.Many2one(related='project_id.company_id', store=True)
    revision_no = fields.Integer(default=1, required=True)
    state = fields.Selection([('draft','Draft'),('approved','Approved'),('cancelled','Cancelled')], default='draft')
    reason = fields.Text(required=True)
    line_ids = fields.One2many('el_construction.task.baseline.revision.line','revision_id')
    _baseline_revision_unique = models.Constraint(
        'unique(project_id, revision_no)',
        'Baseline revision number must be unique per Project.',
    )
    def write(self, vals):
        for rec in self:
            if rec.state in ('approved', 'cancelled') and set(vals) - {'message_follower_ids'}:
                raise UserError(_('Finalized baseline revisions cannot be modified.'))
        return super().write(vals)

    def action_approve(self):
        if not self.env.user.has_group('el_construction_management.group_construction_manager'):
            raise UserError(_('Only Construction Managers can approve baseline revisions.'))
        for rec in self:
            if not rec.line_ids:
                raise UserError(_('A baseline revision must contain at least one line.'))
        self._transition('approved', {'draft': {'approved'}}, manager=True)

    def action_cancel(self):
        return self._transition('cancelled', {'draft': {'cancelled'}}, manager=True)


class ConstructionTaskBaselineRevisionLine(models.Model):
    _name = 'el_construction.task.baseline.revision.line'
    _description = 'Task Baseline Revision Line'

    revision_id = fields.Many2one('el_construction.task.baseline.revision', required=True, ondelete='cascade')
    task_id = fields.Many2one('el_construction.task', required=True, ondelete='restrict')
    baseline_start = fields.Date()
    baseline_end = fields.Date()
    baseline_hours = fields.Float()

    @api.model_create_multi
    def create(self, vals_list):
        revisions = self.env['el_construction.task.baseline.revision'].browse([v.get('revision_id') for v in vals_list if v.get('revision_id')])
        if any(rec.state != 'draft' for rec in revisions):
            raise UserError(_('Baseline revision lines can only be created while the revision is Draft.'))
        return super().create(vals_list)

    @api.constrains('revision_id', 'task_id', 'baseline_start', 'baseline_end', 'baseline_hours')
    def _check_context(self):
        for rec in self:
            if rec.task_id.project_id != rec.revision_id.project_id:
                raise ValidationError(_('Baseline Task must belong to the revision Project.'))
            if rec.baseline_start and rec.baseline_end and rec.baseline_end < rec.baseline_start:
                raise ValidationError(_('Baseline end date cannot be before the baseline start date.'))
            if rec.baseline_hours < 0:
                raise ValidationError(_('Baseline hours cannot be negative.'))

    def write(self, vals):
        for rec in self:
            if rec.revision_id.state != 'draft':
                raise UserError(_('Baseline revision lines can only be changed while the revision is Draft.'))
        return super().write(vals)

    def unlink(self):
        if any(r.revision_id.state != 'draft' for r in self):
            raise UserError(_('Baseline revision lines can only be deleted while the revision is Draft.'))
        return super().unlink()

class ConstructionBOQRevisionActions(ConstructionWorkflowMixin, models.Model):
    _inherit = 'el_construction.boq'

    def action_create_revision(self, reason):
        self.ensure_one()
        if not reason or not reason.strip():
            raise UserError(_('A revision reason is required.'))
        self._lock_records(self)
        last = self.env['el_construction.boq.revision'].search([('boq_id', '=', self.id)], order='revision_no desc', limit=1)
        rev = self.env['el_construction.boq.revision'].create({'name': '%s-R%s' % (self.name, (last.revision_no if last else 0) + 1), 'boq_id': self.id, 'revision_no': (last.revision_no if last else 0) + 1, 'reason': reason})
        rev.line_ids = [(0, 0, {'source_line_id': l.id, 'description': l.description or l.display_name, 'quantity': l.quantity, 'unit_price': l.unit_price}) for l in self.line_ids]
        return rev

class ConstructionBudgetRevisionActions(ConstructionWorkflowMixin, models.Model):
    _inherit = 'el_construction.budget'

    def action_create_revision(self, reason):
        self.ensure_one()
        if not reason or not reason.strip(): raise UserError(_('A revision reason is required.'))
        self._lock_records(self)
        last = self.env['el_construction.budget.revision'].search([('budget_id', '=', self.id)], order='revision_no desc', limit=1)
        no = (last.revision_no if last else 0) + 1
        rev = self.env['el_construction.budget.revision'].create({'name': '%s-R%s' % (self.name, no), 'budget_id': self.id, 'revision_no': no, 'reason': reason})
        rev.line_ids = [(0, 0, {'source_line_id': l.id, 'description': l.description or l.display_name, 'quantity': l.quantity, 'unit_price': l.unit_price}) for l in self.line_ids]
        return rev
