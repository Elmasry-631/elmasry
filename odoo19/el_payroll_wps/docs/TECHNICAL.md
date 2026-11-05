# Payroll WPS Export

- **المسار والإصدار:** `odoo19/el_payroll_wps` — Odoo 19
- **إصدار الحزمة:** `19.0.1.2.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Adds an 'Others' field to payslips and the bank salary file export (WPS)

## المكونات المكتشفة

- Python: 9 file(s)
- XML: 2 file(s)

### نماذج وامتدادات Odoo

- HrPayslip: model _inherit
- WpsExportWizard: model _name

### الملفات المصدرية ذات الصلة

- `views/hr_payslip_views.xml`
- `models/hr_payslip.py`
- `models/__init__.py`
- `security/ir.model.access.csv`
- `wizard/wps_export_wizard_views.xml`
- `wizard/wps_export_wizard.py`
- `wizard/__init__.py`

### حقول معلنة

- `x_others (Float)`
- `month (Date)`
- `bank_code (Char)`
- `payslip_count (Integer)`
- `employee_count (Integer)`
- `total_net (Float)`
- `issues (Html)`
- `has_blocking_issue (Boolean)`
- `state (Selection)`
- `file_data (Binary)`
- `file_name (Char)`

### XML IDs

- `views/hr_payslip_views.xml::view_hr_payslip_form_inherit_wps`
- `wizard/wps_export_wizard_views.xml::view_wps_export_wizard_form`
- `wizard/wps_export_wizard_views.xml::action_wps_export_wizard`
- `wizard/wps_export_wizard_views.xml::menu_wps_export`