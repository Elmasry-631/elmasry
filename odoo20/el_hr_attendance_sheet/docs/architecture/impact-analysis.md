# Impact Analysis — el_hr_attendance_sheet

> Impact of every change on the Odoo 20 system.

## Extended Models

### hr.contract
- **Change:** Add `attendance_policy_id` (Many2one → `hr.attendance.policy`)
- **Impact:** Optional field. No behavioral change to existing flows.
- **Risk:** LOW — read-only field unless explicitly referenced.
- **Migration:** None — additive.

### hr.payslip
- **Change:** Add `attendance_sheet_id` (Many2one → `hr.attendance.sheet`), `overtime_hours`, `late_in_hours`, `absence_days`, `difference_hours` (computed from sheet).
- **Impact:** New fields available to salary rules. Existing salary structures unaffected.
- **Risk:** LOW — computed fields are lazy.
- **Migration:** None — additive.

## New Models

| Model | Risk | Reason |
|---|---|---|
| `hr.attendance.public.holiday` | LOW | Standalone + new menu, no cross-coupling |
| `hr.attendance.rule.overtime` | LOW | Configuration table, no runtime impact |
| `hr.attendance.rule.lateness` + step | LOW | Configuration table |
| `hr.attendance.rule.absence` + step | LOW | Configuration table |
| `hr.attendance.policy` | LOW | Aggregator of rules |
| `hr.attendance.sheet` + line | MEDIUM | Core computation; depends on hr.attendance + resource.calendar + hr.holidays |
| `hr.attendance.sheet.batch` + line | MEDIUM | Generates many sheets; performance concern |
| Wizards (3) | LOW | Ephemeral |

## Performance Considerations

1. **Sheet computation** (`action_compute`) iterates over every day in the period and queries `hr.attendance` for that day. For long periods (e.g. monthly), this is N queries. Optimization: prefetch all attendances for the period with `search_read` in one query, then group by date in Python.

2. **Batch generation** creates one sheet per employee in the department. For large departments (100+ employees), this is heavy. Recommendation: run via cron if department > 50 employees.

3. **Salary rule evaluation** during payslip compute reads sheet data. Add `store=True` on the computed fields `overtime_hours` etc. on `hr.payslip` to avoid re-querying on every rule.

## Uninstall Safety

- All new models are isolated. Uninstalling the module drops the tables cleanly.
- Extended fields on hr.contract / hr.payslip are dropped with the module (Odoo standard behavior).
- Salary rules + structure created via data XML: Odoo will mark them as noupdate=True (via `noupdate="1"` in the data file) to prevent duplicate creation on reinstall.

## Cross-Module Compatibility

| Module | Compatibility |
|---|---|
| `hr_attendance` | ✅ Reads `hr.attendance` records; no writes |
| `hr_holidays` | ✅ Reads approved leaves; no writes |
| `hr_payroll` | ✅ Adds salary rules + structure; standard mechanism |
| `hr` | ✅ Adds field to `hr.contract`; standard extension |
| `resource` | ✅ Reads `resource.calendar` for planned hours; no writes |
| `mail` | ✅ Standard chatter on sheet + policy |
| `calendar` | ✅ Dependency pulled by resource; used for date math |
