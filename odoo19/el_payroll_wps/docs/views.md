# Views — el_payroll_wps

## 1. Inherited View: `view_hr_payslip_form_inherit_wps`

| Property | Value |
|----------|-------|
| **Type** | form (inherit) |
| **Model** | hr.payslip |
| **Inherits** | `hr_payroll.view_hr_payslip_form` |
| **XML ID** | `el_payroll_wps.view_hr_payslip_form_inherit_wps` |

### Modification
Inserts a `<label>` and `<field>` for `x_others` immediately after the `note` field.

```xml
<field name="note" position="after">
    <label for="x_others" string="Others"/>
    <field name="x_others"/>
</field>
```

### Why anchor on `note`?
In Odoo 19, the payslip form does not expose `net_wage` as a directly-addressable field in the inherited view (it lives inside a computed totals section). The `note` field is reliably present and is a sensible visual location for an informational field.

## 2. Wizard Form View: `view_wps_export_wizard_form`

| Property | Value |
|----------|-------|
| **Type** | form |
| **Model** | wps.export.wizard |
| **XML ID** | `el_payroll_wps.view_wps_export_wizard_form` |

### Layout
```xml
<form string="WPS Export">
    <group>
        <field name="month"/>
    </group>
    <footer>
        <button name="action_export" type="object" string="Export CSV" class="btn-primary"/>
        <button string="Cancel" class="btn-secondary" special="cancel"/>
    </footer>
</form>
```

## 3. Action: `action_wps_export_wizard`

| Property | Value |
|----------|-------|
| **Type** | ir.actions.act_window |
| **res_model** | wps.export.wizard |
| **view_mode** | form |
| **target** | new (modal) |

## 4. Menu: `menu_wps_export`

| Property | Value |
|----------|-------|
| **Type** | menuitem |
| **Action** | `action_wps_export_wizard` |
| **Parent** | `hr_work_entry_enterprise.menu_hr_payroll_root` (static) + `post_init_hook` safety net |
| **Sequence** | 100 |

## 5. View-Model Cross-Reference

| View | Field(s) Used | Method(s) Called |
|------|---------------|------------------|
| view_hr_payslip_form_inherit_wps | `x_others` (added), `note` (anchor) | — |
| view_wps_export_wizard_form | `month` | `action_export`, `special=cancel` |
