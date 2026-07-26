# Model Design — el_payroll_wps

## 1. Models Overview

The module is intentionally thin: ONE inherited model (`hr.payslip`) and ONE new TransientModel (`wps.export.wizard`). No persistent configuration model — the wizard's `month` field is the only parameter and it lives on the transient.

### 1.1 hr.payslip — extension

**Why inherit instead of a new model?** The `x_others` value is a derived property of a payslip. Storing it on the payslip itself means:
- It is visible on the payslip form (after `note`).
- It is recomputed automatically when the sheet is recomputed.
- It survives across the payslip's lifecycle without extra joins.

**Why `Float` and not `Monetary`?** `hr.payslip` does not carry a `currency_id` field directly on the model in a way that's safe to reference for a custom Monetary field across Odoo 18/19. `Float(digits='Payroll')` matches the precision used by every other amount on the payslip.

**Why the `x_` prefix?** The `x_` prefix is Odoo's standard convention for "custom" fields added on top of a model — it makes the custom origin instantly visible.

### 1.2 wps.export.wizard — new TransientModel

**Why a wizard and not a direct server action?** The export needs ONE input (the month). A TransientModel wizard is the Odoo-idiomatic way to ask the user for that input via a modal, validate it, and then perform the action.

**Why `month` is a `Date` and not a `Selection`?** A Date picker is faster to use (one click) and survives year boundaries automatically.

## 2. Methods Design

### 2.1 hr.payslip methods

#### `_get_line_amount_by_code(self, line_code) -> float`
- Single-payslip helper (`ensure_one`).
- Filters `self.line_ids` by `code == line_code`, returns `line.total` of the first match or `0.0`.
- Used by the wizard for `NET`, `BASIC`, `HOUALLOW`.
- Defensive: returns `0.0` if the rule code does not exist on the payslip.

#### `_get_line_total_by_category(self, category_code) -> float`
- Single-payslip helper (`ensure_one`).
- Sums `line.total` for every line whose `category_id.code == category_code`.
- Used both for computing `x_others` (`ALW` − `DED`) and for the CSV `discount` column (`DED`).

#### `_compute_x_others(self) -> None`
- NOT a `@api.depends` compute — it is called explicitly from `compute_sheet()` after the parent method runs.
- This is deliberate: an `@api.depends` compute would overwrite manual edits every time the user saves the form. Calling it only from `compute_sheet()` means manual edits survive until the next recompute.
- Sets `x_others = ALW_total − DED_total` for each slip.

#### `compute_sheet(self) -> super()`
- Override: `res = super().compute_sheet()`, then `self._compute_x_others()`, then `return res`.

### 2.2 wps.export.wizard methods

#### `_get_employee_address(self, employee) -> str`
- Odoo 19: reads `employee.private_state_id` directly (a Many2one to `res.country.state` provided by `hr.version` via `_inherits`).
- Returns `employee.private_state_id.name` if set, otherwise `''`.
- This replaces the old `work_contact_id` / `address_home_id` partner lookup — per the user's correct Odoo 19 spec.

#### `_get_bank_account(self, employee) -> (bank_name, acc_number)`
- Odoo 19: prefers `employee.primary_bank_account_id` (the new field), with `employee.bank_account_id` as a defensive fallback for any 19.x version where the rename has not landed.
- Returns the bank's `name` and the account `acc_number`.
- Returns `('', '')` if the employee has no bank account on file.

#### `action_export(self) -> ir.actions.act_url`
- Computes `date_from` (1st of month) and `date_to` (1st of next month) from `self.month`.
- Searches `hr.payslip` where `date_from ∈ [date_from, date_to)` AND `state ∈ ('validated', 'paid')` — **Odoo 19 states** (NOT `done`).
- Raises `UserError` if no payslips match.
- Builds the CSV in memory (`io.StringIO` + `csv.writer`).
- Writes the header row + one row per payslip.
- Encodes as `utf-8-sig` (BOM) for Excel/Arabic compatibility.
- Stores the bytes as an `ir.attachment` and returns `ir.actions.act_url` pointing at `/web/content/<id>?download=true`.
- Filename: `Salary_<Month>_<Year>.csv` (per user's correct spec — NOT `WPS_`).

## 3. Constraints & Indexes
- No `models.Constraint` needed.
- No extra indexes needed — `hr.payslip.date_from` and `hr.payslip.state` are already indexed by `hr_payroll`.

## 4. Inheritance Strategy
- `hr.payslip`: classic `_inherit = 'hr.payslip'` (no `_name` → extends in place).
- `wps.export.wizard`: brand new `_name = 'wps.export.wizard'` with `_description`.
