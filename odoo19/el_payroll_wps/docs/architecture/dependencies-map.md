# Dependencies Map — el_payroll_wps

## 1. Direct Dependencies

| Module | Required? | Reason |
|--------|-----------|--------|
| `base` | ✅ Yes | Required by every Odoo module; the validator (M053) also wants this explicit. |
| `hr_payroll` | ✅ Yes | We `_inherit = 'hr.payslip'` and use `hr_payroll.group_hr_payroll_user` for security. |

## 2. Soft Dependency (menu parent only)

| Module | Required? | Reason |
|--------|-----------|--------|
| `hr_work_entry_enterprise` | ⚠ Soft | Provides `menu_hr_payroll_root` — used as the menu parent xmlid. If this module is not installed, the menu will be parentless; the `post_init_hook` will still try to reparent it by name lookup. |

## 3. Implicit Dependencies (transitive)

| Module | Comes From | Reason |
|--------|------------|--------|
| `hr` | hr_payroll depends on it | `hr.employee`, `private_state_id`, `primary_bank_account_id`, `identification_id` |
| `hr_version` (or `hr.version` model) | via hr | Provides `private_state_id` field on `hr.employee` through `_inherits` |
| `mail` | hr depends on it | (not directly used by us) |

## 4. Deliberately NOT Depended On

| Module | Why Not |
|--------|---------|
| `account` | Out of scope — no accounting entries |
| `l10n_*` | No country-specific logic |
| `hr_payroll_account` | Out of scope — CSV uses payslip line totals, not move lines |

## 5. External Service Dependencies
- **None.** CSV is produced locally with Python's `csv` module.

## 6. Python Imports (runtime)

| Import | Used For |
|--------|----------|
| `base64` | Encode CSV bytes into the ir.attachment `datas` field |
| `csv` | Write rows |
| `io` | In-memory buffer (no temp files on disk) |
| `odoo.models`, `odoo.fields`, `odoo.api` | ORM |
| `odoo.exceptions.UserError` | Raise when no payslips found |
