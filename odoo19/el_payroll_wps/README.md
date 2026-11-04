# Payroll WPS Export

> Auto-generated documentation — 2026-07-26 07:11

## Description


Payroll WPS Export
===================
- Adds an "Others" field on the payslip (Allowances - Deductions, auto-computed,
  manually editable, informational only — does not affect Net Salary).
- Adds a "WPS Export" wizard/action that generates a CSV file for all payslips
  in a chosen month, with the columns required for WPS bank submission:
  Bank, Account, Salary (Net), Notice (Month), Name, ID Number, Address,
  Wage, House, Others, Discount (Deductions).
- Odoo 19 compatible: uses primary_bank_account_id, private_state_id,
  validated/paid states, HOUALLOW housing rule code.


## Module Info

| Property | Value |
|---|---|
| **Version** | 19.0.1.0.0 |
| **Author** | Ibrahim Elmasry |
| **License** | LGPL-3 |
| **Category** | Human Resources/Payroll |
| **Dependencies** | base, hr_payroll |

## Installation

```bash
# Copy module to addons directory
cp -r el_payroll_wps/ /opt/odoo/custom_addons/

# Install via CLI
odoo-bin -c odoo.conf -d mydb -i el_payroll_wps
```

## Module Statistics

| Metric | Count |
|---|---|
| Models | 0 |
| Views | 1 |
| Reports | 0 |
| Security Groups | 0 |
| Access Rules | 2 |

## Detailed Documentation

See [`docs/el_payroll_wps_technical.md`](docs/el_payroll_wps_technical.md) for full technical reference.
