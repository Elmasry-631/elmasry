# Impact Analysis — el_payroll_wps

## 1. Files Touched in Standard Odoo

| File | Touched? | How |
|------|----------|-----|
| `hr_payroll/views/hr_payslip_views.xml` | Indirectly | We inherit `view_hr_payslip_form` and add `x_others` after `note`. We do NOT modify the original file. |

No other standard view, model, or security file is modified.

## 2. Database Impact

| Effect | Description |
|--------|-------------|
| New column | `hr_payslip.x_others` (Float) — added by ORM at install |
| New table | `wps_export_wizard` (TransientModel — auto-cleaned daily) |
| New ir.attachment records | One per export run — recommend monthly purge cron (out of scope) |
| New ir.ui.menu | `menu_wps_export` — parented under `hr_work_entry_enterprise.menu_hr_payroll_root` |
| New ir.actions.act_window | `action_wps_export_wizard` |
| New ir.rule | None (we re-use `hr_payroll.group_hr_payroll_user`) |

## 3. Performance Impact

| Operation | Before | After | Risk |
|-----------|--------|-------|------|
| `compute_sheet()` on 1 payslip | baseline | +1 SQL to sum ALW + 1 SQL to sum DED (cached) | Negligible |
| Payslip form load | baseline | +0 SQL (x_others is stored, not computed on view) | None |
| WPS export of 1,000 payslips | N/A | ~1 search query + 1,000 × 4 line-filter ops | Acceptable (< 5s) |

## 4. Security Impact

| Vector | Risk | Mitigation |
|--------|------|------------|
| Unauthorized user runs export | Medium | Wizard ACL restricts to `hr_payroll.group_hr_payroll_user` |
| Multi-company leakage | Low | Inherits `hr_payroll`'s record rules on `hr.payslip` |
| CSV leaks employee PII | Inherent | Restricted to Payroll users who already have access |

## 5. Upgrade Safety

| Odoo Upgrade Path | Risk | Mitigation |
|-------------------|------|------------|
| 19.0 → 19.x patch | None | No private APIs used |
| 19.x → 20.0 | Low | `primary_bank_account_id` may be renamed — `_get_bank_account` checks `_fields` and falls back to `bank_account_id` |
| `hr_payroll` major version bump | Low | `compute_sheet` is a stable public method |

## 6. Rollback Plan
1. `odoo -d <db> --uninstall el_payroll_wps --stop-after-init`
2. `x_others` column dropped; `wps_export_wizard` table dropped; menu/action/ACL records removed.
3. Existing `ir.attachment` CSV files remain (owned by `ir.attachment`, not by this module).
