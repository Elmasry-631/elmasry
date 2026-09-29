# Model Design — el_hr_attendance_sheet

> Relationships between the 17 models in this module.

## Model Relationship Map (text)

```
                                  ┌─────────────────────────────┐
                                  │   hr.attendance.policy      │
                                  │   - name, active            │
                                  │   - overtime_working_id     │──┐
                                  │   - overtime_weekend_id     │  │
                                  │   - overtime_holiday_id     │  │
                                  │   - lateness_id             │  │
                                  │   - absence_id              │  │
                                  └───────────┬─────────────────┘  │
                                              │                    │
                                              │ (Many2one)         │
                                              ▼                    │
                              ┌─────────────────────────────┐      │
                              │   hr.contract (EXTEND)      │      │
                              │   - attendance_policy_id    │      │
                              └───────────┬─────────────────┘      │
                                          │                        │
                                          │ (One2many from sheet)  │
                                          ▼                        │
              ┌───────────────────────────────────────────┐        │
              │   hr.attendance.sheet                     │        │
              │   - name, employee_id, date_from, date_to │        │
              │   - contract_id, policy_id, state         │        │
              │   - total_overtime, total_late_in         │        │
              │   - total_absence, total_difference       │        │
              │   - payslip_id, batch_id                  │        │
              └─────┬───────────────────────┬─────────────┘        │
                    │                       │                      │
                    │ (One2many)            │ (Many2one)           │
                    ▼                       ▼                      │
   ┌──────────────────────────────┐  ┌──────────────────────┐      │
   │ hr.attendance.sheet.line     │  │ hr.payslip (EXTEND)  │      │
   │ - sheet_id, date             │  │ - attendance_sheet_id│      │
   │ - planned_hours, worked_hours│  │ - overtime_hours     │      │
   │ - overtime_hours             │  │ - late_in_hours      │      │
   │ - late_in_minutes            │  │ - absence_days       │      │
   │ - is_absent, is_leave        │  │ - difference_hours   │      │
   │ - leave_id, difference_hours │  └──────────────────────┘      │
   │ - attendance_ids, note       │                                │
   └──────────────────────────────┘                                │
                                                                   │
   ┌──────────────────────────────────┐                            │
   │ hr.attendance.public.holiday     │                            │
   │ - name, date_from, date_to       │                            │
   │ - active, state                  │                            │
   │ - line_ids                       │                            │
   └─────┬────────────────────────────┘                            │
         │                                                        │
         │ (One2many)                                             │
         ▼                                                        │
   ┌──────────────────────────────────┐                            │
   │ hr.attendance.public.holiday.line│                            │
   │ - holiday_id                     │                            │
   │ - employee_id, department_id     │                            │
   │ - employee_tag_ids               │                            │
   └──────────────────────────────────┘                            │
                                                                   │
   ┌──────────────────────────────────┐    ┌───────────────────┐   │
   │ hr.attendance.rule.overtime      │◄───│ (policy uses 3)   │───┘
   │ - name, type, apply_after_minutes│    └───────────────────┘
   │ - rate, active                   │
   └──────────────────────────────────┘
   type = working_day | weekend | public_holiday

   ┌──────────────────────────────────┐    ┌──────────────────────┐
   │ hr.attendance.rule.lateness      │───►│ hr.attendance.rule   │
   │ - name, active, step_ids         │    │ .lateness.step       │
   └──────────────────────────────────┘    │ - lateness_id        │
                                           │ - from_minutes       │
                                           │ - to_minutes         │
                                           │ - penalty_type       │
                                           │ - rate, amount       │
                                           │ - initial_rate       │
                                           └──────────────────────┘

   ┌──────────────────────────────────┐    ┌──────────────────────┐
   │ hr.attendance.rule.absence       │───►│ hr.attendance.rule   │
   │ - name, active, step_ids         │    │ .absence.step        │
   └──────────────────────────────────┘    │ - absence_id         │
                                           │ - from_days, to_days │
                                           │ - rate               │
                                           └──────────────────────┘

   ┌──────────────────────────────────┐
   │ hr.attendance.sheet.batch        │
   │ - name, department_id            │
   │ - date_from, date_to, state      │
   │ - line_ids                       │
   └─────┬────────────────────────────┘
         │
         ▼
   ┌──────────────────────────────────┐
   │ hr.attendance.sheet.batch.line   │
   │ - batch_id, employee_id          │
   │ - sheet_id (generated)           │
   └──────────────────────────────────┘

   ┌──────────────────────────────────────────────┐
   │ WIZARDS (TransientModels)                    │
   ├──────────────────────────────────────────────┤
   │ hr.attendance.change.data.wizard             │
   │ - sheet_line_id, new_overtime_hours          │
   │ - new_late_in_minutes, new_difference_hours  │
   │ - reason                                     │
   ├──────────────────────────────────────────────┤
   │ hr.attendance.sheet.batch.wizard             │
   │ - department_id, date_from, date_to          │
   │ - employee_ids                               │
   ├──────────────────────────────────────────────┤
   │ hr.attendance.create.payslip.wizard          │
   │ - sheet_id, employee_id, date_from, date_to  │
   │ - struct_id                                  │
   └──────────────────────────────────────────────┘
```

## Field Inheritance Strategy

- `hr.contract`: inherit (classic) → add `attendance_policy_id`
- `hr.payslip`: inherit (classic) → add 5 fields + computed
- All other models: NEW (`_name` + `_description`)
- All config models inherit nothing (no chatter, lightweight)
- Transactional models (sheet, batch, policy, public.holiday) inherit `mail.thread` + `mail.activity.mixin` where appropriate

## Computed Fields Summary

| Model | Field | Compute Method | Depends |
|---|---|---|---|
| hr.attendance.sheet | total_overtime | `_compute_totals` | line_ids.overtime_hours |
| hr.attendance.sheet | total_late_in | `_compute_totals` | line_ids.late_in_minutes |
| hr.attendance.sheet | total_absence | `_compute_totals` | line_ids.is_absent |
| hr.attendance.sheet | total_difference | `_compute_totals` | line_ids.difference_hours |
| hr.payslip | overtime_hours | `_compute_attendance_data` | attendance_sheet_id |
| hr.payslip | late_in_hours | `_compute_attendance_data` | attendance_sheet_id |
| hr.payslip | absence_days | `_compute_attendance_data` | attendance_sheet_id |
| hr.payslip | difference_hours | `_compute_attendance_data` | attendance_sheet_id |
