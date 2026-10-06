# Models Reference — el_hr_attendance_sheet

> All 17 models in the module, with field/method tables.

## 1. hr.attendance.public.holiday

**Purpose:** Define public holidays that affect overtime calculation, scoped to specific employees/departments/tags.

**Inherits:** `mail.thread`, `mail.activity.mixin`

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Holiday name (e.g. "National Day") |
| date_from | Date | Start date (inclusive) |
| date_to | Date | End date (inclusive) |
| active | Boolean | Soft-delete flag |
| state | Selection | draft / active / cancelled |
| line_ids | One2many → hr.attendance.public.holiday.line | Lines defining who is on holiday |
| company_id | Many2one → res.company | Company (multi-company) |

**Methods:**
- `action_activate()` — set state to active (requires lines)
- `action_cancel()` — set state to cancelled
- `action_draft()` — reset to draft (only from cancelled)
- `is_employee_on_holiday(employee, date)` — check if employee is on holiday

## 2. hr.attendance.public.holiday.line

| Field | Type | Description |
|-------|------|-------------|
| holiday_id | Many2one → hr.attendance.public.holiday | Parent holiday |
| employee_id | Many2one → hr.employee | Specific employee (optional) |
| department_id | Many2one → hr.department | Department scope (optional) |
| employee_tag_ids | Many2many → hr.employee.category | Tag-based scope (optional) |

**Methods:**
- `matches_employee(employee)` — True if this line applies to the employee

## 3. hr.attendance.rule.overtime

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Rule name |
| type | Selection | working_day / weekend / public_holiday |
| apply_after_minutes | Float | Overtime counted only after this many minutes |
| rate | Float | Multiplier on hourly rate (1.5 = 150%) |
| active | Boolean | Active flag |
| company_id | Many2one → res.company | Company |

**Constraint:** `unique(type, company_id)` — one rule per type per company.

## 4. hr.attendance.rule.lateness

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Rule name |
| active | Boolean | Active flag |
| step_ids | One2many → hr.attendance.rule.lateness.step | Penalty steps |
| company_id | Many2one → res.company | Company |

**Methods:** `get_step_for_minutes(late_minutes)` — returns matching step.

## 5. hr.attendance.rule.lateness.step

| Field | Type | Description |
|-------|------|-------------|
| lateness_id | Many2one → hr.attendance.rule.lateness | Parent rule |
| from_minutes | Float | Step lower bound (inclusive) |
| to_minutes | Float | Step upper bound (inclusive) |
| penalty_type | Selection | rate / amount |
| rate | Float | Multiplier on initial rate (when type=rate) |
| initial_rate | Float | Base rate the multiplier applies to |
| amount | Float | Fixed amount deduction (when type=amount) |

## 6. hr.attendance.rule.absence + 7. hr.attendance.rule.absence.step

Same pattern as lateness rule, but using days instead of minutes.

| Field | Type | Description |
|-------|------|-------------|
| from_days | Integer | Step lower bound (inclusive) |
| to_days | Integer | Step upper bound (inclusive) |
| rate | Float | Multiplier on daily wage |

## 8. hr.attendance.policy

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Policy name |
| active | Boolean | Active flag |
| company_id | Many2one → res.company | Company |
| overtime_working_id | Many2one → hr.attendance.rule.overtime | OT rule for working days |
| overtime_weekend_id | Many2one → hr.attendance.rule.overtime | OT rule for weekends |
| overtime_holiday_id | Many2one → hr.attendance.rule.overtime | OT rule for public holidays |
| lateness_id | Many2one → hr.attendance.rule.lateness | Lateness rule |
| absence_id | Many2one → hr.attendance.rule.absence | Absence rule |
| contract_ids | One2many → hr.contract | Contracts using this policy |

**Methods:** `get_overtime_rule(day_type)` — returns the OT rule for the given day type.

## 9. hr.attendance.sheet

The main transactional model.

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Sequence reference (AS/YYYY/MM/####) |
| employee_id | Many2one → hr.employee | Employee |
| date_from | Date | Period start |
| date_to | Date | Period end |
| contract_id | Many2one → hr.contract | Active contract (auto-computed) |
| policy_id | Many2one → hr.attendance.policy | Policy (related from contract) |
| state | Selection | draft / computed / approved / done / cancelled |
| company_id | Many2one → res.company | Company |
| line_ids | One2many → hr.attendance.sheet.line | Daily lines |
| total_overtime | Float | Sum of overtime_hours |
| total_late_in | Float | Sum of late_in_minutes |
| total_absence | Float | Count of absent days |
| total_difference | Float | Sum of difference_hours |
| total_planned | Float | Sum of planned_hours |
| total_worked | Float | Sum of worked_hours |
| payslip_id | Many2one → hr.payslip | Linked payslip |
| batch_id | Many2one → hr.attendance.sheet.batch | Parent batch |

**Methods:** `action_compute`, `action_approve`, `action_done`, `action_cancel`, `action_draft`, `action_create_payslip`, `action_print_report`, `action_open_payslip`, plus internal `_run_computation`, `_fetch_attendances_by_day`, `_fetch_leaves_by_day`, `_fetch_public_holidays_by_day`, `_compute_line_for_day`, `_planned_hours_for_day`, `_shift_start_for_day`, `_compute_overtime_hours`.

## 10. hr.attendance.sheet.line

| Field | Type | Description |
|-------|------|-------------|
| sheet_id | Many2one → hr.attendance.sheet | Parent sheet |
| date | Date | Day |
| day_type | Selection | working_day / weekend / public_holiday |
| planned_hours | Float | Planned hours from calendar |
| worked_hours | Float | Actual worked hours (sum of intervals) |
| overtime_hours | Float | Billable overtime hours |
| late_in_minutes | Float | Minutes late on first check-in |
| is_absent | Boolean | True if absent without leave |
| is_leave | Boolean | True if on approved leave |
| leave_id | Many2one → hr.leave | Linked leave |
| difference_hours | Float | Worked - Planned - Overtime |
| attendance_ids | Many2many → hr.attendance | Linked raw attendances |
| note | Text | Manual change notes |
| changed_manually | Boolean | True if values were overridden |

**Methods:** `action_open_change_wizard` — opens the change-data wizard.

## 11. hr.attendance.sheet.batch + 12. hr.attendance.sheet.batch.line

Batch model that generates one sheet per employee in a department. See state machine doc.

## 13-15. Wizards

| Wizard | Purpose |
|--------|---------|
| hr.attendance.change.data.wizard | Override overtime/late/diff on a single line with reason |
| hr.attendance.sheet.batch.wizard | Generate a batch by department + period |
| hr.attendance.create.payslip.wizard | Create a payslip from an approved sheet |

## 16. hr.contract (extended)

Added field: `attendance_policy_id` (Many2one → hr.attendance.policy).

## 17. hr.payslip (extended)

Added fields:
- `attendance_sheet_id` (Many2one → hr.attendance.sheet)
- `overtime_hours` (Float, computed, stored)
- `late_in_hours` (Float, computed, stored)
- `absence_days` (Float, computed, stored)
- `difference_hours` (Float, computed, stored)

These computed fields feed the 4 salary rules (OVERT, LATE, ABS, DIFF) defined in the Attendance Salary Structure.

---

*Author: Ibrahim Elmasry*
