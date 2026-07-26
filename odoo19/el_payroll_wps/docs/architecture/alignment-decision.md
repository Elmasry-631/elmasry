# Alignment Decision — el_payroll_wps

## 1. User-Stated Requirements vs. Implementation

| User Said (correct spec) | Implementation Decision | Aligned? |
|---------------------------|-------------------------|----------|
| Add Others field = Allowances − Deductions on paysroll | `x_others` Float on `hr.payslip`, computed in `compute_sheet()` override | ✅ |
| Others is informational — manually editable | NOT `@api.depends` compute — called only from `compute_sheet()` | ✅ |
| Export wizard named WPS that produces CSV per month | `wps.export.wizard` TransientModel + `action_export()` returns CSV download | ✅ |
| CSV columns: Bank, Account, Salary(total), Notice(month), Name, ID number, address, wage, house, Others, discount | Exact column order, exact header strings | ✅ |
| Notice = the month being paid | `strftime('%B')` of `wizard.month` (e.g. `July`) | ✅ |
| Discount = positive (per corrected spec) | `abs(DED_total)` — always positive | ✅ |
| Wage = Basic Salary | `slip._get_line_amount_by_code('BASIC')` | ✅ |
| House = 0 if absent (HOUALLOW code) | `_get_line_amount_by_code('HOUALLOW')` returns `0.0` if no line matches | ✅ |
| Filename = `Salary_<Month>_<Year>.csv` | ` 'Salary_%s.csv' % date_from.strftime('%B_%Y')` | ✅ |
| Odoo 19 states: `validated` / `paid` | `('state', 'in', ['validated', 'paid'])` | ✅ |
| Odoo 19 bank: `primary_bank_account_id` | Prefers `primary_bank_account_id`, falls back to `bank_account_id` | ✅ |
| Odoo 19 address: `private_state_id` (hr.version) | `employee.private_state_id.name or ''` | ✅ |
| Menu parented under Payroll root | `parent="hr_work_entry_enterprise.menu_hr_payroll_root"` + `post_init_hook` safety net | ✅ |

## 2. Decisions Where We Deviated from the Naive Approach

| Decision | Naive Approach | Skill-Compliant Approach | Reason |
|----------|----------------|--------------------------|--------|
| Field naming | `others` | `x_others` | Honors user's spec; `x_` prefix marks custom fields |
| Wizard vs. server action | `ir.actions.server` with context | `TransientModel` wizard + `act_window` | Server actions cannot ask the user for the month input |
| Menu parent | Hardcode `hr_payroll.menu_hr_payroll_root` | `hr_work_entry_enterprise.menu_hr_payroll_root` + `post_init_hook` | The O19 root menu xmlid lives in `hr_work_entry_enterprise`; the hook is a safety net |
| Encoding | `utf-8` | `utf-8-sig` (with BOM) | Excel opens Arabic text correctly only with BOM |
| Address field | `employee.address_home_id` (removed in O19) | `employee.private_state_id` (from `hr.version` via `_inherits`) | Per user's correct O19 spec |
| Bank account | `employee.bank_account_id` (renamed in O19) | `employee.primary_bank_account_id` with `bank_account_id` fallback | Per user's correct O19 spec + defensive |
| Payslip states | `('done', 'paid')` (≤18) | `('validated', 'paid')` (O19) | Per user's correct O19 spec |
| Housing rule code | `HOUSE` | `HOUALLOW` | Per user's correct spec |
| Discount sign | Negative (`-200`) | Positive (`200`) | Per user's corrected spec |
| Filename prefix | `WPS_` | `Salary_` | Per user's corrected spec |
| Compute hook | `@api.depends('line_ids.total')` | Explicit call from `compute_sheet()` | `@api.depends` would overwrite manual edits on every form save |

## 3. Acceptance Check

The implementation aligns 1:1 with every functional requirement in the user's correct (latest) spec. All Odoo 19 compatibility adjustments (`validated`/`paid` states, `primary_bank_account_id`, `private_state_id`, `HOUALLOW`, `Salary_` prefix, positive discount) are reflected exactly as the user provided.
