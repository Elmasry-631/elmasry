# API Reference — el_hr_attendance_sheet

> Public Python API exposed by this module (for use by other modules or scripts).

## Model: hr.attendance.sheet

### Public Methods

#### `action_compute(self)`
Runs the computation engine. Validates contract + policy exist, generates daily lines for the entire period, sets state to `computed`.

**Raises:** `UserError` if state not in (draft, computed), no contract, no policy.

#### `action_approve(self)`
Approves a computed sheet. Requires lines to exist.

#### `action_done(self)`
Sets an approved sheet to done. Requires `payslip_id` to be set.

#### `action_cancel(self)`
Cancels a sheet from any non-terminal state. Refuses if linked payslip is done.

#### `action_draft(self)`
Resets a cancelled sheet back to draft.

#### `action_create_payslip(self)`
Returns an action dict that opens the `hr.attendance.create.payslip.wizard` form, pre-filled with this sheet's data.

#### `action_print_report(self)`
Returns the QWeb PDF report action for this sheet.

#### `action_open_payslip(self)`
Smart-button action — opens the linked payslip form, if any.

### Internal Methods (can be called from inheritors)

#### `_run_computation(self)`
The main per-day pipeline. See `docs/architecture/data-flow.md` for the algorithm.

#### `_fetch_attendances_by_day(self) → dict`
Returns `{date: [hr.attendance, ...]}` for the sheet's period.

#### `_fetch_leaves_by_day(self) → dict`
Returns `{date: hr.leave}` for approved leaves overlapping the sheet's period.

#### `_fetch_public_holidays_by_day(self) → set`
Returns `{date, ...}` for public holidays applicable to this employee.

#### `_compute_line_for_day(self, day, calendar, attendances, leave, is_public_holiday) → dict`
Returns the vals dict for one `hr.attendance.sheet.line` record.

#### `_planned_hours_for_day(self, calendar, day) → float`
Returns total planned hours from the resource calendar for the given day.

#### `_shift_start_for_day(self, calendar, day) → datetime`
Returns the earliest expected check-in datetime for the day.

#### `_compute_overtime_hours(self, worked_hours, planned_hours, day_type, overtime_rule) → float`
Applies the overtime rule to compute billable overtime hours. On working days: `max(0, worked - planned) - apply_after`. On weekend/holiday: `worked - apply_after`.

## Model: hr.attendance.policy

#### `get_overtime_rule(self, day_type) → hr.attendance.rule.overtime`
Returns the overtime rule for the given day type (`'working_day' | 'weekend' | 'public_holiday'`).

## Model: hr.attendance.rule.lateness

#### `get_step_for_minutes(self, late_minutes) → hr.attendance.rule.lateness.step`
Returns the matching step for the given late minutes. Returns empty recordset if no match.

## Model: hr.attendance.rule.absence

#### `get_step_for_days(self, absence_days) → hr.attendance.rule.absence.step`
Returns the matching step for the given absence days count. Returns empty recordset if no match.

## Model: hr.attendance.public.holiday

#### `is_employee_on_holiday(self, employee, date) → bool`
Returns True if the given employee is on this public holiday on the given date.

## Extended Model: hr.contract

New field: `attendance_policy_id` (Many2one → hr.attendance.policy)

## Extended Model: hr.payslip

New computed fields (stored):
- `overtime_hours` (Float) — from `attendance_sheet_id.total_overtime`
- `late_in_hours` (Float) — from `attendance_sheet_id.total_late_in / 60`
- `absence_days` (Float) — from `attendance_sheet_id.total_absence`
- `difference_hours` (Float) — from `attendance_sheet_id.total_difference`

These fields are available as `payslip.overtime_hours` etc. in salary rule Python compute code.

## Salary Rules Python API

The 4 salary rules shipped with the module use the following pattern:

```python
result = 0.0
if payslip.attendance_sheet_id and payslip.overtime_hours:
    contract = payslip.contract_id
    hourly_rate = contract.wage / 240.0 if contract.wage else 0.0
    policy = contract.attendance_policy_id
    rate = 1.5  # default
    if policy and policy.overtime_working_id:
        rate = policy.overtime_working_id.rate
    result = payslip.overtime_hours * hourly_rate * rate
```

Available variables in salary rule compute:
- `payslip` — the hr.payslip record
- `payslip.attendance_sheet_id` — linked sheet (or empty)
- `payslip.overtime_hours` / `late_in_hours` / `absence_days` / `difference_hours`
- `contract` — the hr.contract record
- `contract.attendance_policy_id` — the policy
- `policy.get_overtime_rule(day_type)` — get OT rule
- `policy.lateness_id.get_step_for_minutes(minutes)` — get lateness step
- `policy.absence_id.get_step_for_days(days)` — get absence step

## Reports

### `el_hr_attendance_sheet.action_report_hr_attendance_sheet`
- **Type:** QWeb PDF
- **Model:** hr.attendance.sheet
- **Binding:** Print menu on sheet form
- **Output:** `AS - {employee_name} - {sheet_name}.pdf`

---

*Author: Ibrahim Elmasry*
