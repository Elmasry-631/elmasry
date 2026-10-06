# Workflows — el_hr_attendance_sheet

> State machines + business workflows.

## 1. Attendance Sheet Workflow

```
[Draft] ──compute──► [Computed] ──approve──► [Approved] ──create_payslip──► [Done]
   ▲                    │                        │
   │                    │                        │
   │              cancel │                  cancel │
   │                    ▼                        ▼
   └──draft─── [Cancelled] ◄──draft─────────────
```

### Trigger matrix

| From | To | Trigger | Validation |
|------|-----|---------|------------|
| draft | computed | action_compute() | contract + policy must exist |
| computed | computed | action_compute() (re-run) | always allowed |
| computed | approved | action_approve() | must have lines |
| approved | done | action_done() | payslip must exist |
| draft / computed / approved | cancelled | action_cancel() | payslip not done |
| cancelled | draft | action_draft() | always allowed |

## 2. Batch Workflow

```
[Draft] ──generate_sheets──► [Confirmed] ──done──► [Done]
   ▲                              │
   │                              │
   │                         cancel│
   │                              ▼
   └──draft─── [Cancelled] ◄──draft
```

When a batch is generated, one sheet per employee in the department is created and auto-computed. Cancelling a batch cascades cancellation to all child sheets.

## 3. Public Holiday Workflow

```
[Draft] ──activate──► [Active] ──cancel──► [Cancelled] ──draft──► [Draft]
```

Activation requires at least one line. Active holidays are used in overtime calculation.

## 4. End-to-End Business Workflow

```
1. Setup (one-time)
   ├── Create overtime rules (3 types)
   ├── Create lateness rule + steps
   ├── Create absence rule + steps
   ├── Create attendance policy referencing the rules
   └── Assign policy to each contract (hr.contract.attendance_policy_id)

2. Daily operations
   ├── Employees check in/out via hr_attendance
   ├── HR defines public holidays (when applicable)
   └── Employees request leaves via hr_holidays

3. Payroll cycle (e.g. monthly)
   ├── HR Officer creates attendance sheet per employee
   │     - Set employee + date range
   │     - Click "Compute"
   │     - Review lines; use "Change" wizard to adjust with reason
   │     - Click "Approve"
   ├── OR HR Manager creates a batch by department
   │     - Use batch wizard
   │     - Sheets auto-generated and auto-computed
   │     - Manager reviews/approves each sheet
   ├── For each approved sheet
   │     - Click "Create Payslip"
   │     - Select "Attendance Structure"
   │     - Payslip created with OT/late/absence/diff inputs
   │     - Salary rules OVERT, LATE, ABS, DIFF compute monetary amounts
   ├── Confirm payslips in hr_payroll
   └── Sheet state moves to "Done" automatically

4. Reporting
   └── Click "Print" on any sheet for PDF report
```

## 5. Computation Pipeline (Internal)

When `action_compute()` runs:

1. **Validate** state (draft or computed), contract exists, policy exists
2. **Delete** existing lines
3. **Bulk fetch** all attendances for the period (single query)
4. **Bulk fetch** all approved leaves for the period (single query)
5. **Bulk fetch** all active public holidays overlapping the period (single query)
6. **For each day** in [date_from, date_to]:
   - Determine day_type (working_day / weekend / public_holiday)
   - Get planned_hours from resource.calendar
   - Compute worked_hours (sum of check_out - check_in, multi-interval aware)
   - Compute late_in_minutes (only on working days, vs shift start)
   - Detect is_absent / is_leave
   - Apply overtime rule → billable overtime hours
   - Compute difference_hours = worked - planned - overtime
   - Create sheet.line record
7. **Compute totals** from lines (sum)
8. **Set state** to computed
9. **Post message** in chatter

---

*Author: Ibrahim Elmasry*
