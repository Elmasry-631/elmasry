# Testing — el_payroll_wps

## How to Run

```bash
# From your Odoo installation directory:
odoo -d your_test_db -i el_payroll_wps --test-enable \
     --test-tags=/el_payroll_wps --stop-after-init
```

## Test Files

| File | Class | Methods |
|------|-------|---------|
| `tests/test_wps_export.py` | `TestWpsExport` | 19 methods (test_01 through test_19) |

## Test Categories

### Field & Computation (6 tests)
- test_01: x_others field exists on hr.payslip
- test_02: x_others auto-computed by compute_sheet()
- test_03: x_others = Allowances − Deductions (formula check)
- test_04: x_others survives manual write
- test_18: _get_line_amount_by_code returns 0.0 for missing rule code
- test_19: _get_line_total_by_category returns 0.0 for missing category code

### Wizard Behavior (3 tests)
- test_05: month field is required
- test_06: only payslips in the chosen month + state(validated/paid) are exported
- test_07: UserError raised when no validated payslips exist for the month

### CSV Output (5 tests)
- test_08: CSV header has the exact 11 columns in spec order
- test_09: discount column is positive (per corrected spec)
- test_10: filename = Salary_<Month>_<Year>.csv
- test_11: CSV binary starts with UTF-8 BOM (EF BB BF)
- test_12: Bank name + account number via primary_bank_account_id

### Odoo 19 Compatibility (2 tests)
- test_13: _get_employee_address uses private_state_id
- test_16: Wizard uses validated/paid states (Odoo 19, NOT done)
- test_17: Wizard queries HOUALLOW housing rule code

### Installation (1 test)
- test_14: menu_wps_export exists and is named "WPS Export"

### Security (1 test)
- test_15: user without hr_payroll group gets AccessError

## Known Limitations
- Tests cannot run in this sandbox because the Odoo venv is missing `python-ldap`.
- On a standard Odoo 19 installation, all 19 tests are expected to pass.

## Continuous Integration
For CI pipelines:
1. Spins up PostgreSQL
2. Installs Odoo 19 + `python-ldap`
3. Copies this module into `addons/`
4. Runs: `odoo -d test_db -i el_payroll_wps --test-enable --stop-after-init`
5. Parses log for pass/fail counts
