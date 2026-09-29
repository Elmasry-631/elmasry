from .workflow_mixin import ConstructionWorkflowMixin

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ConstructionQualityCheck(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.quality.check'
    _description = 'Construction Quality Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True, index=True)
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project', index=True)
    phase_id = fields.Many2one('el_construction.phase', string='Phase', index=True)
    work_order_id = fields.Many2one('el_construction.work.order', string='Work Order', index=True)
    company_id = fields.Many2one(
        'res.company', string='Company', required=True, index=True,
        default=lambda self: self.env.company,
    )

    date = fields.Date(string='Inspection Date', required=True, default=fields.Date.context_today, index=True)
    inspector_id = fields.Many2one('hr.employee', string='Inspector', index=True)
    inspection_method = fields.Selection([
        ('visual', 'Visual Inspection'),
        ('measurement', 'Measurement / Dimensional Check'),
        ('test', 'Test / Laboratory'),
        ('document', 'Document Review'),
        ('other', 'Other'),
    ], string='Inspection Method', default='visual')
    check_type = fields.Selection([
        ('material', 'Material Inspection'),
        ('workmanship', 'Workmanship Inspection'),
        ('safety', 'Safety Check'),
        ('structural', 'Structural Inspection'),
        ('electrical', 'Electrical Inspection'),
        ('plumbing', 'Plumbing Inspection'),
        ('final', 'Final Inspection'),
        ('other', 'Other'),
    ], string='Check Type', required=True, default='material')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Inspection'),
        ('pass', 'Passed'),
        ('conditional', 'Conditional Pass'),
        ('fail', 'Failed'),
        ('recheck', 'Re-inspection Required'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, index=True)

    check_line_ids = fields.One2many(
        'el_construction.quality.check.line', 'quality_check_id', string='Check Points',
    )

    result_notes = fields.Text(string='Inspection Result / Notes')
    corrective_action = fields.Text(string='Corrective / Preventive Action')
    recheck_date = fields.Date(string='Re-inspection Date')
    closed_date = fields.Date(string='Closed Date', readonly=True)
    closed_by_id = fields.Many2one('res.users', string='Closed By', readonly=True)

    document = fields.Binary(string='Inspection Report', attachment=True)
    document_name = fields.Char(string='File Name')
    image_ids = fields.One2many(
        'el_construction.quality.check.image', 'quality_check_id', string='Evidence / Images',
    )

    total_check_points = fields.Integer(compute='_compute_result_summary', store=True)
    passed_check_points = fields.Integer(compute='_compute_result_summary', store=True)
    failed_check_points = fields.Integer(compute='_compute_result_summary', store=True)
    pending_check_points = fields.Integer(compute='_compute_result_summary', store=True)
    completion_percent = fields.Float(compute='_compute_result_summary', store=True)

    _reference_unique = models.Constraint(
        'UNIQUE(name)',
        'Quality Check Reference must be unique.',
    )

    @api.depends('check_line_ids.result')
    def _compute_result_summary(self):
        for rec in self:
            lines = rec.check_line_ids
            total = len(lines)
            passed = len(lines.filtered(lambda line: line.result == 'pass'))
            failed = len(lines.filtered(lambda line: line.result == 'fail'))
            pending = len(lines.filtered(lambda line: line.result == 'na'))
            rec.total_check_points = total
            rec.passed_check_points = passed
            rec.failed_check_points = failed
            rec.pending_check_points = pending
            rec.completion_percent = (passed + failed) / total * 100 if total else 0.0

    @api.constrains('project_id', 'sub_project_id', 'phase_id', 'work_order_id', 'company_id', 'inspector_id')
    def _check_consistency(self):
        for rec in self:
            if rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('Quality Check company must match the Project company.'))
            if rec.sub_project_id:
                if rec.sub_project_id.project_id != rec.project_id:
                    raise ValidationError(_('Sub Project must belong to the selected Project.'))
                if rec.sub_project_id.company_id != rec.company_id:
                    raise ValidationError(_('Quality Check company must match the Sub Project company.'))
            if rec.phase_id:
                if rec.phase_id.project_id != rec.project_id:
                    raise ValidationError(_('Phase must belong to the selected Project.'))
                if rec.sub_project_id and rec.phase_id.sub_project_id and rec.phase_id.sub_project_id != rec.sub_project_id:
                    raise ValidationError(_('Phase must belong to the selected Sub Project.'))
                if rec.phase_id.company_id != rec.company_id:
                    raise ValidationError(_('Quality Check company must match the Phase company.'))
            if rec.work_order_id:
                if rec.work_order_id.project_id != rec.project_id:
                    raise ValidationError(_('Work Order must belong to the selected Project.'))
                if rec.sub_project_id and rec.work_order_id.sub_project_id and rec.work_order_id.sub_project_id != rec.sub_project_id:
                    raise ValidationError(_('Work Order must belong to the selected Sub Project.'))
                if rec.phase_id and rec.work_order_id.phase_id and rec.work_order_id.phase_id != rec.phase_id:
                    raise ValidationError(_('Work Order must belong to the selected Phase.'))
                if rec.work_order_id.company_id != rec.company_id:
                    raise ValidationError(_('Quality Check company must match the Work Order company.'))
            if rec.inspector_id and rec.inspector_id.company_id and rec.inspector_id.company_id != rec.company_id:
                raise ValidationError(_('Inspector must belong to the Quality Check company.'))

    @api.constrains('date', 'recheck_date', 'closed_date')
    def _check_dates(self):
        for rec in self:
            if rec.recheck_date and rec.recheck_date < rec.date:
                raise ValidationError(_('Re-inspection Date cannot be before the Inspection Date.'))
            if rec.closed_date and rec.closed_date < rec.date:
                raise ValidationError(_('Closed Date cannot be before the Inspection Date.'))

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if not self.project_id:
            self.sub_project_id = self.phase_id = self.work_order_id = False
            return
        if self.sub_project_id and self.sub_project_id.project_id != self.project_id:
            self.sub_project_id = False
        if self.phase_id and self.phase_id.project_id != self.project_id:
            self.phase_id = False
        if self.work_order_id and self.work_order_id.project_id != self.project_id:
            self.work_order_id = False

    @api.onchange('sub_project_id')
    def _onchange_sub_project_id(self):
        if self.sub_project_id and self.sub_project_id.project_id != self.project_id:
            self.sub_project_id = False
        if self.phase_id and self.sub_project_id and self.phase_id.sub_project_id and self.phase_id.sub_project_id != self.sub_project_id:
            self.phase_id = False
        if self.work_order_id and self.sub_project_id and self.work_order_id.sub_project_id and self.work_order_id.sub_project_id != self.sub_project_id:
            self.work_order_id = False

    @api.onchange('phase_id')
    def _onchange_phase_id(self):
        if self.phase_id and self.phase_id.project_id != self.project_id:
            self.phase_id = False
        if self.work_order_id and self.phase_id and self.work_order_id.phase_id and self.work_order_id.phase_id != self.phase_id:
            self.work_order_id = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.setdefault('company_id', self.env.company.id)
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.quality.check') or 'New'
        records = super().create(vals_list)
        records._check_consistency()
        return records

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        for record in self:
            if record.state in ('closed', 'cancelled'):
                protected = set(vals) - {'state'}
                if protected:
                    raise UserError(_('Closed or cancelled Quality Checks are read-only. Reset a cancelled check before editing it.'))
            if record.state in ('pass', 'conditional', 'fail', 'recheck'):
                if set(vals) & {'project_id', 'sub_project_id', 'phase_id', 'work_order_id', 'company_id', 'date', 'inspector_id', 'check_type'}:
                    raise UserError(_('Inspection identity and planning fields cannot be changed after the inspection has started.'))
        result = super().write(vals)
        if set(vals) & {'project_id', 'sub_project_id', 'phase_id', 'work_order_id', 'company_id', 'inspector_id'}:
            self._check_consistency()
        return result

    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Only Draft Quality Checks can be deleted.'))
        return super().unlink()

    def _validate_ready_for_inspection(self):
        self.ensure_one()
        if not self.inspector_id:
            raise UserError(_('An Inspector must be assigned before starting the inspection.'))
        if not self.check_line_ids:
            raise UserError(_('Add at least one Check Point before starting the inspection.'))

    def _validate_result(self, result_state):
        self.ensure_one()
        if not self.check_line_ids:
            raise UserError(_('At least one Check Point is required before recording a result.'))
        if self.pending_check_points:
            raise UserError(_('Complete every Check Point before recording the final inspection result.'))
        if result_state == 'pass' and self.failed_check_points:
            raise UserError(_('A Quality Check with failed Check Points cannot be marked Passed.'))
        if result_state == 'fail' and not self.failed_check_points:
            raise UserError(_('Mark at least one Check Point as Failed before marking the Quality Check Failed.'))
        if result_state in ('fail', 'conditional') and not self.corrective_action:
            raise UserError(_('Corrective / Preventive Action is required for a Failed or Conditional Quality Check.'))

    def action_start(self):
        for record in self:
            record._validate_ready_for_inspection()
        return self._transition('in_progress', {'draft': {'in_progress'}})

    def action_pass(self):
        for record in self:
            record._validate_result('pass')
        return self._transition('pass', {'in_progress': {'pass'}, 'recheck': {'pass'}})

    def action_fail(self):
        for record in self:
            record._validate_result('fail')
            if not record.recheck_date:
                raise UserError(_('Set the Re-inspection Date before marking a Quality Check Failed.'))
        return self._transition('fail', {'in_progress': {'fail'}, 'recheck': {'fail'}})

    def action_conditional(self):
        for record in self:
            record._validate_result('conditional')
        return self._transition('conditional', {'in_progress': {'conditional'}, 'recheck': {'conditional'}})

    def action_recheck(self):
        for record in self:
            if record.state != 'fail':
                raise UserError(_('Only Failed Quality Checks can be sent for Re-inspection.'))
            if not record.recheck_date:
                raise UserError(_('Set the Re-inspection Date before requesting Re-inspection.'))
            if not record.corrective_action:
                raise UserError(_('Corrective / Preventive Action is required before Re-inspection.'))
        return self._transition('recheck', {'fail': {'recheck'}})

    def action_close(self):
        self.ensure_one()
        if self.state not in ('pass', 'conditional'):
            raise UserError(_('Only Passed or Conditional Quality Checks can be closed.'))
        if self.state == 'conditional' and not self.corrective_action:
            raise UserError(_('A Conditional Quality Check requires a documented Corrective / Preventive Action.'))
        self._require_manager(_('Only Construction Managers can close a Quality Check.'))
        self.write({
            'closed_date': fields.Date.context_today(self),
            'closed_by_id': self.env.user.id,
        })
        return self._transition('closed', {'pass': {'closed'}, 'conditional': {'closed'}}, manager=True)

    def action_cancel(self):
        return self._transition(
            'cancelled',
            {'draft': {'cancelled'}, 'in_progress': {'cancelled'}, 'recheck': {'cancelled'}},
            manager=True,
        )

    def action_reset_draft(self):
        return self._transition('draft', {'cancelled': {'draft'}}, manager=True)
