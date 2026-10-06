# Testing — el_hr_attendance_sheet

> Test plan for the HR Attendance Sheet And Policies module.
> Execute these tests on a running Odoo 20 instance after installing the module.

## 1. State Machine Test Plan — hr.attendance.sheet

| # | Test Case | Steps | Expected Result |
|---|-----------|-------|-----------------|
| 1 | Create sheet | Create new sheet for an employee with a valid date range | State = draft, name = AS/YYYY/MM/#### |
| 2 | Compute sheet | Click "Compute" on a draft sheet | State = computed, lines generated |
| 3 | Approve sheet | Click "Approve" on a computed sheet | State = approved |
| 4 | Create payslip | Click "Create Payslip" on approved sheet → select structure → confirm | Payslip created, sheet state = done |
| 5 | Cancel from computed | Click "Cancel" on a computed sheet | State = cancelled |
| 6 | Reset to draft | Click "Reset to Draft" on cancelled sheet | State = draft |
| 7 | Cancel from done (negative) | Try "Cancel" on a done sheet with linked payslip | UserError raised |
| 8 | Compute without policy | Try to compute a sheet whose contract has no policy | UserError raised |
| 9 | Compute without contract | Try to compute a sheet for an employee with no contract | UserError raised |
| 10 | Overlapping sheets | Try to create a second sheet for the same employee/period | UserError raised |

## 2. State Machine Test Plan — hr.attendance.sheet.batch

| # | Test Case | Steps | Expected Result |
|---|-----------|-------|-----------------|
| 1 | Create batch | Create new batch with department + date range | State = draft, name = ASB/YYYY/#### |
| 2 | Generate sheets | Click "Generate Sheets" | State = confirmed, one sheet per employee created |
| 3 | Done batch | Approve all child sheets first, then click "Set to Done" | State = done |
| 4 | Cancel batch | Click "Cancel" | State = cancelled, child sheets also cancelled |
| 5 | Generate from non-draft | Try to generate sheets from a confirmed batch | UserError raised |

## 3. State Machine Test Plan — hr.attendance.public.holiday

| # | Test Case | Steps | Expected Result |
|---|-----------|-------|-----------------|
| 1 | Create holiday | Create new public holiday with dates | State = draft |
| 2 | Activate with lines | Add a line + click "Activate" | State = active |
| 3 | Activate without lines | Try to activate without any lines | UserError raised |
| 4 | Cancel active holiday | Click "Cancel" on active holiday | State = cancelled, active = False |
| 5 | Reset to draft | Click "Reset to Draft" on cancelled | State = draft |

## 4. Computation Engine Test Plan

| # | Test Case | Setup | Expected Result |
|---|-----------|-------|-----------------|
| 1 | Working day overtime | Calendar: 8h/day Mon-Fri. Attendance: 10h on Monday. | planned=8, worked=10, overtime=2 |
| 2 | Weekend work | Calendar: 0h Sat/Sun. Attendance: 4h on Saturday. | planned=0, worked=4, overtime=4 |
| 3 | Public holiday work | Public holiday defined. Attendance: 6h. | planned=0, worked=6, overtime=6 (rate from holiday rule) |
| 4 | Lateness detection | Calendar: starts 09:00. Attendance: check-in 09:30. | late_in_minutes=30 |
| 5 | Absence detection | Calendar: 8h Mon-Fri. No attendance on Monday. No leave. | is_absent=True |
| 6 | Approved leave day | Calendar: 8h. Leave approved for the day. No attendance. | is_leave=True, is_absent=False |
| 7 | Multi-interval attendance | 2 check-in/out pairs on same day: 9-13 + 14-18 | worked=8 (sum of both intervals) |
| 8 | Apply-after overtime | Rule: apply_after_minutes=30. Worked 10h, planned 8h. | overtime=1.5 (10-8-0.5) |
| 9 | Difference negative | Worked 6h, planned 8h, no overtime | difference=-2 |
| 10 | Computed totals | 5 days, OT: 2+1+0+3+1 | total_overtime=7 |

## 5. Permission Test Plan

| # | Test Case | User | Expected |
|---|-----------|------|----------|
| 1 | Manager CRUD | Manager group | Full create/read/write/delete |
| 2 | Officer CRUD (no delete) | Officer group | Create/read/write OK, delete denied |
| 3 | User read-only | User group | Read only, no write/create |
| 4 | User sees own sheet | Regular employee | Sees only their own sheets |
| 5 | Multi-company isolation | User in Company A | Cannot see Company B sheets |

## 6. Payslip Integration Test Plan

| # | Test Case | Steps | Expected Result |
|---|-----------|-------|-----------------|
| 1 | Create payslip from sheet | Approved sheet → "Create Payslip" wizard | hr.payslip created with attendance_sheet_id |
| 2 | Payslip inputs computed | Open payslip → Attendance tab | overtime_hours, late_in_hours, absence_days, difference_hours populated |
| 3 | Salary rules fire | Compute payslip | OVERT, LATE, ABS, DIFF lines appear in payslip lines |
| 4 | Print report | Click "Print" on sheet | PDF report downloads with all daily lines + totals |
| 5 | Block double payslip | Try to create payslip on sheet with existing payslip | UserError raised |

## 7. Change Data Wizard Test Plan

| # | Test Case | Steps | Expected Result |
|---|-----------|-------|-----------------|
| 1 | Change overtime | Open line → "Change" → new_overtime=5, reason="extra hours approved" | Line updated, note recorded, changed_manually=True |
| 2 | Change without reason | Try to apply with empty reason | UserError raised |
| 3 | Change on non-computed sheet | Try to open wizard from approved sheet | UserError raised |

## 8. View Rendering Checklist

| # | View | What to Verify |
|---|------|----------------|
| 1 | Sheet kanban | Groups by state, cards show OT/late/absence totals |
| 2 | Sheet list | Columns render, sum row at bottom for OT/late/absence/diff |
| 3 | Sheet form | Statusbar shows draft→computed→approved→done, buttons show/hide correctly |
| 4 | Sheet pivot | Employee × month matrix with OT as measure |
| 5 | Sheet graph | Bar chart of OT per employee |
| 6 | Contract form (extended) | Attendance Policy group visible under Notes |
| 7 | Payslip form (extended) | Attendance page appears when attendance_sheet_id is set |
| 8 | Search filters | All state filters + Has Overtime + Has Absence work |
| 9 | Group By | Status / Employee / Policy groupings work |

## 9. Edge Cases Test Plan

| # | Test Case | Expected |
|---|-----------|----------|
| 1 | Empty required field (name on sheet) | Validation error |
| 2 | Duplicate sheet name (sequence collision) | Sequence auto-increments, no collision |
| 3 | Negative apply_after_minutes | No special validation (just produces more overtime) |
| 4 | Lateness step overlapping ranges | No constraint — first match wins |
| 5 | Public holiday line with no employee/dept/tag | Line matches all employees |
| 6 | Sheet with no attendances in period | All lines have worked_hours=0, all working days absent |
| 7 | Sheet across calendar month boundary | Works correctly — uses date range, not month |

## 10. Performance Test Plan

| # | Test Case | Setup | Expected Result |
|---|-----------|-------|-----------------|
| 1 | Monthly sheet computation | 1 employee, 30 days, ~2 attendances/day | < 2 seconds |
| 2 | Batch generation 50 employees | Department with 50 employees, monthly period | < 60 seconds |
| 3 | Batch generation 200 employees | Department with 200 employees | Use cron; < 5 minutes |

---

*Author: Ibrahim Elmasry*
