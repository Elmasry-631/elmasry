# Data Flow — el_hr_attendance_sheet

> How data flows through the module from raw attendance to payslip.

## Pipeline Stages

```
┌────────────────────────────────────────────────────────────────────┐
│ STAGE 1 — CONFIGURATION (one-time setup)                           │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  1. HR Manager creates overtime rules:                             │
│     - hr.attendance.rule.overtime(type=working_day, rate=1.5)      │
│     - hr.attendance.rule.overtime(type=weekend, rate=2.0)          │
│     - hr.attendance.rule.overtime(type=public_holiday, rate=3.0)   │
│                                                                    │
│  2. HR Manager creates lateness rules with steps:                  │
│     - hr.attendance.rule.lateness                                  │
│       └ step 1: 0-15 min, rate=1.0x                                │
│       └ step 2: 15-30 min, rate=1.5x                               │
│       └ step 3: 30-60 min, rate=2.0x + amount=$10                  │
│       └ step 4: 60+ min, rate=3.0x + amount=$25                    │
│                                                                    │
│  3. HR Manager creates absence rules with steps:                   │
│     - hr.attendance.rule.absence                                   │
│       └ step 1: 1-3 days, rate=1.0x                                │
│       └ step 2: 4-7 days, rate=1.5x                                │
│       └ step 3: 8+ days, rate=2.0x                                 │
│                                                                    │
│  4. HR Manager creates policy:                                     │
│     - hr.attendance.policy(                                        │
│         overtime_working_id=<step1>,                               │
│         overtime_weekend_id=<step2>,                               │
│         overtime_holiday_id=<step3>,                               │
│         lateness_id=<lateness>,                                    │
│         absence_id=<absence>)                                      │
│                                                                    │
│  5. HR Manager assigns policy to contract:                         │
│     - hr.contract.attendance_policy_id = <policy>                  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ STAGE 2 — DAILY ATTENDANCE (already running)                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Employees check-in/out via hr_attendance:                         │
│     - hr.attendance(employee_id, check_in, check_out)              │
│                                                                    │
│  Public holidays defined:                                          │
│     - hr.attendance.public.holiday(date_from, date_to, line_ids)   │
│                                                                    │
│  Approved leaves via hr_holidays:                                  │
│     - hr.leave(employee_id, date_from, date_to, state=validate)    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ STAGE 3 — SHEET COMPUTATION (per employee per period)              │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  HR Officer creates sheet:                                         │
│     - hr.attendance.sheet(employee_id, date_from, date_to)         │
│     - state = draft                                                │
│                                                                    │
│  Click "Compute":                                                  │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │ action_compute() pipeline:                                    │ │
│  │ 1. Get contract = employee.contract_id on date_from           │ │
│  │ 2. Get policy = contract.attendance_policy_id                 │ │
│  │ 3. Get calendar = contract.resource_calendar_id               │ │
│  │ 4. Get all attendances in [date_from, date_to] (one query)    │ │
│  │ 5. Get all approved leaves in [date_from, date_to]            │ │
│  │ 6. Get all public holidays in [date_from, date_to]            │ │
│  │ 7. For each day in period:                                    │ │
│  │    a. planned_hours = calendar.hours_for_day(date)            │ │
│  │    b. worked_hours = sum(check_out - check_in for that day)   │ │
│  │    c. Handle multi-interval days (multiple check-in/out)      │ │
│  │    d. Handle overlapping intervals                            │ │
│  │    e. is_leave = approved leave exists for this day?          │ │
│  │    f. is_absent = (planned > 0 AND worked == 0 AND no leave)  │ │
│  │    g. late_in_minutes = max(0, first_check_in - shift_start)  │ │
│  │    h. overtime_hours = compute_overtime(worked, planned,      │ │
│  │                                  policy, is_public_holiday)   │ │
│  │    i. difference_hours = worked - planned - overtime          │ │
│  │    j. Create hr.attendance.sheet.line with all values         │ │
│  │ 8. Compute totals from lines                                  │ │
│  │ 9. state = computed                                           │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ STAGE 4 — REVIEW & CORRECTION                                      │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  HR Officer reviews sheet:                                         │
│  - For each line, can click "Change Data" → wizard:                │
│    hr.attendance.change.data.wizard(                               │
│      sheet_line_id=<line>,                                         │
│      new_overtime_hours=2.5,                                       │
│      new_late_in_minutes=10,                                       │
│      new_difference_hours=0,                                       │
│      reason="Approved by manager - shift extension")              │
│    → action_apply() updates the line + stores reason in note       │
│                                                                    │
│  Click "Approve":                                                  │
│    - state = approved                                              │
│    - Posts message in chatter "Sheet approved by <user>"           │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ STAGE 5 — PAYSLIP GENERATION                                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Click "Create Payslip":                                           │
│    - Opens wizard: hr.attendance.create.payslip.wizard             │
│    - User selects salary structure (default: Attendance Structure) │
│    - action_create_payslip() creates:                              │
│      hr.payslip(                                                   │
│        employee_id, date_from, date_to,                            │
│        struct_id=attendance_structure,                             │
│        attendance_sheet_id=<this sheet>,                           │
│        contract_id=<employee's contract>)                          │
│    - On payslip compute:                                           │
│      - overtime_hours = sheet.total_overtime                       │
│      - late_in_hours = sheet.total_late_in / 60                    │
│      - absence_days = sheet.total_absence                          │
│      - difference_hours = sheet.total_difference                   │
│    - Salary rules compute:                                         │
│      - OVERT = overtime_hours * contract.wage / 240 * policy.rate  │
│      - LATE = late_in_hours * lateness_step_rate * ...             │
│      - ABS = absence_days * contract.wage / 30 * absence_step_rate │
│      - DIFF = difference_hours * contract.wage / 240               │
│    - Sheet state = done                                            │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ STAGE 6 — BATCH MODE (optional, by department)                     │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  HR Manager opens batch wizard:                                    │
│    - hr.attendance.sheet.batch.wizard(department_id, period)       │
│    - action_create_batch() creates:                                │
│      hr.attendance.sheet.batch(department_id, date_from, date_to)  │
│      For each employee in department:                              │
│        hr.attendance.sheet.batch.line(                             │
│          batch_id, employee_id,                                    │
│          sheet_id=<newly created sheet>)                           │
│      Each sheet auto-computed                                      │
│    - Confirm batch → all sheets go to approved                     │
│    - Done batch → all sheets go to done (payslips must exist)      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

## Key Algorithms

### Overtime Calculation Algorithm
```python
def compute_overtime(worked_hours, planned_hours, day_type, policy):
    """day_type: 'working_day' | 'weekend' | 'public_holiday'"""
    if day_type == 'public_holiday':
        rule = policy.overtime_holiday_id
    elif day_type == 'weekend':
        rule = policy.overtime_weekend_id
    else:
        rule = policy.overtime_working_id
    
    if not rule:
        return 0.0
    
    # On working day: overtime = max(0, worked - planned) - apply_after
    # On weekend/holiday: overtime = worked (all counts) - apply_after
    if day_type == 'working_day':
        overtime_raw = max(0, worked_hours - planned_hours)
    else:
        overtime_raw = worked_hours
    
    apply_after = rule.apply_after_minutes / 60.0
    billable = max(0, overtime_raw - apply_after)
    
    # The rate is applied in salary rule, not here
    # Here we just return billable hours
    return billable
```

### Lateness Penalty Algorithm
```python
def compute_lateness_penalty(late_minutes, lateness_rule):
    """Returns (rate, amount) tuple for salary rule."""
    if not lateness_rule or late_minutes <= 0:
        return (0.0, 0.0)
    
    # Find matching step
    step = None
    for s in lateness_rule.step_ids:
        if s.from_minutes <= late_minutes <= s.to_minutes:
            step = s
            break
    if not step:
        return (0.0, 0.0)
    
    if step.penalty_type == 'rate':
        return (step.rate * step.initial_rate, 0.0)
    else:  # amount
        return (0.0, step.amount * (late_minutes / step.from_minutes if step.from_minutes > 0 else 1))
```

### Absence Penalty Algorithm
```python
def compute_absence_penalty(absence_days, absence_rule):
    """Returns rate for salary rule."""
    if not absence_rule or absence_days <= 0:
        return 0.0
    
    step = None
    for s in absence_rule.step_ids:
        if s.from_days <= absence_days <= s.to_days:
            step = s
            break
    return step.rate if step else 0.0
```
