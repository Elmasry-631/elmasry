# Requirements Specification — el_payroll_wps

## 1. Overview
- **Module Name:** el_payroll_wps
- **Target Odoo Version:** 19
- **Category:** Human Resources/Payroll
- **Summary:** Adds an auto-computed "Others" field on payslips (Allowances − Deductions) and a WPS-style CSV export wizard that produces a monthly salary file for bank submission.
- **Author:** Ibrahim Elmasry

## 2. Business Problem
Companies participating in the **Wages Protection System (WPS)** must submit a monthly CSV file to the bank/authority. The file must contain, for every employee whose payslip was validated that month: bank name, account number, net salary, the salary month, employee name, national ID, employee state (address-equivalent column), basic wage, housing allowance, an "Others" amount (Allowances − Deductions), and the total deductions.

Standard `hr_payroll` does not expose a single button that produces this CSV, nor does it carry an "Others" informational column on the payslip. Today the HR team hand-builds this file in Excel every month — slow, error-prone, and inconsistent. This module removes that manual step.

## 3. Functional Requirements

### 3.1 Models
| # | Model Name | Purpose | Inherits | Key Fields |
|---|-----------|---------|----------|------------|
| 1 | hr.payslip (extend) | Add `x_others` informational field | — | x_others |
| 2 | wps.export.wizard (new TransientModel) | Wizard that produces the CSV for a chosen month | — | month |

### 3.2 Fields per Model

#### hr.payslip (inherited)
| Field | Type | Required | Index | Tracking | Notes |
|-------|------|----------|-------|----------|-------|
| x_others | Float | No | No | No | Auto = Allowances − Deductions; manually editable; informational only |

#### wps.export.wizard
| Field | Type | Required | Index | Tracking | Notes |
|-------|------|----------|-------|----------|-------|
| month | Date | Yes | No | No | Any date inside the target month; default = today |

### 3.3 State Machines
None — the wizard is a single-step transient; the payslip already has its own state machine from `hr_payroll`.

### 3.4 Views Required
| View ID | Type | Model | Purpose |
|---------|------|-------|---------|
| view_hr_payslip_form_inherit_wps | form (inherit) | hr.payslip | Show `x_others` after `note` |
| view_wps_export_wizard_form | form | wps.export.wizard | Wizard form with month + buttons |

### 3.5 Actions & Menus
| Action | Model | View Mode | Menu Parent |
|--------|-------|-----------|-------------|
| action_wps_export_wizard | wps.export.wizard | form | hr_work_entry_enterprise.menu_hr_payroll_root |

### 3.6 Security
| Group | Name | Permissions | Stakeholder |
|-------|------|-------------|-------------|
| hr_payroll.group_hr_payroll_user | Payroll User | RWCD on wps.export.wizard | HR Officer |

No new security group is created — the module re-uses the standard `hr_payroll` user group.

### 3.7 Reports
None — the deliverable is a CSV file, not a PDF report.

### 3.8 Wizards
| Wizard | Purpose | Triggered From |
|--------|---------|---------------|
| wps.export.wizard | Pick a month → produce WPS CSV | Payroll → WPS Export menu |

### 3.9 Email Templates
None.

### 3.10 Cron Jobs
None — the export is run on demand.

### 3.11 CSV Output Specification
File name: `Salary_<Month>_<Year>.csv` (e.g. `Salary_July_2026.csv`) — **per user's correct spec**.
Encoding: UTF-8 with BOM (so Excel opens Arabic text correctly).

Columns (in this exact order — per user's correct spec):

| # | Column Header | Source | Notes |
|---|---------------|--------|-------|
| 1 | `Bank` | `employee.primary_bank_account_id.bank_id.name` (Odoo 19) with `bank_account_id` fallback | Empty if no bank account |
| 2 | `Account` | `employee.primary_bank_account_id.acc_number` | Empty if no bank account |
| 3 | `Salary(total)` | Payslip line where `code = 'NET'` | Net salary |
| 4 | `Notice(month)` | Month name of the wizard's `month` (e.g. `July`) | The month being paid |
| 5 | `Name` | `employee.name` | |
| 6 | `ID number` | `employee.identification_id` | National ID |
| 7 | `address` | `employee.private_state_id.name` (from `hr.version` via `_inherits`) | Employee's state/province |
| 8 | `wage` | Payslip line where `code = 'BASIC'` | Basic wage |
| 9 | `house` | Payslip line where `code = 'HOUALLOW'` | Housing allowance (0 if absent) |
| 10 | `Others` | `slip.x_others` | Allowances − Deductions |
| 11 | `discount` | Total of payslip lines whose category code is `DED`, written as a **positive** number | e.g. `200.00` (per user's correct spec) |

Selection filter for the export: all `hr.payslip` whose `date_from` falls within the chosen month AND whose `state` is `validated` or `paid` (Odoo 19 states — NOT `done`).

## 4. Odoo 19 Compatibility Notes (per user's correct spec)

This module is built for Odoo 19 specifically. The following changes from the older "standard" spec are intentional:

| Field/Concept | Old (Odoo ≤18) | New (Odoo 19) — used in this module |
|---------------|----------------|--------------------------------------|
| Payslip states | `done`, `paid` | `validated`, `paid` |
| Employee bank account | `bank_account_id` | `primary_bank_account_id` (with `bank_account_id` fallback for safety) |
| Employee address | `address_home_id` (partner) | `private_state_id` (state/province via `hr.version` `_inherits`) |
| Housing rule code | `HOUSE` | `HOUALLOW` |
| View anchor on payslip form | `net_wage` (does not exist on the O19 form) | `note` |
| Menu parent xmlid | `hr_payroll.menu_hr_payroll_root` | `hr_work_entry_enterprise.menu_hr_payroll_root` |
| Filename prefix | `WPS_` | `Salary_` (per user's correct spec) |
| Discount sign | Negative (`-200`) | Positive (`200`) (per user's correct spec) |

## 5. Non-Functional Requirements
- **Performance:** Export of 1,000 payslips must complete in < 5 seconds.
- **Multi-company:** Inherited from `hr_payroll`.
- **Multi-currency:** Out of scope.
- **Mobile:** Not required.
- **i18n:** Arabic (required) + English.

## 6. Dependencies
| Module | Reason |
|--------|--------|
| base | always required |
| hr_payroll | We `_inherit = 'hr.payslip'` and use `hr_payroll.group_hr_payroll_user` for security |
| hr_work_entry_enterprise | Provides the Payroll root menu xmlid used as the menu parent |

## 7. Constraints
- NO Enterprise module dependencies on the model layer (only on the menu parent xmlid, which is harmless if the module is not installed — the menu will be parentless and the `post_init_hook` will reparent it).
- NO deprecated patterns (Odoo 19+).
- Author: Ibrahim Elmasry.

## 8. Acceptance Criteria
- [ ] Module installs without errors on Odoo 19
- [ ] 13+ tests pass
- [ ] Pre-flight validation: 0 errors
- [ ] Full validation: 0 errors, 0 warnings
- [ ] Documentation: 7+ files in docs/
- [ ] Arabic translations: 10+ entries
- [ ] Module icon: 256×256 PNG < 100KB
- [ ] `x_others` auto-fills on `compute_sheet()` and is editable afterwards
- [ ] CSV columns are in the exact order specified
- [ ] `discount` is positive
- [ ] CSV opens correctly in Excel (UTF-8 BOM)
- [ ] CSV filename uses `Salary_` prefix

## 9. Requirements Traceability Matrix

| # | Requirement | Model.Field | View | Test Method | Doc Section |
|---|-------------|-------------|------|-------------|-------------|
| 1 | x_others field exists | hr.payslip.x_others | view_hr_payslip_form_inherit_wps | test_01_others_field_exists | models.md §1 |
| 2 | x_others auto-computed on compute_sheet | hr.payslip._compute_x_others | — | test_02_others_auto_computed | models.md §2 |
| 3 | x_others = Allowances − Deductions | hr.payslip._compute_x_others | — | test_03_others_formula | models.md §2 |
| 4 | x_others manually editable | hr.payslip.x_others | view_hr_payslip_form_inherit_wps | test_04_others_editable | models.md §3 |
| 5 | Wizard month field required | wps.export.wizard.month | view_wps_export_wizard_form | test_05_wizard_month_required | wizards.md §1 |
| 6 | Wizard filters by month + state (validated/paid) | wps.export.wizard.action_export | — | test_06_wizard_filter | wizards.md §2 |
| 7 | Export raises if no payslips | wps.export.wizard.action_export | — | test_07_no_payslips_raises | wizards.md §3 |
| 8 | CSV has 11 columns in correct order | wps.export.wizard.action_export | — | test_08_csv_columns_order | wizards.md §4 |
| 9 | CSV discount is positive | wps.export.wizard.action_export | — | test_09_discount_positive | wizards.md §4 |
| 10 | CSV filename = Salary_<Month>_<Year>.csv | wps.export.wizard.action_export | — | test_10_filename | wizards.md §4 |
| 11 | CSV UTF-8 BOM for Excel/Arabic | wps.export.wizard.action_export | — | test_11_utf8_bom | wizards.md §4 |
| 12 | Bank/Account extracted from primary_bank_account_id | wps.export.wizard._get_bank_account | — | test_12_bank_account | wizards.md §5 |
| 13 | Address uses private_state_id (Odoo 19) | wps.export.wizard._get_employee_address | — | test_13_address_o19 | wizards.md §5 |
| 14 | Menu parented under hr_work_entry_enterprise Payroll root | wps_export_menus.xml | menu_wps_export | test_14_menu_parented | installation.md §1 |
| 15 | Security: only Payroll User can run | ir.model.access.csv | — | test_15_security | security.md §1 |
| 16 | Payslip states validated/paid (Odoo 19) | wps.export_wizard.action_export | — | test_16_o19_states | wizards.md §6 |
| 17 | Housing rule code = HOUALLOW | wps.export_wizard.action_export | — | test_17_houallow_code | wizards.md §6 |
