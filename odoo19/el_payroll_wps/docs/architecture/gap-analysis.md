# GAP Analysis — el_payroll_wps

## 1. Requirement → Standard Module Mapping

| # | Requirement | Standard Module | Coverage | Custom Work Needed? |
|---|-------------|-----------------|----------|---------------------|
| 1 | Auto "Others" field on payslip | `hr_payroll` | ❌ None | ✅ YES — add `x_others` field + compute hook |
| 2 | Monthly WPS CSV export | `hr_payroll` | ❌ None | ✅ YES — build `wps.export.wizard` + CSV writer |
| 3 | CSV columns Bank/Account/Name/ID/State | `hr` + `hr_payroll` + `hr.version` | ✅ Full data | ❌ NO — read from existing fields |
| 4 | CSV columns Wage/House/Others/Discount | `hr_payroll` | ⚠ Partial — line codes `BASIC`, `HOUALLOW`, `NET` exist; categories `ALW`/`DED` exist | ❌ NO — aggregate from existing line_ids |
| 5 | Excel/Arabic-safe encoding | `base` (Python stdlib) | ✅ Full | ❌ NO — use `utf-8-sig` |
| 6 | Menu under Payroll app | `hr_work_entry_enterprise` | ✅ Full | ❌ NO — use `parent="hr_work_entry_enterprise.menu_hr_payroll_root"` + `post_init_hook` safety net |
| 7 | Security: Payroll-only access | `hr_payroll.group_hr_payroll_user` | ✅ Full | ❌ NO — reuse existing group |

## 2. Build Scope (Custom Work)

1. **Models to build:** `wps.export.wizard` (TransientModel — 1 field, 3 methods)
2. **Models to extend:** `hr.payslip` (add `x_others`, override `compute_sheet`, 3 helper methods)
3. **Views to write:** 1 wizard form, 1 payslip form inherit
4. **Menus to write:** 1 menu item (`menu_wps_export`)
5. **Security to write:** 1 ACL line on `wps.export.wizard`

## 3. Dependency Decision

| Module | Action | Reason |
|--------|--------|--------|
| `base` | depend | Always required + validator (M053) wants it explicit |
| `hr_payroll` | depend | Extend `hr.payslip` + reuse `group_hr_payroll_user` |
| `hr_work_entry_enterprise` | soft (menu parent xmlid only) | If installed, the menu parents correctly; if not, the `post_init_hook` reparents by name |
| `account` | ❌ NOT depend | No accounting impact |
| `hr_payroll_account` | ❌ NOT depend | CSV uses payslip lines, not move lines |

## 4. Estimated Effort Reduction
- Requirements that standard Odoo covers: 5 out of 7
- Effort saved: ~70%
- Actual custom scope: 2 small Python files + 2 small XML views + 1 ACL line + 1 hook function
