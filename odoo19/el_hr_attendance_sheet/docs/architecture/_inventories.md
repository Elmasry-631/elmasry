# Architecture Inventories — el_hr_attendance_sheet

> STOP GATE 1 deliverable. User must confirm these 4 inventories before any Python code is written.

---

## STEP 0 — Requirements Summary

```
=== REQUIREMENTS SUMMARY ===

Spec: https://apps.odoo.com/apps/modules/19.0/el_hr_attendance_sheet
Target Odoo: 19.0
Module Technical Name: el_hr_attendance_sheet
Module Pretty Name: HR Attendance Sheet And Policies
License: LGPL-3
Author: Ibrahim Elmasry

DEPENDENCIES:
  hr_attendance, hr, hr_payroll, hr_holidays, mail, calendar

MODELS IDENTIFIED (17 total):
  1.  hr.attendance.public.holiday        — Public holiday definition (period + active flag + employee selection)
  2.  hr.attendance.public.holiday.line   — Line: which employees/departments/tags the holiday applies to
  3.  hr.attendance.rule.overtime         — Overtime rule (3 types: working_day / weekend / public_holiday) with apply_after + rate
  4.  hr.attendance.rule.lateness         — Lateness rule header
  5.  hr.attendance.rule.lateness.step    — Lateness step (from_minutes → to_minutes, penalty type, rate/amount)
  6.  hr.attendance.rule.absence          — Absence rule header
  7.  hr.attendance.rule.absence.step     — Absence step (from_days → to_days, rate)
  8.  hr.attendance.policy                — Policy combining overtime + lateness + absence rules
  9.  hr.attendance.sheet                 — Main sheet: employee + period + computed totals (overtime/late/absence/diff)
  10. hr.attendance.sheet.line            — Per-day breakdown: planned/actual/overtime/late/absence/leave/diff
  11. hr.attendance.sheet.batch           — Batch header to generate sheets for a department
  12. hr.attendance.sheet.batch.line      — Batch line: sheet per employee in the department
  13. hr.attendance.change.data.wizard    — Transient: modify overtime/late/diff with reason note
  14. hr.attendance.sheet.batch.wizard    — Transient: select department + period → generate batch
  15. hr.attendance.create.payslip.wizard — Transient: select employee + sheet → generate payslip
  16. hr.contract (EXTEND)                — add attendance_policy_id field
  17. hr.payslip (EXTEND)                 — add attendance_sheet_id link + computed inputs

WIZARDS:
  - hr.attendance.change.data.wizard
  - hr.attendance.sheet.batch.wizard
  - hr.attendance.create.payslip.wizard

REPORTS:
  - Attendance Sheet PDF report (QWeb)

DATA FILES:
  - Salary Rules (Overtime, Absence, Late In, Difference Time)
  - Attendance Salary Structure referencing the 4 rules
  - Sequences for sheet, batch, policy

CONTROLLERS / OWL: None required (pure backend module)

STATE MACHINES:
  - hr.attendance.sheet:        draft → computed → approved → done / cancelled
  - hr.attendance.sheet.batch:  draft → confirmed → done / cancelled
  - hr.attendance.public.holiday: draft → active / cancelled

⚠️ UNCLEAR / NEEDS CLARIFICATION:
  1. Multi-company? → Assume multi-company aware via hr.contract.company_id (multi-company rules)
  2. Working schedule? → Reuse resource.calendar from hr.contract (no new model)
  3. Language? → English only (user's previous answer)
  4. License? → LGPL-3
```

---

## STEP 1.1 — Model Inventory

| # | Model Name | Type | Key Fields | Inherited |
|---|---|---|---|---|
| 1 | `hr.attendance.public.holiday` | `models.Model` | name, date_from, date_to, active, state, line_ids | mail.thread, mail.activity.mixin |
| 2 | `hr.attendance.public.holiday.line` | `models.Model` | holiday_id, employee_id, department_id, employee_tag_ids | — |
| 3 | `hr.attendance.rule.overtime` | `models.Model` | name, type (working_day/weekend/public_holiday), apply_after_minutes, rate, active | — |
| 4 | `hr.attendance.rule.lateness` | `models.Model` | name, active, step_ids | — |
| 5 | `hr.attendance.rule.lateness.step` | `models.Model` | lateness_id, from_minutes, to_minutes, penalty_type (rate/amount), rate, amount, initial_rate | — |
| 6 | `hr.attendance.rule.absence` | `models.Model` | name, active, step_ids | — |
| 7 | `hr.attendance.rule.absence.step` | `models.Model` | absence_id, from_days, to_days, rate | — |
| 8 | `hr.attendance.policy` | `models.Model` | name, overtime_working_id, overtime_weekend_id, overtime_holiday_id, lateness_id, absence_id, active | mail.thread |
| 9 | `hr.attendance.sheet` | `models.Model` | name, employee_id, date_from, date_to, contract_id, policy_id, state, total_overtime, total_late_in, total_absence, total_difference, line_ids, payslip_id, batch_id | mail.thread, mail.activity.mixin |
| 10 | `hr.attendance.sheet.line` | `models.Model` | sheet_id, date, planned_hours, worked_hours, overtime_hours, late_in_minutes, is_absent, is_leave, leave_id, difference_hours, attendance_ids, note | — |
| 11 | `hr.attendance.sheet.batch` | `models.Model` | name, department_id, date_from, date_to, state, line_ids | mail.thread |
| 12 | `hr.attendance.sheet.batch.line` | `models.Model` | batch_id, employee_id, sheet_id | — |
| 13 | `hr.attendance.change.data.wizard` | `TransientModel` | sheet_line_id, new_overtime_hours, new_late_in_minutes, new_difference_hours, reason | — |
| 14 | `hr.attendance.sheet.batch.wizard` | `TransientModel` | department_id, date_from, date_to, employee_ids | — |
| 15 | `hr.attendance.create.payslip.wizard` | `TransientModel` | sheet_id, employee_id, date_from, date_to, struct_id | — |
| 16 | `hr.contract` (extend) | `models.Model` | attendance_policy_id | (existing) |
| 17 | `hr.payslip` (extend) | `models.Model` | attendance_sheet_id, overtime_hours, late_in_hours, absence_days, difference_hours | (existing) |

**Rules:** Every model in `models/__init__.py`. TransientModels in `wizard/__init__.py`. Extensions of hr.contract / hr.payslip in `models/`.

---

## STEP 1.2 — View Inventory

| Model | Form | List | Search | Kanban | Pivot | Graph |
|---|---|---|---|---|---|---|
| `hr.attendance.public.holiday` | ✅ | ✅ | ✅ | — | — | — |
| `hr.attendance.rule.overtime` | ✅ | ✅ | ✅ | — | — | — |
| `hr.attendance.rule.lateness` | ✅ (with step_ids inline) | ✅ | ✅ | — | — | — |
| `hr.attendance.rule.absence` | ✅ (with step_ids inline) | ✅ | ✅ | — | — | — |
| `hr.attendance.policy` | ✅ | ✅ | ✅ | — | — | — |
| `hr.attendance.sheet` | ✅ (with line_ids tree in form) | ✅ | ✅ | ✅ | ✅ (overtime by dept) | ✅ (bar: overtime/late/absence) |
| `hr.attendance.sheet.batch` | ✅ | ✅ | ✅ | — | — | — |
| `hr.contract` (extended) | ✅ (xpath add policy_id) | — | — | — | — | — |
| `hr.payslip` (extended) | ✅ (xpath add attendance_sheet_id) | — | — | — | — | — |
| Wizards (3) | ✅ each | — | — | — | — | — |

**Rule:** Every model with menu → form + list + search at minimum. Pivot/graph only on sheet (analytical model).

---

## STEP 1.3 — Action Inventory

| Action XML ID | Type | Target Model | Views | Triggered By |
|---|---|---|---|---|
| `action_hr_attendance_public_holiday` | act_window | hr.attendance.public.holiday | form, list, search | menu_hr_attendance_public_holiday |
| `action_hr_attendance_rule_overtime` | act_window | hr.attendance.rule.overtime | form, list, search | menu_hr_attendance_rule_overtime |
| `action_hr_attendance_rule_lateness` | act_window | hr.attendance.rule.lateness | form, list, search | menu_hr_attendance_rule_lateness |
| `action_hr_attendance_rule_absence` | act_window | hr.attendance.rule.absence | form, list, search | menu_hr_attendance_rule_absence |
| `action_hr_attendance_policy` | act_window | hr.attendance.policy | form, list, search | menu_hr_attendance_policy |
| `action_hr_attendance_sheet` | act_window | hr.attendance.sheet | kanban, form, list, pivot, graph, search | menu_hr_attendance_sheet |
| `action_hr_attendance_sheet_batch` | act_window | hr.attendance.sheet.batch | form, list, search | menu_hr_attendance_sheet_batch |
| `action_hr_attendance_sheet_by_employee` | act_window (filtered) | hr.attendance.sheet | form, list, search | menu (under Employee form) |

---

## STEP 1.4 — Button → Method Map

| View | Button `name` | Python Method | Status |
|---|---|---|---|
| public.holiday form | `action_activate` | `def action_activate(self)` | MUST define |
| public.holiday form | `action_cancel` | `def action_cancel(self)` | MUST define |
| public.holiday form | `action_draft` | `def action_draft(self)` | MUST define |
| sheet form | `action_compute` | `def action_compute(self)` | MUST define — main calculation engine |
| sheet form | `action_approve` | `def action_approve(self)` | MUST define |
| sheet form | `action_done` | `def action_done(self)` | MUST define |
| sheet form | `action_cancel` | `def action_cancel(self)` | MUST define |
| sheet form | `action_draft` | `def action_draft(self)` | MUST define |
| sheet form | `action_create_payslip` | `def action_create_payslip(self)` | MUST define — opens wizard |
| sheet form | `action_change_data` | `def action_change_data(self)` | MUST define — opens wizard |
| sheet.line form (in sheet form) | `action_open_change_wizard` | `def action_open_change_wizard(self)` | MUST define |
| batch form | `action_generate_sheets` | `def action_generate_sheets(self)` | MUST define |
| batch form | `action_confirm` | `def action_confirm(self)` | MUST define |
| batch form | `action_done` | `def action_done(self)` | MUST define |
| batch form | `action_cancel` | `def action_cancel(self)` | MUST define |
| batch form | `action_draft` | `def action_draft(self)` | MUST define |
| change.data.wizard form | `action_apply` | `def action_apply(self)` | MUST define |
| batch.wizard form | `action_create_batch` | `def action_create_batch(self)` | MUST define |
| create.payslip.wizard form | `action_create_payslip` | `def action_create_payslip(self)` | MUST define |

**Rule:** Any row showing undefined method = STOP and define it before generating code.

---

## Architecture Files To Generate in STEP 1.5

1. `docs/architecture/gap-analysis.md` — Odoo standard coverage vs gaps closed
2. `docs/architecture/impact-analysis.md` — impact of extending hr.contract + hr.payslip
3. `docs/architecture/alignment-decision.md` — alignment with Odoo design patterns
4. `docs/architecture/model-design.md` — model relationships diagram (text)
5. `docs/architecture/data-flow.md` — sheet computation pipeline
6. `docs/architecture/state-machine-design.md` — sheet + batch + public.holiday state machines
7. `docs/architecture/dependencies-map.md` — depends + cross-module touchpoints

---

*Author: Ibrahim Elmasry — generated via odoo-master skill v10.7.1 BUILD MODE*
