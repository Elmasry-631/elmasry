# Stock Movement Report

- **المسار والإصدار:** `odoo19/ie_stock_movement_report` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** PDF report of inventory movements with opening/closing balance and running value.

## المكونات المكتشفة

- Python: 10 file(s)
- XML: 4 file(s)

### نماذج وامتدادات Odoo

- StockMovementReportHandler: model _name
- StockMovementReport: model _name
- StockMovementReportWizard: model _name

### الملفات المصدرية ذات الصلة

- `views/stock_movement_report_menu.xml`
- `models/__init__.py`
- `models/stock_movement_report.py`
- `security/ir.module.privilege.xml`
- `security/ir.model.access.csv`
- `wizard/__init__.py`
- `wizard/stock_movement_report_wizard_views.xml`

### حقول معلنة

- `date_from (Date)`
- `date_to (Date)`
- `warehouse_id (Many2one)`
- `location_id (Many2one)`
- `product_id (Many2one)`
- `categ_id (Many2one)`

### XML IDs

- `reports/stock_movement_report_template.xml::report_stock_movement_document`
- `reports/stock_movement_report_template.xml::paperformat_stock_movement_landscape`
- `reports/stock_movement_report_template.xml::action_report_stock_movement`
- `views/stock_movement_report_menu.xml::menu_stock_movement_report_root`
- `security/ir.module.privilege.xml::privilege_stock_movement_report`
- `security/ir.module.privilege.xml::group_stock_movement_report_user`
- `security/ir.module.privilege.xml::group_stock_movement_report_manager`
- `wizard/stock_movement_report_wizard_views.xml::view_stock_movement_report_wizard_form`
- `wizard/stock_movement_report_wizard_views.xml::action_stock_movement_report_wizard`