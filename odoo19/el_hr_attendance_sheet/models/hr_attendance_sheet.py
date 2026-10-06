# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime, time, timedelta

import pytz

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrAttendanceSheet(models.Model):
    _name = 'hr.attendance.sheet'
    _description = 'HR Attendance Sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_from desc, employee_id'
    _rec_name = 'name'

    # ------------------------------------------------------------
    # FIELDS
    # ------------------------------------------------------------
    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
        tracking=True,
        index=True,
    )
    date_from = fields.Date(string='Date From', required=True, tracking=True)
    date_to = fields.Date(string='Date To', required=True, tracking=True)
    contract_id = fields.Many2one(
        'hr.version',
        string='Contract',
        compute='_compute_contract',
        store=True,
        readonly=False,
        tracking=True,
    )
    policy_id = fields.Many2one(
        'hr.attendance.policy',
        string='Attendance Policy',
        related='contract_id.attendance_policy_id',
        store=True,
        tracking=True,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('computed', 'Computed'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False, index=True)

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        store=True,
    )

    # Lines
    line_ids = fields.One2many(
        'hr.attendance.sheet.line',
        'sheet_id',
        string='Attendance Lines',
        copy=True,
    )

    # Totals (computed from lines)
    total_overtime = fields.Float(
        string='Total Overtime (hours)',
        compute='_compute_totals',
        store=True,
        help="Sum of overtime hours across all days in the period.",
    )
    total_late_in = fields.Float(
        string='Total Late In (minutes)',
        compute='_compute_totals',
        store=True,
        help="Sum of late-in minutes across all days.",
    )
    total_absence = fields.Float(
        string='Total Absence (days)',
        compute='_compute_totals',
        store=True,
        help="Count of days where the employee was absent without leave.",
    )
    total_late_penalty_hours = fields.Float(
        string='Total Late Penalty (hours)',
        compute='_compute_totals',
        store=True,
        help="Sum of the dynamic lateness penalties after escalation.",
    )
    total_absence_penalty_days = fields.Float(
        string='Total Absence Penalty (days)',
        compute='_compute_totals',
        store=True,
        help="Sum of the dynamic absence deductions after escalation.",
    )
    total_difference = fields.Float(
        string='Total Difference (hours)',
        compute='_compute_totals',
        store=True,
        help="Sum of difference hours (worked - planned - overtime).",
    )
    total_planned = fields.Float(
        string='Total Planned (hours)',
        compute='_compute_totals',
        store=True,
    )
    total_worked = fields.Float(
        string='Total Worked (hours)',
        compute='_compute_totals',
        store=True,
    )

    payslip_id = fields.Many2one(
        'hr.payslip',
        string='Payslip',
        readonly=True,
        copy=False,
        tracking=True,
    )
    batch_id = fields.Many2one(
        'hr.attendance.sheet.batch',
        string='Batch',
        readonly=True,
        copy=False,
    )

    # ------------------------------------------------------------
    # COMPUTES
    # ------------------------------------------------------------
    @api.depends('employee_id', 'date_from')
    def _compute_contract(self):
        for rec in self:
            if rec.employee_id and rec.date_from:
                contract = self.env['hr.version'].search([
                    ('employee_id', '=', rec.employee_id.id),
                    ('date_start', '<=', rec.date_from),
                    '|',
                    ('date_end', '=', False),
                    ('date_end', '>=', rec.date_from),
                ], limit=1, order='date_version desc')
                rec.contract_id = contract
            else:
                rec.contract_id = False

    @api.depends(
        'line_ids.overtime_hours',
        'line_ids.late_in_minutes',
        'line_ids.is_absent',
        'line_ids.difference_hours',
        'line_ids.planned_hours',
        'line_ids.worked_hours',
        'line_ids.late_penalty',
        'line_ids.absence_penalty_days',
    )
    def _compute_totals(self):
        for rec in self:
            rec.total_overtime = sum(rec.line_ids.mapped('overtime_hours'))
            rec.total_late_in = sum(rec.line_ids.mapped('late_in_minutes'))
            rec.total_absence = sum(1 for line in rec.line_ids if line.is_absent)
            rec.total_late_penalty_hours = sum(
                rec.line_ids.mapped('late_penalty'))
            rec.total_absence_penalty_days = sum(
                rec.line_ids.mapped('absence_penalty_days'))
            rec.total_difference = sum(rec.line_ids.mapped('difference_hours'))
            rec.total_planned = sum(rec.line_ids.mapped('planned_hours'))
            rec.total_worked = sum(rec.line_ids.mapped('worked_hours'))

    # ------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hr.attendance.sheet'
                ) or _('New')
        return super().create(vals_list)

    @api.constrains('date_from', 'date_to', 'employee_id')
    def _check_period(self):
        for rec in self:
            if rec.date_to < rec.date_from:
                raise UserError(_(
                    "End date (%s) cannot be before start date (%s)."
                ) % (rec.date_to, rec.date_from))
            # Check overlapping sheets for the same employee
            overlapping = self.search([
                ('id', '!=', rec.id),
                ('employee_id', '=', rec.employee_id.id),
                ('state', '!=', 'cancelled'),
                ('date_from', '<=', rec.date_to),
                ('date_to', '>=', rec.date_from),
            ], limit=1)
            if overlapping:
                raise UserError(_(
                    "Period overlaps with existing sheet %s for employee %s."
                ) % (overlapping.name, rec.employee_id.name))

    # ------------------------------------------------------------
    # STATE MACHINE
    # ------------------------------------------------------------
    def action_compute(self):
        """Main computation engine — runs the per-day pipeline."""
        for rec in self:
            if rec.state not in ('draft', 'computed'):
                raise UserError(_(
                    "Sheet %s: can only compute from Draft or Computed state."
                ) % rec.name)
            if not rec.contract_id:
                raise UserError(_(
                    "Sheet %s: no active contract for employee %s on %s."
                ) % (rec.name, rec.employee_id.name, rec.date_from))
            if not rec.policy_id:
                raise UserError(_(
                    "Sheet %s: contract %s has no attendance policy assigned."
                ) % (rec.name, rec.contract_id.name))
            rec._run_computation()
            rec.write({'state': 'computed'})
            rec.message_post(
                body=_("Attendance sheet computed by %s") % self.env.user.name
            )

    def action_approve(self):
        for rec in self:
            if rec.state != 'computed':
                raise UserError(_(
                    "Sheet %s: only computed sheets can be approved."
                ) % rec.name)
            if not rec.line_ids:
                raise UserError(_(
                    "Sheet %s: cannot approve a sheet without lines."
                ) % rec.name)
        self.write({'state': 'approved'})
        for rec in self:
            rec.message_post(
                body=_("Attendance sheet approved by %s") % self.env.user.name
            )

    def action_done(self):
        for rec in self:
            if rec.state != 'approved':
                raise UserError(_(
                    "Sheet %s: only approved sheets can be set to Done."
                ) % rec.name)
            if not rec.payslip_id:
                raise UserError(_(
                    "Sheet %s: a payslip must be created before setting Done."
                ) % rec.name)
        self.write({'state': 'done'})

    def action_cancel(self):
        for rec in self:
            if rec.state not in ('draft', 'computed', 'approved'):
                raise UserError(_(
                    "Sheet %s: cannot cancel a sheet in %s state."
                ) % (rec.name, rec.state))
            if rec.payslip_id and rec.payslip_id.state == 'done':
                raise UserError(_(
                    "Sheet %s: cannot cancel — payslip %s is already done."
                ) % (rec.name, rec.payslip_id.name))
        self.write({'state': 'cancelled'})

    def action_draft(self):
        for rec in self:
            if rec.state != 'cancelled':
                raise UserError(_(
                    "Sheet %s: only cancelled sheets can be reset to draft."
                ) % rec.name)
        self.write({'state': 'draft'})

    # ------------------------------------------------------------
    # COMPUTATION ENGINE
    # ------------------------------------------------------------
    def _run_computation(self):
        """Run the per-day computation pipeline for this sheet."""
        self.ensure_one()
        SheetLine = self.env['hr.attendance.sheet.line']
        # Clear existing lines
        self.line_ids.unlink()

        calendar = self.contract_id.resource_calendar_id
        if not calendar:
            raise UserError(_(
                "Contract %s has no working schedule (resource.calendar)."
            ) % self.contract_id.name)

        # Bulk fetch data for the whole period
        attendances_by_day = self._fetch_attendances_by_day()
        leaves_by_day = self._fetch_leaves_by_day()
        holidays_by_day = self._fetch_public_holidays_by_day()

        # Iterate each day
        current = self.date_from
        delta = timedelta(days=1)
        absence_seq = 0
        late_seq = 0
        while current <= self.date_to:
            day_attendances = attendances_by_day.get(current, [])
            day_leave = leaves_by_day.get(current)
            is_public_holiday = current in holidays_by_day

            line_vals = self._compute_line_for_day(
                current, calendar, day_attendances,
                day_leave, is_public_holiday,
            )
            if line_vals:
                # Track repetition counters used by the escalation rules.
                if line_vals.get('is_absent'):
                    absence_seq += 1
                    line_vals['absence_occurrence'] = absence_seq
                if line_vals.get('late_in_minutes'):
                    late_seq += 1
                    line_vals['late_occurrence'] = late_seq
                line_vals['sheet_id'] = self.id
                SheetLine.create(line_vals)
            current += delta

    def _fetch_attendances_by_day(self):
        """Return dict {date: [hr.attendance, ...]} for the sheet period."""
        self.ensure_one()
        attendances = self.env['hr.attendance'].search([
            ('employee_id', '=', self.employee_id.id),
            ('check_in', '>=', datetime.combine(self.date_from, time.min)),
            ('check_in', '<=', datetime.combine(
                self.date_to, time.max)),
        ])
        result = defaultdict(list)
        for att in attendances:
            day = att.check_in.date()
            result[day].append(att)
        return result

    def _fetch_leaves_by_day(self):
        """Return dict {date: hr.leave} for approved leaves."""
        self.ensure_one()
        leaves = self.env['hr.leave'].search([
            ('employee_id', '=', self.employee_id.id),
            ('state', '=', 'validate'),
            ('date_from', '<=', datetime.combine(self.date_to, time.max)),
            ('date_to', '>=', datetime.combine(self.date_from, time.min)),
        ])
        result = {}
        for leave in leaves:
            current = leave.date_from.date()
            end = leave.date_to.date()
            delta = timedelta(days=1)
            while current <= end:
                if self.date_from <= current <= self.date_to:
                    result[current] = leave
                current += delta
        return result

    def _fetch_public_holidays_by_day(self):
        """Return set of dates where the employee is on public holiday."""
        self.ensure_one()
        holidays = self.env['hr.attendance.public.holiday'].search([
            ('state', '=', 'active'),
            ('company_id', 'in', [False, self.company_id.id]),
            ('date_from', '<=', self.date_to),
            ('date_to', '>=', self.date_from),
        ])
        result = set()
        for holiday in holidays:
            current = holiday.date_from
            delta = timedelta(days=1)
            while current <= holiday.date_to:
                if self.date_from <= current <= self.date_to:
                    if holiday.is_employee_on_holiday(self.employee_id, current):
                        result.add(current)
                current += delta
        return result

    def _compute_line_for_day(self, day, calendar, attendances, leave,
                              is_public_holiday):
        """Compute the values for one sheet line for one day."""
        self.ensure_one()
        # Determine day type (working_day, weekend, public_holiday)
        if is_public_holiday:
            day_type = 'public_holiday'
        elif not self._work_intervals_for_day(calendar, day):
            day_type = 'weekend'
        else:
            day_type = 'working_day'

        # Planned hours: from calendar — 0 on weekends/holidays
        if day_type == 'working_day':
            planned_hours = self._planned_hours_for_day(calendar, day)
        else:
            planned_hours = 0.0

        # Worked hours: sum of (check_out - check_in) — handles multi intervals
        worked_hours = 0.0
        first_check_in = None
        for att in attendances:
            if att.check_in and att.check_out:
                duration = (att.check_out - att.check_in).total_seconds() / 3600.0
                if duration > 0:
                    worked_hours += duration
                if first_check_in is None or att.check_in < first_check_in:
                    first_check_in = att.check_in

        # Late in minutes: only on working days, compare first check-in vs shift start
        late_in_minutes = 0.0
        if day_type == 'working_day' and first_check_in and planned_hours > 0:
            shift_start = self._shift_start_for_day(calendar, day)
            if shift_start:
                check_in_dt = first_check_in
                if check_in_dt > shift_start:
                    late_in_minutes = (check_in_dt - shift_start).total_seconds() / 60.0

        # Absence: planned > 0 AND worked == 0 AND no approved leave
        is_absent = (
            day_type == 'working_day'
            and planned_hours > 0
            and worked_hours == 0
            and leave is None
        )
        is_leave = leave is not None

        # Overtime hours
        overtime_rule = self.policy_id.get_overtime_rule(day_type)
        overtime_hours = self._compute_overtime_hours(
            worked_hours, planned_hours, day_type, overtime_rule,
        )

        # Difference: worked - planned - overtime (can be negative)
        difference_hours = worked_hours - planned_hours - overtime_hours

        return {
            'date': day,
            'day_type': day_type,
            'planned_hours': planned_hours,
            'worked_hours': worked_hours,
            'overtime_hours': overtime_hours,
            'late_in_minutes': late_in_minutes,
            'is_absent': is_absent,
            'is_leave': is_leave,
            'leave_id': leave.id if leave else False,
            'difference_hours': difference_hours,
            'attendance_ids': [(6, 0, [a.id for a in attendances])],
        }

    def _work_intervals_for_day(self, calendar, day):
        """Return the working intervals of ``calendar`` for ``day``.

        Intervals are returned as (float_hour_start, float_hour_end) tuples,
        sorted by start time, following the same attendance selection rules as
        ``resource.calendar``: break periods and section lines are ignored, and
        two-weeks calendars only take the attendances of the matching week.
        """
        self.ensure_one()
        attendances = calendar.attendance_ids.filtered(
            lambda a: not a.display_type and a.day_period != 'lunch')
        if calendar.two_weeks_calendar:
            week_type = self.env['resource.calendar.attendance'].get_week_type(day)
            attendances = attendances.filtered(
                lambda a: a.week_type == str(week_type))
        attendances = attendances.filtered(
            lambda a: a.dayofweek == str(day.weekday()) and a.hour_to > a.hour_from)
        return sorted(
            (attendance.hour_from, attendance.hour_to)
            for attendance in attendances
        )

    def _planned_hours_for_day(self, calendar, day):
        """Return total planned working hours for the given day."""
        self.ensure_one()
        hours = 0.0
        for (start, end) in self._work_intervals_for_day(calendar, day):
            hours += (end - start)
        return hours

    def _shift_start_for_day(self, calendar, day):
        """Return the earliest expected check-in datetime for the day.

        ``resource.calendar.attendance.hour_from`` is a wall-clock time of the
        calendar's own timezone (see ``resource.calendar`` localize the naive
        datetime before using it), while ``hr.attendance.check_in`` is stored
        in UTC. Returning the shift start in UTC makes the comparison in
        ``_compute_line_for_day`` meaningful — comparing the naive local time
        against a UTC check-in would always report the employee as early.
        """
        self.ensure_one()
        intervals = self._work_intervals_for_day(calendar, day)
        if not intervals:
            return None
        # intervals are (float_hour_start, float_hour_end) in the calendar tz
        first_start = intervals[0][0]
        hour = int(first_start)
        minute = int((first_start - hour) * 60)
        local_start = datetime.combine(day, time(hour=hour, minute=minute))
        return self._to_utc(local_start, calendar)

    @api.model
    def _to_utc(self, naive_dt, calendar):
        """Convert a calendar-local naive datetime to a naive UTC datetime."""
        tz_name = calendar.tz or self.env.user.tz or 'UTC'
        try:
            tz = pytz.timezone(tz_name)
        except Exception:
            return naive_dt
        # pytz needs localize() for correct DST handling.
        localized = tz.localize(naive_dt, is_dst=None)
        return localized.astimezone(pytz.utc).replace(tzinfo=None)

    def _compute_overtime_hours(self, worked_hours, planned_hours,
                                day_type, overtime_rule):
        """Apply overtime rule to compute billable overtime hours."""
        self.ensure_one()
        if not overtime_rule:
            return 0.0
        if day_type == 'working_day':
            overtime_raw = max(0.0, worked_hours - planned_hours)
        else:
            # Weekend or public holiday — all worked time counts
            overtime_raw = worked_hours
        apply_after_hours = overtime_rule.apply_after_minutes / 60.0
        return max(0.0, overtime_raw - apply_after_hours)

    # ------------------------------------------------------------
    # ACTIONS (open wizards)
    # ------------------------------------------------------------
    def action_create_payslip(self):
        """Open the create-payslip wizard for this sheet."""
        self.ensure_one()
        if self.state != 'approved':
            raise UserError(_(
                "Sheet %s: payslip can only be created from an approved sheet."
            ) % self.name)
        if self.payslip_id:
            raise UserError(_(
                "Sheet %s already has a payslip (%s)."
            ) % (self.name, self.payslip_id.name))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Payslip'),
            'res_model': 'hr.attendance.create.payslip.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sheet_id': self.id,
                'default_employee_id': self.employee_id.id,
                'default_date_from': self.date_from,
                'default_date_to': self.date_to,
            },
        }

    # ------------------------------------------------------------
    # REPORT
    # ------------------------------------------------------------
    def action_print_report(self):
        return self.env.ref(
            'el_hr_attendance_sheet.action_report_hr_attendance_sheet'
        ).report_action(self)

    def action_open_payslip(self):
        """Smart-button action: open the linked payslip."""
        self.ensure_one()
        if not self.payslip_id:
            return False
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payslip'),
            'res_model': 'hr.payslip',
            'res_id': self.payslip_id.id,
            'view_mode': 'form',
            'target': 'current',
        }


class HrAttendanceSheetLine(models.Model):
    _name = 'hr.attendance.sheet.line'
    _description = 'HR Attendance Sheet Line'
    _order = 'sheet_id, date'

    sheet_id = fields.Many2one(
        'hr.attendance.sheet',
        string='Sheet',
        required=True,
        ondelete='cascade',
    )
    date = fields.Date(string='Date', required=True)
    day_type = fields.Selection([
        ('working_day', 'Working Day'),
        ('weekend', 'Weekend'),
        ('public_holiday', 'Public Holiday'),
    ], string='Day Type')
    planned_hours = fields.Float(string='Planned Hours')
    worked_hours = fields.Float(string='Worked Hours')
    overtime_hours = fields.Float(string='Overtime Hours')
    late_in_minutes = fields.Float(string='Late In (minutes)')
    is_absent = fields.Boolean(string='Absent')
    is_leave = fields.Boolean(string='On Leave')
    leave_id = fields.Many2one('hr.leave', string='Leave')
    difference_hours = fields.Float(
        string='Difference (hours)',
        help="Worked - Planned - Overtime. Can be negative.",
    )
    absence_occurrence = fields.Integer(
        string='Absence #',
        copy=False,
        help="Sequence number of this absence day inside the sheet period.",
    )
    late_occurrence = fields.Integer(
        string='Late #',
        copy=False,
        help="Sequence number of this late-in day inside the sheet period.",
    )
    late_penalty = fields.Float(
        string='Late Penalty',
        compute='_compute_line_penalty',
        store=True,
        help="Penalty hours for this day, based on the lateness step that "
             "matches both the late amount and its repetition number.",
    )
    absence_penalty_days = fields.Float(
        string='Absence Penalty (days)',
        compute='_compute_line_penalty',
        store=True,
        help="Days deducted for this absence, based on the absence step that "
             "matches both the absence and its repetition number.",
    )
    note = fields.Text(string='Note')
    attendance_ids = fields.Many2many(
        'hr.attendance',
        string='Attendances',
    )
    changed_manually = fields.Boolean(string='Changed Manually', copy=False)

    @api.depends('date')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = _("%s - %s") % (rec.sheet_id.name, rec.date)

    @api.depends('late_in_minutes', 'late_occurrence', 'is_absent',
                 'absence_occurrence', 'sheet_id.policy_id')
    def _compute_line_penalty(self):
        """Resolve the dynamic penalty for this line from the policy rules."""
        for rec in self:
            policy = rec.sheet_id.policy_id
            rec.late_penalty = 0.0
            rec.absence_penalty_days = 0.0
            if not policy:
                continue
            if rec.late_in_minutes > 0 and policy.lateness_id:
                rule = policy.lateness_id
                # late_in_minutes is always stored in minutes, so look the
                # step up in minutes directly. Going through get_step() would
                # feed hours into a rule configured with unit='minutes' and
                # match the wrong step.
                step = rule.get_step_for_minutes(
                    rec.late_in_minutes, rec.late_occurrence or 1)
                if step:
                    if step.penalty_type == 'amount':
                        rec.late_penalty = step.amount
                    elif step.penalty_type == 'hours':
                        # The step charges a flat number of penalised hours,
                        # independent of how late the employee actually was.
                        rec.late_penalty = step.penalty_hours
                    else:
                        rec.late_penalty = (
                            (rec.late_in_minutes / 60.0)
                            * step.initial_rate * step.rate
                        )
            if rec.is_absent and policy.absence_id:
                # Every absence is charged on its own tier: the 1st absence
                # uses the 1st tier's step, the 2nd absence the 2nd tier's
                # step, and so on. The step amount is taken as-is -- the
                # occurrence number only *selects* the step, it never
                # multiplies it, so repeating an absence escalates instead of
                # multiplying every earlier penalty again.
                absence_count = rec.absence_occurrence or 1
                step = policy.absence_id.get_step_for_days(
                    absence_count, absence_count,
                )
                if step:
                    if step.penalty_type == 'days':
                        rec.absence_penalty_days = step.deduction_days or 1.0
                    else:
                        rec.absence_penalty_days = step.rate

    def action_open_change_wizard(self):
        """Open the change-data wizard for this line."""
        self.ensure_one()
        if self.sheet_id.state != 'computed':
            raise UserError(_(
                "Sheet %s: data can only be changed while in Computed state."
            ) % self.sheet_id.name)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Change Attendance Data'),
            'res_model': 'hr.attendance.change.data.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sheet_line_id': self.id,
                'default_new_overtime_hours': self.overtime_hours,
                'default_new_late_in_minutes': self.late_in_minutes,
                'default_new_difference_hours': self.difference_hours,
            },
        }
