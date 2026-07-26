# Models — el_payroll_wps

## 1. hr.payslip (extended)

### 1.1 Fields added

| Field | Type | Digits | Help | Stored |
|-------|------|--------|------|--------|
| `x_others` | Float | `Payroll` precision | Auto = Allowances − Deductions; manually editable | ✅ Yes |

### 1.2 Methods added

#### `_get_line_amount_by_code(self, line_code) → float`
Returns `total` of the first payslip line whose `code` matches. Returns `0.0` if no line matches.

Used by:
- `wps.export.wizard.action_export()` for `NET`, `BASIC`, `HOUALLOW`

#### `_get_line_total_by_category(self, category_code) → float`
Sums `total` across all payslip lines whose `category_id.code` matches. Returns `0.0` if no lines match.

Used by:
- `_compute_x_others()` for `ALW` and `DED`
- `wps.export_wizard.action_export()` for `DED` (the `discount` column)

#### `_compute_x_others(self) → None`
For each slip, sets `x_others = _get_line_total_by_category('ALW') − _get_line_total_by_category('DED')`.

Called explicitly from `compute_sheet()` — NOT a `@api.depends` compute, so manual edits are not overwritten on form save.

#### `compute_sheet(self) → super().compute_sheet()`
Override: calls `super()`, then `_compute_x_others()`, then returns the original result.

### 1.3 Why `x_others` is not `@api.depends`
An `@api.depends` compute would trigger on every save and wipe the HR officer's manual override. The explicit-call approach lets the override survive until the next `compute_sheet()`.

## 2. wps.export.wizard (new TransientModel)

### 2.1 Fields

| Field | Type | Required | Default | Help |
|-------|------|----------|---------|------|
| `month` | Date | ✅ Yes | `fields.Date.context_today` | Pick any date within the month |

### 2.2 Methods

#### `_get_employee_address(self, employee) → str`
- Odoo 19: reads `employee.private_state_id` (a `res.country.state` provided by `hr.version` via `_inherits`).
- Returns `private_state_id.name` or `''`.

#### `_get_bank_account(self, employee) → (bank_name, acc_number)`
- Odoo 19: prefers `employee.primary_bank_account_id`, with `bank_account_id` fallback.
- Returns `('', '')` if no bank account is set.

#### `action_export(self) → ir.actions.act_url`
1. Compute `date_from = month.replace(day=1)` and `date_to = first day of next month`.
2. Search `hr.payslip` where `date_from ∈ [date_from, date_to)` AND `state ∈ ('validated', 'paid')`.
3. If no payslips → raise `UserError`.
4. Build CSV with `csv.writer` and the 11-column header.
5. For each slip: extract employee, bank account, line totals, address, and write a row.
6. Encode as `utf-8-sig` (BOM).
7. Create `ir.attachment` with `mimetype='text/csv'`.
8. Return `ir.actions.act_url` → `/web/content/<id>?download=true`.
9. Filename: `Salary_<Month>_<Year>.csv`.

### 2.3 Why TransientModel
A wizard is the Odoo-idiomatic way to ask the user for a single input (the month). Records auto-purge after a few hours.

## 3. Constraints & Indexes
None added.

## 4. Inheritance Map

```
hr.payslip (hr_payroll)
    └── _inherit (el_payroll_wps)
        └── x_others field + 4 methods added

wps.export.wizard (el_payroll_wps)
    └── _name (brand new TransientModel)
        └── 1 field + 3 methods
```
