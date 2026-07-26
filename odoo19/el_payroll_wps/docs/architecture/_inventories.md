# Inventories — el_payroll_wps

## 1. Model Inventory

### 1.1 hr.payslip (inherited via _inherit)
| Field | Type | Method | State | Constraint |
|-------|------|--------|-------|------------|
| x_others | Float(digits='Payroll') | _compute_x_others() (called from compute_sheet override) | — | none |

| Method | Signature | Purpose |
|--------|-----------|---------|
| _get_line_amount_by_code | (self, line_code) → float | Return total of a single payslip line matched by code |
| _get_line_total_by_category | (self, category_code) → float | Sum totals of payslip lines for a category code |
| _compute_x_others | (self) → None | Set x_others = ALW − DED for each slip |
| compute_sheet | (self) → super() | Override: recompute sheet, then call _compute_x_others |

### 1.2 wps.export.wizard (new TransientModel)
| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| month | Date | Yes | fields.Date.context_today | Any date inside target month |

| Method | Signature | Purpose |
|--------|-----------|---------|
| _get_employee_address | (self, employee) → str | Return employee.private_state_id.name (Odoo 19) |
| _get_bank_account | (self, employee) → (bank_name, acc_number) | Extract bank from primary_bank_account_id (O19) with bank_account_id fallback |
| action_export | (self) → ir.actions.act_url | Build CSV, save as attachment, return download URL |

## 2. View Inventory

| View ID | Type | Model | Inherit | Fields Used | Buttons |
|---------|------|-------|---------|-------------|---------|
| view_hr_payslip_form_inherit_wps | form (inherit) | hr.payslip | hr_payroll.view_hr_payslip_form | x_others (added after note) | — |
| view_wps_export_wizard_form | form | wps.export.wizard | — | month | action_export, cancel |

## 3. Action Inventory

| Action ID | Name | res_model | view_mode | Target |
|-----------|------|-----------|-----------|--------|
| action_wps_export_wizard | WPS Export | wps.export.wizard | form | new (modal) |

## 4. Button → Method Map

| Button XML | Model | Method | Type |
|-----------|------|--------|------|
| action_export (in wizard footer) | wps.export.wizard | action_export | object |
| cancel (in wizard footer) | wps.export.wizard | (special=cancel) | special |

## 5. Menu Inventory

| Menu ID | Name | Parent | Action | Sequence |
|---------|------|--------|--------|----------|
| menu_wps_export | WPS Export | hr_work_entry_enterprise.menu_hr_payroll_root | action_wps_export_wizard | 100 |
