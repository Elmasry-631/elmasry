# GAP Analysis — el_hr_attendance_sheet

> Functional gap analysis: what Odoo 19 standard covers vs what this module adds.

## Requirements vs Odoo Standard

| Requirement | Odoo 19 Standard Coverage | Gap | Module Solution |
|---|---|---|---|
| Public holidays definition | `resource.calendar.leaves` (resource module) | No employee/tag selection; no active flag for overtime calc | New `hr.attendance.public.holiday` model with employee/dept/tag scoping |
| Overtime calculation per day | `hr.attendance` records check-in/out only | No overtime computation, no rate per type | `hr.attendance.rule.overtime` with 3 types (working/weekend/holiday) + rate + apply_after |
| Lateness calculation | None | No multi-step lateness penalty matrix | `hr.attendance.rule.lateness` + `.step` with from_minutes/to_minutes + rate/amount |
| Absence calculation | `hr.holidays` covers leaves; not unexcused absence | No absence detection from attendance gaps | `hr.attendance.rule.absence` + `.step` with from_days/to_days + rate |
| Policy assignment | None | No way to attach rules to employee | `hr.attendance.policy` linked to `hr.contract.attendance_policy_id` |
| Attendance sheet per period | `hr.attendance` shows raw check-in/out | No aggregated sheet | `hr.attendance.sheet` + `.line` with planned/actual/overtime/late/absence per day |
| Manual data correction | None | No wizard to override computed values | `hr.attendance.change.data.wizard` records reason note + updates line |
| Payslip integration | `hr_payroll` salary rules can read inputs | No standard inputs for overtime/late/absence | Salary rules + structure data files + `hr.payslip.attendance_sheet_id` link |
| Batch by department | None | No batch generation | `hr.attendance.sheet.batch` + `.batch.line` + wizard |
| Working schedule reuse | `resource.calendar` (via hr.contract.resource_calendar_id) | OK | Reuse — no new model |

## GAP Decision

**Build vs Reuse:**
- Reuse `resource.calendar` for working hours (no new model)
- Reuse `hr.holidays` for approved leaves (no new model)
- Reuse `hr.attendance` for raw check-in/out (extend, not replace)
- Build new `hr.attendance.public.holiday` (more flexible than `resource.calendar.leaves`)
- Build new `hr.attendance.sheet` (no equivalent in standard)

## Affected Standard Modules

| Module | Change Type | Reason |
|---|---|---|
| `hr.contract` | Extension (add `attendance_policy_id` field) | Link policy to contract |
| `hr.payslip` | Extension (add `attendance_sheet_id` + computed inputs) | Read attendance data on payslip |
| `hr_payroll` | Data: salary rules + structure | 4 rules + 1 structure for attendance inputs |
