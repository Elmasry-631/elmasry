from datetime import datetime, time, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class RmAttendanceSheet(models.Model):
    _name = "rm.attendance.sheet"
    _description = "Attendance Sheet"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_from desc, employee_id"

    name = fields.Char(compute="_compute_name", store=True)
    employee_id = fields.Many2one("hr.employee", required=True, tracking=True)
    department_id = fields.Many2one("hr.department", related="employee_id.department_id", store=True)
    version_id = fields.Many2one(
        "hr.version",
        string="Contract / Employee Record",
        required=True,
        tracking=True,
        domain="[('employee_id', '=', employee_id)]",
    )
    policy_id = fields.Many2one(
        "rm.attendance.policy",
        related="version_id.attendance_policy_id",
        store=True,
        readonly=True,
    )
    date_from = fields.Date(required=True, tracking=True)
    date_to = fields.Date(required=True, tracking=True)
    state = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
        default="draft",
        required=True,
        tracking=True,
    )
    sheet_line_ids = fields.One2many("rm.attendance.sheet.line", "sheet_id", string="Daily Lines", copy=False)
    total_planned_hours = fields.Float(compute="_compute_totals", store=True)
    total_worked_hours = fields.Float(compute="_compute_totals", store=True)
    total_overtime = fields.Float(compute="_compute_totals", store=True)
    total_working_day_overtime = fields.Float(compute="_compute_totals", store=True)
    total_weekend_overtime = fields.Float(compute="_compute_totals", store=True)
    total_holiday_overtime = fields.Float(compute="_compute_totals", store=True)
    total_late_in = fields.Float(string="Total Late In (hours)", compute="_compute_totals", store=True)
    total_absence_days = fields.Integer(compute="_compute_totals", store=True)
    total_difference = fields.Float(compute="_compute_totals", store=True)
    total_leave_days = fields.Float(compute="_compute_totals", store=True)
    total_overtime_amount = fields.Float(compute="_compute_totals", store=True)
    total_late_penalty = fields.Float(compute="_compute_totals", store=True)
    total_absence_penalty = fields.Float(compute="_compute_totals", store=True)
    total_difference_amount = fields.Float(compute="_compute_totals", store=True)
    payslip_id = fields.Many2one("hr.payslip", string="Generated Payslip", readonly=True, copy=False)
    company_id = fields.Many2one("res.company", related="employee_id.company_id", store=True)

    _unique_employee_period = models.UniqueIndex(
        "(employee_id, date_from, date_to) WHERE state != 'cancelled'",
        "An attendance sheet already exists for this employee and period.",
    )

    @api.depends("employee_id", "date_from", "date_to")
    def _compute_name(self):
        for sheet in self:
            if sheet.employee_id and sheet.date_from and sheet.date_to:
                sheet.name = f"{sheet.employee_id.name} - {sheet.date_from} / {sheet.date_to}"
            else:
                sheet.name = self.env._("New Attendance Sheet")

    @api.depends(
        "sheet_line_ids.planned_hours",
        "sheet_line_ids.worked_hours",
        "sheet_line_ids.overtime_hours",
        "sheet_line_ids.overtime_type",
        "sheet_line_ids.late_in_minutes",
        "sheet_line_ids.is_absent",
        "sheet_line_ids.is_leave",
        "sheet_line_ids.difference_hours",
        "sheet_line_ids.overtime_amount",
        "sheet_line_ids.late_penalty",
        "sheet_line_ids.absence_penalty",
        "sheet_line_ids.difference_amount",
    )
    def _compute_totals(self):
        for sheet in self:
            lines = sheet.sheet_line_ids
            sheet.total_planned_hours = sum(lines.mapped("planned_hours"))
            sheet.total_worked_hours = sum(lines.mapped("worked_hours"))
            sheet.total_overtime = sum(lines.mapped("overtime_hours"))
            sheet.total_working_day_overtime = sum(lines.filtered(lambda l: l.overtime_type == "working_day").mapped("overtime_hours"))
            sheet.total_weekend_overtime = sum(lines.filtered(lambda l: l.overtime_type == "weekend").mapped("overtime_hours"))
            sheet.total_holiday_overtime = sum(lines.filtered(lambda l: l.overtime_type == "public_holiday").mapped("overtime_hours"))
            sheet.total_late_in = sum(lines.mapped("late_in_minutes")) / 60.0
            sheet.total_absence_days = len(lines.filtered("is_absent"))
            sheet.total_difference = sum(lines.mapped("difference_hours"))
            sheet.total_leave_days = len(lines.filtered("is_leave"))
            sheet.total_overtime_amount = sum(lines.mapped("overtime_amount"))
            sheet.total_late_penalty = sum(lines.mapped("late_penalty"))
            sheet.total_absence_penalty = sum(lines.mapped("absence_penalty"))
            sheet.total_difference_amount = sum(lines.mapped("difference_amount"))

    @api.onchange("employee_id", "date_from")
    def _onchange_employee_id(self):
        if self.employee_id:
            self.version_id = self._find_version(self.employee_id, self.date_from or fields.Date.today())

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        for sheet in self:
            if sheet.date_from and sheet.date_to and sheet.date_from > sheet.date_to:
                raise ValidationError(self.env._("Period start must be before period end."))

    @api.model
    def _find_version(self, employee, target_date):
        versions = self.env["hr.version"].search(
            [
                ("employee_id", "=", employee.id),
                ("active", "=", True),
                ("date_version", "<=", target_date),
            ],
            order="date_version desc",
            limit=1,
        )
        return versions or employee.version_id

    def action_calculate(self):
        for sheet in self:
            if sheet.state != "draft":
                raise UserError(self.env._("Only draft attendance sheets can be calculated."))
            sheet._generate_sheet_lines()
        return True

    def action_confirm(self):
        self.write({"state": "confirmed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_draft(self):
        self.write({"state": "draft"})

    def action_open_change_wizard(self):
        self.ensure_one()
        if self.state != "draft":
            raise UserError(self.env._("Attendance changes are only allowed in draft state."))
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Modify Attendance Line"),
            "res_model": "rm.attendance.sheet.change.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_sheet_id": self.id},
        }

    def action_create_payslip(self):
        self.ensure_one()
        if self.state != "confirmed":
            raise UserError(self.env._("Confirm the attendance sheet before creating a payslip."))
        existing = self.env["hr.payslip"].search(
            [
                ("employee_id", "=", self.employee_id.id),
                ("date_from", "=", self.date_from),
                ("date_to", "=", self.date_to),
                ("state", "!=", "cancel"),
            ],
            limit=1,
        )
        if existing:
            raise UserError(self.env._("A payslip already exists for this employee and period."))
        structure = self.env.ref("rm_hr_attendance_sheet.structure_attendance_sheet", raise_if_not_found=False)
        payslip = self.env["hr.payslip"].create(
            {
                "name": self.env._(
                    "Attendance Sheet Payslip - %(employee)s - %(date_from)s / %(date_to)s",
                    employee=self.employee_id.name,
                    date_from=self.date_from,
                    date_to=self.date_to,
                ),
                "employee_id": self.employee_id.id,
                "version_id": self.version_id.id,
                "struct_id": structure.id if structure else False,
                "date_from": self.date_from,
                "date_to": self.date_to,
                "attendance_sheet_id": self.id,
            }
        )
        self.payslip_id = payslip
        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.payslip",
            "res_id": payslip.id,
            "view_mode": "form",
        }

    def _generate_sheet_lines(self):
        self.ensure_one()
        self.sheet_line_ids.unlink()
        date_cursor = self.date_from
        attendance_by_date = self._attendance_by_date()
        leaves_by_date = self._leaves_by_date()
        holidays_by_date = self._holidays_by_date()
        absence_counter = 0
        line_values = []
        while date_cursor <= self.date_to:
            day_attendances = attendance_by_date.get(date_cursor, self.env["hr.attendance"])
            leave = leaves_by_date.get(date_cursor)
            holiday = holidays_by_date.get(date_cursor)
            intervals = self._working_intervals(date_cursor)
            planned_hours = sum(end - start for start, end in intervals)
            worked_hours = self._worked_hours(day_attendances)
            is_holiday = bool(holiday)
            is_leave = bool(leave)
            is_weekend = not intervals
            day_type = "holiday" if is_holiday else "leave" if is_leave else "weekend" if is_weekend else "working"
            late_minutes = 0.0
            if intervals and day_attendances and not is_holiday and not is_leave:
                late_minutes = self._late_minutes(date_cursor, intervals, day_attendances)
            is_absent = bool(intervals and not worked_hours and not is_holiday and not is_leave)
            if is_absent:
                absence_counter += 1
            overtime_type = False
            if is_holiday and holiday.active_for_overtime:
                overtime_type = "public_holiday"
                overtime_hours = worked_hours
            elif is_weekend:
                overtime_type = "weekend"
                overtime_hours = worked_hours
            else:
                overtime_type = "working_day"
                overtime_hours = max(worked_hours - planned_hours, 0.0)
            difference_hours = planned_hours - worked_hours
            amounts = self._calculate_amounts(overtime_hours, overtime_type, late_minutes, is_absent, absence_counter, difference_hours)
            line_values.append(
                {
                    "sheet_id": self.id,
                    "date": date_cursor,
                    "day_type": day_type,
                    "planned_hours": planned_hours,
                    "worked_hours": worked_hours,
                    "overtime_hours": overtime_hours,
                    "overtime_type": overtime_type,
                    "late_in_minutes": late_minutes,
                    "is_absent": is_absent,
                    "is_leave": is_leave,
                    "leave_id": leave.id if leave else False,
                    "public_holiday_id": holiday.id if holiday else False,
                    "difference_hours": difference_hours,
                    **amounts,
                }
            )
            date_cursor += timedelta(days=1)
        self.env["rm.attendance.sheet.line"].create(line_values)

    def _working_intervals(self, day):
        self.ensure_one()
        calendar = self.version_id.resource_calendar_id or self.employee_id.resource_calendar_id
        if not calendar:
            return []
        weekday = str(day.weekday())
        attendances = calendar.attendance_ids.filtered(lambda a: a.dayofweek == weekday and not getattr(a, "date_from", False) and not getattr(a, "date_to", False))
        return [(attendance.hour_from, attendance.hour_to) for attendance in attendances]

    def _attendance_by_date(self):
        self.ensure_one()
        dt_from = datetime.combine(self.date_from, time.min)
        dt_to = datetime.combine(self.date_to, time.max)
        attendances = self.env["hr.attendance"].search(
            [
                ("employee_id", "=", self.employee_id.id),
                ("check_in", "<=", dt_to),
                ("check_out", ">=", dt_from),
            ]
        )
        result = {}
        for attendance in attendances.filtered("check_out"):
            current = max(attendance.check_in.date(), self.date_from)
            last = min(attendance.check_out.date(), self.date_to)
            while current <= last:
                result.setdefault(current, self.env["hr.attendance"])
                result[current] |= attendance
                current += timedelta(days=1)
        return result

    def _leaves_by_date(self):
        self.ensure_one()
        dt_from = datetime.combine(self.date_from, time.min)
        dt_to = datetime.combine(self.date_to, time.max)
        leaves = self.env["hr.leave"].search(
            [
                ("employee_id", "=", self.employee_id.id),
                ("state", "=", "validate"),
                ("date_from", "<=", dt_to),
                ("date_to", ">=", dt_from),
            ]
        )
        result = {}
        for leave in leaves:
            current = max(leave.date_from.date(), self.date_from)
            last = min(leave.date_to.date(), self.date_to)
            while current <= last:
                result.setdefault(current, leave)
                current += timedelta(days=1)
        return result

    def _holidays_by_date(self):
        self.ensure_one()
        dt_from = datetime.combine(self.date_from, time.min)
        dt_to = datetime.combine(self.date_to, time.max)
        holidays = self.env["resource.calendar.leaves"].search(
            [
                ("rm_public_holiday", "=", True),
                ("date_from", "<=", dt_to),
                ("date_to", ">=", dt_from),
                ("company_id", "in", [False, self.company_id.id]),
            ]
        )
        result = {}
        for holiday in holidays:
            if not holiday.applies_to_employee(self.employee_id):
                continue
            current = max(holiday.date_from.date(), self.date_from)
            last = min(holiday.date_to.date(), self.date_to)
            while current <= last:
                result.setdefault(current, holiday)
                current += timedelta(days=1)
        return result

    def _worked_hours(self, attendances):
        total = 0.0
        for attendance in attendances.filtered("check_out"):
            total += (attendance.check_out - attendance.check_in).total_seconds() / 3600.0
        return total

    def _late_minutes(self, day, intervals, attendances):
        first_check_in = min(attendances.filtered("check_in").mapped("check_in"))
        planned_start_hour = min(start for start, _end in intervals)
        planned_start = datetime.combine(day, time.min) + timedelta(hours=planned_start_hour)
        return max((first_check_in - planned_start).total_seconds() / 60.0, 0.0)

    def _calculate_amounts(self, overtime_hours, overtime_type, late_minutes, is_absent, absence_count, difference_hours):
        self.ensure_one()
        hourly_rate = self._hourly_rate()
        daily_rate = self._daily_rate()
        overtime_amount = 0.0
        late_penalty = 0.0
        absence_penalty = 0.0
        difference_amount = max(difference_hours, 0.0) * hourly_rate
        policy = self.policy_id
        if policy:
            overtime_rules = policy.overtime_rule_ids.filtered(lambda r: r.active and r.ot_type == overtime_type).sorted("apply_after", reverse=True)
            overtime_minutes = overtime_hours * 60.0
            for rule in overtime_rules[:1]:
                counted_hours = max((overtime_minutes - rule.apply_after) / 60.0, 0.0)
                overtime_amount = counted_hours * hourly_rate * rule.rate
            for rule in policy.lateness_rule_ids.filtered("active")[:1]:
                late_penalty = rule.get_penalty(late_minutes, hourly_rate)
            if is_absent:
                for rule in policy.absence_rule_ids.filtered("active")[:1]:
                    absence_penalty = rule.get_penalty(absence_count, daily_rate)
                    break
                if not absence_penalty:
                    absence_penalty = daily_rate
        return {
            "overtime_amount": overtime_amount,
            "late_penalty": late_penalty,
            "absence_penalty": absence_penalty,
            "difference_amount": difference_amount,
        }

    def _daily_rate(self):
        self.ensure_one()
        return (self.version_id.wage or 0.0) / 30.0

    def _hourly_rate(self):
        self.ensure_one()
        return self._daily_rate() / 8.0 if self._daily_rate() else 0.0


class RmAttendanceSheetLine(models.Model):
    _name = "rm.attendance.sheet.line"
    _description = "Attendance Sheet Line"
    _order = "date"
    _rec_name = "name"

    name = fields.Char(compute="_compute_name", store=True)
    sheet_id = fields.Many2one("rm.attendance.sheet", required=True, ondelete="cascade")
    employee_id = fields.Many2one(related="sheet_id.employee_id", store=True)
    date = fields.Date(required=True)
    day_name = fields.Char(compute="_compute_day_name", store=True)
    day_type = fields.Selection(
        [
            ("working", "Working Day"),
            ("weekend", "Weekend"),
            ("holiday", "Public Holiday"),
            ("leave", "Leave"),
        ],
        default="working",
        required=True,
    )
    planned_hours = fields.Float()
    worked_hours = fields.Float()
    overtime_hours = fields.Float()
    overtime_type = fields.Selection(
        [
            ("working_day", "Working Day"),
            ("weekend", "Weekend"),
            ("public_holiday", "Public Holiday"),
        ],
    )
    late_in_minutes = fields.Float()
    is_absent = fields.Boolean()
    is_leave = fields.Boolean()
    leave_id = fields.Many2one("hr.leave", string="Leave")
    public_holiday_id = fields.Many2one("resource.calendar.leaves", string="Public Holiday")
    difference_hours = fields.Float()
    overtime_amount = fields.Float()
    late_penalty = fields.Float()
    absence_penalty = fields.Float()
    difference_amount = fields.Float()
    change_note = fields.Text()
    changed_by = fields.Many2one("res.users", readonly=True)
    changed_date = fields.Datetime(readonly=True)

    @api.depends("employee_id", "date")
    def _compute_name(self):
        for line in self:
            if line.employee_id and line.date:
                line.name = f"{line.employee_id.name} - {line.date}"
            elif line.date:
                line.name = str(line.date)
            else:
                line.name = self.env._("Attendance Sheet Line")

    @api.depends("date")
    def _compute_day_name(self):
        for line in self:
            line.day_name = line.date.strftime("%A") if line.date else False
