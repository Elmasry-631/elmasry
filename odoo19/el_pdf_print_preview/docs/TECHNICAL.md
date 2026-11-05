# PDF Print Preview

- **المسار والإصدار:** `odoo19/el_pdf_print_preview` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Preview PDF reports in-browser before printing — no download needed

## المكونات المكتشفة

- Python: 10 file(s)
- XML: 4 file(s)
- JavaScript/TypeScript: 7 file(s)

### نماذج وامتدادات Odoo

- IrHttp: model _inherit
- ResUsers: model _inherit
- IrActionsReport: model _inherit

### الملفات المصدرية ذات الصلة

- `report/ir_actions_report_templates.xml`
- `report/ir_actions_report.xml`
- `controllers/main.py`
- `controllers/__init__.py`
- `views/res_users_views.xml`
- `models/ir_http.py`
- `models/__init__.py`
- `models/res_users.py`
- `models/ir_actions_report.py`
- `security/ir.model.access.csv`

### حقول معلنة

- `preview_print (Boolean)`
- `automatic_printing (Boolean)`

### XML IDs

- `report/ir_actions_report_templates.xml::report_error_catcher`
- `report/ir_actions_report.xml::action_report_error_catcher`
- `views/res_users_views.xml::view_users_pdf_preview_form`