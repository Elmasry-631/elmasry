# Views — el_hr_attendance_sheet

> View layouts, button maps, and inherited views.

## Custom Views (per model)

### hr.attendance.public.holiday
- **List:** name, date_from, date_to, state (badge), company_id
- **Form:** header (Activate / Cancel / Reset to Draft buttons + statusbar) → group (name, dates, company) → notebook (lines: employee/dept/tags)
- **Search:** name, date_from, date_to + filters (Active, Draft) + group by state

### hr.attendance.rule.overtime
- **List:** name, type, apply_after_minutes, rate, active (toggle)
- **Form:** name, type, apply_after_minutes, rate, active, company

### hr.attendance.rule.lateness
- **Form:** name + active + notebook page with editable step list (from_minutes, to_minutes, penalty_type, rate/initial_rate/amount)

### hr.attendance.rule.absence
- **Form:** same pattern as lateness but with from_days/to_days/rate

### hr.attendance.policy
- **List:** name, all 3 overtime rules, lateness, absence, active
- **Form:** name + active + company + 2 notebook pages (Overtime Rules / Lateness & Absence) + chatter

### hr.attendance.sheet (most complex)
- **Kanban:** grouped by state, shows employee, period, OT/late/absence totals
- **List:** name, employee, dates, totals (with sum), state badge
- **Form:** header with 7 buttons (Compute, Approve, Create Payslip, Done, Cancel, Reset, Print) + statusbar → button box (payslip smart button) → group (name, employee, dates, contract, policy, company) → notebook (Attendance Lines / Summary) + chatter
- **Pivot:** employee × month with OT, late, absence, diff as measures
- **Graph:** bar chart OT per employee
- **Search:** 5 state filters + Has Overtime + Has Absence + group by state/employee/policy

### hr.attendance.sheet.batch
- **List:** name, department, dates, state badge
- **Form:** header with 4 buttons (Generate, Done, Cancel, Reset) + statusbar → group → batch lines (employee, sheet)

## Inherited Views

### hr.contract (extend form)
**XPath:** before `notes` field
**Adds:** group "Attendance Policy" with `attendance_policy_id` field

### hr.payslip (extend form)
**XPath:** inside `notebook`
**Adds:** page "Attendance" (invisible when no attendance_sheet_id) showing:
- attendance_sheet_id (readonly)
- Computed inputs group: overtime_hours, late_in_hours, absence_days, difference_hours

## Wizard Views

### Change Data Wizard
- sheet_line_id (readonly)
- new_overtime_hours, new_late_in_minutes, new_difference_hours
- reason (required, textarea)
- Footer: Apply Change / Cancel

### Batch Wizard
- department_id, date_from, date_to, company_id
- employee_ids (optional, many2many tags, filtered by department)
- Footer: Create Batch / Cancel

### Create Payslip Wizard
- sheet_id, employee_id, contract_id (all readonly)
- date_from, date_to (readonly)
- struct_id (default = Attendance Structure)
- Footer: Create Payslip / Cancel

## Menu Hierarchy

```
HR
└── Attendance (existing hr_attendance menu)
    └── Attendance Sheets (new)
        ├── Attendance Sheets      → action_hr_attendance_sheet
        ├── Batches                 → action_hr_attendance_sheet_batch
        └── Configuration
            ├── Public Holidays     → action_hr_attendance_public_holiday
            ├── Rules
            │   ├── Overtime Rules  → action_hr_attendance_rule_overtime
            │   ├── Lateness Rules  → action_hr_attendance_rule_lateness
            │   └── Absence Rules   → action_hr_attendance_rule_absence
            └── Attendance Policies → action_hr_attendance_policy
```

## Button → Method Map

| View | Button | Method |
|------|--------|--------|
| sheet form | Compute | action_compute |
| sheet form | Approve | action_approve |
| sheet form | Create Payslip | action_create_payslip (wizard) |
| sheet form | Set to Done | action_done |
| sheet form | Cancel | action_cancel |
| sheet form | Reset to Draft | action_draft |
| sheet form | Print | action_print_report |
| sheet form (button box) | Payslip | action_open_payslip |
| sheet line | Change | action_open_change_wizard (wizard) |
| batch form | Generate Sheets | action_generate_sheets |
| batch form | Set to Done | action_done |
| batch form | Cancel | action_cancel |
| batch form | Reset to Draft | action_draft |
| public.holiday form | Activate | action_activate |
| public.holiday form | Cancel | action_cancel |
| public.holiday form | Reset to Draft | action_draft |
| change.data.wizard | Apply Change | action_apply |
| batch.wizard | Create Batch | action_create_batch |
| create.payslip.wizard | Create Payslip | action_create_payslip |

---

*Author: Ibrahim Elmasry*
