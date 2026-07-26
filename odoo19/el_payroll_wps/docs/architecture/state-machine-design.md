# State Machine Design — el_payroll_wps

## 1. No New State Machines

This module does NOT introduce any new state machine:

- `hr.payslip` already has its own state machine owned by `hr_payroll`. In Odoo 19, the relevant states are `draft`, `verify`, `validated`, `paid`, `cancel`. We do not modify this machine — we only filter on `validated` and `paid` in the wizard's search domain.
- `wps.export.wizard` is a single-step transient: the user opens the wizard, picks a month, clicks "Export CSV", the file downloads, and the wizard record is auto-purged.

## 2. Lifecycle Hooks Used

| Hook | Where | Purpose |
|------|-------|---------|
| `compute_sheet()` override | hr.payslip | Recompute `x_others` whenever the sheet is recomputed |
| `post_init_hook` | module __init__.py | Reparent `menu_wps_export` under the actual Payroll root menu at install time, as a safety net in case the static `parent="hr_work_entry_enterprise.menu_hr_payroll_root"` reference is missing on a custom build |

## 3. Why No State Machine on the Wizard
A state machine on a transient wizard is over-engineering — there is no "review → submit → approve" flow. The wizard is purely "fill one field, click one button, get one file".
