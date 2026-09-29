# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


# ============================================================
# Overtime Rule
# ============================================================
class HrAttendanceRuleOvertime(models.Model):
    _name = 'hr.attendance.rule.overtime'
    _description = 'HR Attendance Overtime Rule'
    _order = 'type, name'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    type = fields.Selection([
        ('working_day', 'Overtime On Working Days'),
        ('weekend', 'Overtime On Weekends'),
        ('public_holiday', 'Overtime On Public Holidays'),
    ], string='Type', required=True)
    apply_after_minutes = fields.Float(
        string='Apply After (minutes)',
        default=0.0,
        help="Overtime will be calculated only after this number of minutes.",
    )
    rate = fields.Float(
        string='Rate',
        default=1.0,
        required=True,
        help="Multiplier applied to the employee hourly rate. "
             "1.5 = 150% of the hourly rate.",
    )
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    _unique_type_company = models.Constraint(
        'unique(type, company_id)',
        'Only one overtime rule per type per company is allowed.',
    )


# ============================================================
# Lateness Rule + Steps
# ============================================================
class HrAttendanceRuleLateness(models.Model):
    _name = 'hr.attendance.rule.lateness'
    _description = 'HR Attendance Lateness Rule'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(string='Active', default=True)
    step_ids = fields.One2many(
        'hr.attendance.rule.lateness.step',
        'lateness_id',
        string='Lateness Steps',
        copy=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    def get_step_for_minutes(self, late_minutes):
        """Return matching step for given late minutes, or empty recordset."""
        self.ensure_one()
        for step in self.step_ids:
            if step.from_minutes <= late_minutes <= step.to_minutes:
                return step
        return self.env['hr.attendance.rule.lateness.step']


class HrAttendanceRuleLatenessStep(models.Model):
    _name = 'hr.attendance.rule.lateness.step'
    _description = 'HR Attendance Lateness Step'
    _order = 'from_minutes'

    lateness_id = fields.Many2one(
        'hr.attendance.rule.lateness',
        string='Lateness Rule',
        required=True,
        ondelete='cascade',
    )
    from_minutes = fields.Float(string='From (minutes)', required=True)
    to_minutes = fields.Float(
        string='To (minutes)',
        required=True,
        help="Use a large number for the upper bound of the last step.",
    )
    penalty_type = fields.Selection([
        ('rate', 'Rate (multiplier on hourly rate)'),
        ('amount', 'Amount (fixed deduction)'),
    ], string='Penalty Type', required=True, default='rate')
    rate = fields.Float(
        string='Rate',
        default=1.0,
        help="Multiplier applied to initial rate. 1.5 = 150% of initial rate.",
    )
    initial_rate = fields.Float(
        string='Initial Rate',
        default=1.0,
        help="Base rate the multiplier applies to (usually 1.0).",
    )
    amount = fields.Float(
        string='Amount',
        help="Fixed amount deducted when this step is hit.",
    )
    company_id = fields.Many2one(
        'res.company',
        related='lateness_id.company_id',
        store=True,
    )

    @api.constrains('from_minutes', 'to_minutes')
    def _check_ranges(self):
        for rec in self:
            if rec.to_minutes < rec.from_minutes:
                raise UserError(_(
                    "Step 'To' (%s) cannot be smaller than 'From' (%s)."
                ) % (rec.to_minutes, rec.from_minutes))


# ============================================================
# Absence Rule + Steps
# ============================================================
class HrAttendanceRuleAbsence(models.Model):
    _name = 'hr.attendance.rule.absence'
    _description = 'HR Attendance Absence Rule'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(string='Active', default=True)
    step_ids = fields.One2many(
        'hr.attendance.rule.absence.step',
        'absence_id',
        string='Absence Steps',
        copy=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    def get_step_for_days(self, absence_days):
        """Return matching step for given absence days, or empty recordset."""
        self.ensure_one()
        for step in self.step_ids:
            if step.from_days <= absence_days <= step.to_days:
                return step
        return self.env['hr.attendance.rule.absence.step']


class HrAttendanceRuleAbsenceStep(models.Model):
    _name = 'hr.attendance.rule.absence.step'
    _description = 'HR Attendance Absence Step'
    _order = 'from_days'

    absence_id = fields.Many2one(
        'hr.attendance.rule.absence',
        string='Absence Rule',
        required=True,
        ondelete='cascade',
    )
    from_days = fields.Integer(string='From (days)', required=True, default=1)
    to_days = fields.Integer(
        string='To (days)',
        required=True,
        default=9999,
        help="Use a large number for the upper bound of the last step.",
    )
    rate = fields.Float(
        string='Rate',
        default=1.0,
        help="Multiplier applied to the daily wage. 1.5 = 150% deduction.",
    )
    company_id = fields.Many2one(
        'res.company',
        related='absence_id.company_id',
        store=True,
    )

    @api.constrains('from_days', 'to_days')
    def _check_ranges(self):
        for rec in self:
            if rec.to_days < rec.from_days:
                raise UserError(_(
                    "Step 'To' (%s) cannot be smaller than 'From' (%s)."
                ) % (rec.to_days, rec.from_days))
