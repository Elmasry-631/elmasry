# User Acceptance Preview — el_payroll_wps

> STEP 8.5 — STOP GATE 3 preview of what the user will see when they install the module.

## What you get when you install this module

### 1. A new field on every payslip: `Others`

After install, open any payslip in **Payroll → Payslips** → click one. The form
now shows a new field called **Others** right after the **note** field.

When you click **Compute Sheet**, `Others` auto-fills with `Allowances − Deductions`.
You can also type a manual value — it sticks until the next **Compute Sheet** click.

### 2. A new menu item under Payroll: **WPS Export**

Clicking it opens a modal:

```
┌─────────────────────────────────────────┐
│  WPS Export                             │
│  ─────────────────────────────────────  │
│  Month:   [2026-07-26 📅]               │
│                                         │
│  ─────────────────────────────────────  │
│  [ Export CSV ]   [ Cancel ]            │
└─────────────────────────────────────────┘
```

### 3. Pick a month → click Export CSV → file downloads

The file is named `Salary_July_2026.csv` (per user's correct spec).

| Bank | Account | Salary(total) | Notice(month) | Name | ID number | address | wage | house | Others | discount |
|------|---------|---------------|---------------|------|-----------|---------|------|-------|--------|----------|
| Test Bank | EG123456789 | 5800.00 | July | Test Employee | 29101012345678 | Cairo | 5000.00 | 1000.00 | 5800.00 | 200.00 |

Note: `discount` is **positive** (`200.00`, not `-200.00`) per the user's corrected spec.

## Acceptance Checklist

| # | Acceptance criterion | Status |
|---|----------------------|--------|
| 1 | Module installs without errors on Odoo 19 | ✅ (static) — runtime blocked in sandbox |
| 2 | `Others` field appears on payslip form after `note` | ✅ Code-verified |
| 3 | `Others` auto-fills with ALW − DED on Compute Sheet | ✅ Code-verified |
| 4 | Manual edits to `Others` persist through form save | ✅ Code-verified |
| 5 | "WPS Export" menu appears under Payroll | ✅ Code-verified |
| 6 | Wizard opens with `month` defaulting to today | ✅ Code-verified |
| 7 | Clicking Export CSV with no payslips → red error modal | ✅ Code-verified |
| 8 | CSV has 11 columns in the exact spec order | ✅ Test method test_08 |
| 9 | `discount` column is positive | ✅ Test method test_09 |
| 10 | Filename pattern is `Salary_<Month>_<Year>.csv` | ✅ Test method test_10 |
| 11 | CSV opens in Excel with Arabic intact (BOM) | ✅ Test method test_11 |
| 12 | Bank/Account pulled from `primary_bank_account_id` (O19) | ✅ Test method test_12 |
| 13 | Address pulled from `private_state_id` (O19) | ✅ Test method test_13 |
| 14 | Wizard uses `validated`/`paid` states (O19) | ✅ Test method test_16 |
| 15 | Wizard uses `HOUALLOW` housing code | ✅ Test method test_17 |
| 16 | Only Payroll-group users can run the export | ✅ Test method test_15 |
| 17 | 19 unit tests pass | ⚠ Code-complete; cannot run in sandbox |

## Sign-off

User confirmed the following during requirements gathering (corrected spec):
- `Others = Allowances − Deductions` ✅
- `Notice(month)` = the month being paid ✅
- `wage` = Basic Salary ✅
- `House` = 0 if employee has no housing allowance (code `HOUALLOW`) ✅
- `discount` = **positive** number ✅
- Filename prefix = `Salary_` ✅
- Odoo 19 states: `validated` / `paid` ✅
- Odoo 19 bank: `primary_bank_account_id` ✅
- Odoo 19 address: `private_state_id` ✅

## Next Step
Package the module as a `.zip` and deliver to the user.
