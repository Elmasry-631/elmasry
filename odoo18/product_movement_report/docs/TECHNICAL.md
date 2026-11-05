# Product Movement Lifecycle Report

- **المسار والإصدار:** `odoo18/product_movement_report` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Full movement history of a product/lot from first receipt until fully sold

## المكونات المكتشفة

- Python: 6 file(s)
- XML: 2 file(s)

### نماذج وامتدادات Odoo

- ProductMovementLine: model _name
- ProductMovementSummary: model _name
- ProductMovementWizard: model _name

### الملفات المصدرية ذات الصلة

- `report/product_movement_report.xml`
- `views/product_movement_views.xml`
- `models/product_movement_line.py`
- `models/__init__.py`
- `security/ir.model.access.csv`
- `wizard/product_movement_wizard.py`
- `wizard/__init__.py`

### حقول معلنة

- `wizard_id (Many2one)`
- `sequence (Integer)`
- `cycle_no (Integer)`
- `is_sold_out (Boolean)`
- `date (Datetime)`
- `reference (Char)`
- `picking_id (Many2one)`
- `origin (Char)`
- `move_type (Selection)`
- `location_id (Many2one)`
- `location_dest_id (Many2one)`
- `partner_id (Many2one)`
- `lot_id (Many2one)`
- `user_id (Many2one)`
- `qty_in (Float)`
- `qty_out (Float)`
- `balance (Float)`
- `cost (Float)`
- `uom_id (Many2one)`
- `wizard_id (Many2one)`
- `sequence (Integer)`
- `group (Selection)`
- `name (Char)`
- `qty (Float)`
- `cost (Float)`
- `is_bold (Boolean)`
- `product_id (Many2one)`
- `lot_id (Many2one)`
- `date_from (Date)`
- `date_to (Date)`
- `line_ids (One2many)`
- `summary_ids (One2many)`
- `company_id (Many2one)`
- `currency_id (Many2one)`
- `sales_revenue (Float)`
- `sales_cogs (Float)`
- `margin (Float)`
- `margin_pct (Float)`

### XML IDs

- `report/product_movement_report.xml::paperformat_product_movement`
- `report/product_movement_report.xml::action_report_product_movement`
- `report/product_movement_report.xml::report_product_movement`
- `views/product_movement_views.xml::product_movement_wizard_form`
- `views/product_movement_views.xml::action_product_movement_wizard`
- `views/product_movement_views.xml::product_movement_line_list`
- `views/product_movement_views.xml::product_movement_line_search`
- `views/product_movement_views.xml::product_movement_summary_list`
- `views/product_movement_views.xml::product_movement_wizard_result_form`
- `views/product_movement_views.xml::menu_product_movement_report`