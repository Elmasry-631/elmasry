# Data Flow — el_payroll_wps

## 1. Pay Slip Computation Flow (x_others)

```
HR Officer clicks "Compute Sheet" on hr.payslip
        │
        ▼
hr_payroll.HrPayslip.compute_sheet()
        │  (super) — populates line_ids with NET/BASIC/HOUALLOW/ALW/DED lines
        ▼
el_payroll_wps.HrPayslip.compute_sheet() override
        │
        ▼
self._compute_x_others()
        │
        ├── _get_line_total_by_category('ALW')  →  sum(line.total for cat.code == 'ALW')
        ├── _get_line_total_by_category('DED')  →  sum(line.total for cat.code == 'DED')
        │
        ▼
slip.x_others = ALW_total − DED_total
        │
        ▼
x_others displayed on payslip form (after `note`)
        │
        ▼
HR Officer may manually edit x_others — value persists until next compute_sheet()
```

## 2. WPS Export Flow (CSV)

```
HR Officer opens Payroll → WPS Export menu
        │
        ▼
Wizard form opens (modal) — month defaults to today
        │
        ▼
User picks any date inside target month → clicks "Export CSV"
        │
        ▼
wps.export.wizard.action_export()
        │
        ├── date_from = month.replace(day=1)
        ├── date_to   = first day of next month
        │
        ├── search hr.payslip where date_from ∈ [date_from, date_to)
        │                            AND state ∈ ('validated', 'paid')   ← Odoo 19
        │
        ├── if empty → raise UserError("No validated payslips for <Month Year>")
        │
        ├── for each slip:
        │     ├── employee = slip.employee_id
        │     ├── bank_name, acc_number  = _get_bank_account(employee)
        │     │     ├── try primary_bank_account_id (Odoo 19)
        │     │     └── fallback to bank_account_id
        │     ├── net_total   = slip._get_line_amount_by_code('NET')
        │     ├── wage        = slip._get_line_amount_by_code('BASIC')
        │     ├── house       = slip._get_line_amount_by_code('HOUALLOW')   ← Odoo 19 code
        │     ├── deductions  = abs(slip._get_line_total_by_category('DED'))
        │     └── write CSV row:
        │           [bank_name, acc_number, net_total, month_name,
        │            employee.name, employee.identification_id,
        │            employee.private_state_id.name or '',
        │            wage, house, slip.x_others, deductions]   ← positive
        │
        ├── csv_bytes = buffer.getvalue().encode('utf-8-sig')  ← BOM for Excel
        ├── filename  = "Salary_<Month>_<Year>.csv"            ← per user spec
        │
        ├── ir.attachment.create({name, type='binary', datas=base64(csv_bytes),
        │                        mimetype='text/csv'})
        │
        └── return ir.actions.act_url → /web/content/<id>?download=true
                │
                ▼
        Browser downloads the CSV file
```

## 3. Menu Re-parenting Flow (post_init_hook — safety net)

The static XML already sets `parent="hr_work_entry_enterprise.menu_hr_payroll_root"`.
The `post_init_hook` is a runtime safety net: if that xmlid does not exist on the
target database (e.g. a custom build), the hook searches for a root menu named
"Payroll" and reparents the WPS Export menu under it.

```
Module installation completes
        │
        ▼
post_init_hook(env)
        │
        ├── env.ref('el_payroll_wps.menu_wps_export')
        │
        ├── search ir.ui.menu where parent_id=False AND name='Payroll'
        │   (fallback: name ilike 'payroll')
        │
        └── if found: menu_wps_export.write({parent_id: payroll_root.id})
```

## 4. Data Sources Summary

| CSV Column | Source Table | Source Field |
|-----------|--------------|--------------|
| Bank | res.bank | name (via employee.primary_bank_account_id.bank_id) |
| Account | res.partner.bank | acc_number |
| Salary(total) | hr.payslip.line | total (where code='NET') |
| Notice(month) | (computed) | strftime('%B') of wizard.month |
| Name | hr.employee | name |
| ID number | hr.employee | identification_id |
| address | res.country.state (via hr.version) | name (via employee.private_state_id) |
| wage | hr.payslip.line | total (where code='BASIC') |
| house | hr.payslip.line | total (where code='HOUALLOW') |
| Others | hr.payslip | x_others |
| discount | hr.payslip.line | sum(total) where category.code='DED' (positive) |
