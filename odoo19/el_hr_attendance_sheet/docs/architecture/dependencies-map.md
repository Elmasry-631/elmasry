# Dependencies Map — el_hr_attendance_sheet

> Module dependencies and cross-module touchpoints.

## Direct Dependencies (in __manifest__.py `depends`)

| Module | Reason |
|---|---|
| `hr_attendance` | Reads `hr.attendance` records for check-in/out times |
| `hr` | Extends `hr.contract` to add `attendance_policy_id` |
| `hr_payroll` | Extends `hr.payslip`; creates salary rules + structure |
| `hr_holidays` | Reads approved `hr.leave` records to detect leaves |
| `mail` | Provides `mail.thread` + `mail.activity.mixin` |
| `calendar` | Required by `resource` (transitive) for date math |

## Transitive Dependencies

| Module | Required By |
|---|---|
| `resource` | `hr` (for `resource.calendar` on contract) |
| `base` | All modules |
| `web` | All UI modules |

## Cross-Module Touchpoints

### Reads (no writes to other modules' tables)

| Source Model | Target Model | Field Used | Read When |
|---|---|---|---|
| `hr.attendance.sheet` | `hr.attendance` | employee_id, check_in, check_out | Sheet computation |
| `hr.attendance.sheet` | `hr.leave` | employee_id, date_from, date_to, state | Sheet computation |
| `hr.attendance.sheet` | `hr.attendance.public.holiday` | date_from, date_to, line_ids | Sheet computation |
| `hr.attendance.sheet` | `resource.calendar` | _get_day_work_hours() | Sheet computation |
| `hr.attendance.sheet` | `hr.contract` | wage, resource_calendar_id, attendance_policy_id | Sheet computation + payslip |
| `hr.attendance.sheet.line` | `hr.attendance` | (same as above) | Per-day computation |

### Writes (extensions via _inherit)

| Extended Model | Field Added | Default | Notes |
|---|---|---|---|
| `hr.contract` | `attendance_policy_id` | False | Optional — sheet computation fails with UserError if not set |
| `hr.payslip` | `attendance_sheet_id` | False | Set when payslip created from sheet |
| `hr.payslip` | `overtime_hours` | 0.0 | Computed from sheet, store=True |
| `hr.payslip` | `late_in_hours` | 0.0 | Computed from sheet, store=True |
| `hr.payslip` | `absence_days` | 0.0 | Computed from sheet, store=True |
| `hr.payslip` | `difference_hours` | 0.0 | Computed from sheet, store=True |

### Data Records Created (in this module's data files)

| Record | Module | Purpose |
|---|---|---|
| Salary Rule: `OVERT` (Overtime) | hr_payroll | Compute overtime amount from `overtime_hours * wage / 240 * rate` |
| Salary Rule: `LATE` (Lateness) | hr_payroll | Compute lateness deduction from `late_in_hours * penalty_rate * wage` |
| Salary Rule: `ABS` (Absence) | hr_payroll | Compute absence deduction from `absence_days * wage / 30 * rate` |
| Salary Rule: `DIFF` (Difference Time) | hr_payroll | Compute difference time from `difference_hours * wage / 240` |
| Salary Structure: `Attendance Structure` | hr_payroll | References the 4 rules above + standard NET/GROSS |
| Sequence: `Attendance Sheet` | ir.sequence | Sheet name = `AS/%(year)s/%(month)s/####` |
| Sequence: `Attendance Sheet Batch` | ir.sequence | Batch name = `ASB/%(year)s/####` |
| Sequence: `Attendance Policy` | ir.sequence | Policy name = `POL/####` |

## Version Compatibility

| Odoo Version | Compatible | Notes |
|---|---|---|
| 19.0 | ✅ Target | Uses Odoo 19 APIs (models.Constraint, Domain, etc.) |
| 18.0 | ⚠️ Likely compatible | Minor differences in OWL — not used here |
| 17.0 and below | ❌ Not tested | `<list>` tag introduced in 17, but other APIs differ |

## Install Order

1. Install `hr_payroll` (pulls `hr`, `hr_attendance`, `hr_holidays`, `mail`, `calendar`, `resource`)
2. Install `el_hr_attendance_sheet`

## Uninstall Order

1. Uninstall `el_hr_attendance_sheet` (drops all new models + extended fields + data records)
2. (Optional) Uninstall `hr_payroll` if no longer needed
