# Configuration Guide — el_payroll_wps

## What needs configuration?

**Almost nothing.** This module is intentionally zero-config.

## Salary Rule Codes (required)

| Code | Purpose | Required? |
|------|---------|-----------|
| `BASIC` | Basic wage — populates `wage` column | ✅ Yes |
| `HOUALLOW` | Housing allowance — populates `house` column | ⚠ Recommended (column shows 0 if absent) |
| `NET` | Net salary — populates `Salary(total)` column | ✅ Yes |

### How to verify
1. **Payroll → Configuration → Rules**.
2. Filter by code — there should be exactly one rule per code.

### If your codes differ
Either rename your rules, or edit the module's Python:
- `wizard/wps_export_wizard.py::action_export()`:
  - `slip._get_line_amount_by_code('NET')` → change `'NET'` to your code
  - `slip._get_line_amount_by_code('BASIC')` → change `'BASIC'`
  - `slip._get_line_amount_by_code('HOUALLOW')` → change `'HOUALLOW'`
- `models/hr_payslip.py::_compute_x_others()`:
  - `slip._get_line_total_by_category('ALW')` → change `'ALW'`
  - `slip._get_line_total_by_category('DED')` → change `'DED'`

## Salary Rule Category Codes (required)

| Code | Purpose |
|------|---------|
| `ALW` | Allowances category — used to compute `x_others` |
| `DED` | Deductions category — used to compute `x_others` AND the `discount` column |

## Employee Fields (recommended)

For best CSV output, each employee should have:
- **Primary Bank Account** set (Odoo 19: HR → Employees → open → Private tab → Primary Bank Account).
- **National ID** set in `identification_id`.
- **Private State** set (state/province via `hr.version`).

If any are missing, the corresponding CSV columns will be empty for that employee.

## Security Configuration
No additional configuration. The module re-uses `hr_payroll.group_hr_payroll_user`.

## Multi-Company
Inherits `hr_payroll`'s existing multi-company record rules on `hr.payslip`.

## Multi-Currency
Out of scope. CSV uses whatever currency the payslip is in.
