# Purchase Actual Quantity

- **المسار والإصدار:** `odoo18/el_purchase_actual_qty` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Actual purchase quantity with preserved value, dashboard and reporting

## المكونات المكتشفة

- Python: 10 file(s)
- XML: 6 file(s)
- JavaScript/TypeScript: 1 file(s)

### نماذج وامتدادات Odoo

- ResConfigSettings: model _inherit
- PurchaseActualReport: model _name
- PurchaseOrderLine: model _inherit

### الملفات المصدرية ذات الصلة

- `controllers/__init__.py`
- `controllers/purchase_actual_export.py`
- `views/res_config_settings_views.xml`
- `views/purchase_actual_report_views.xml`
- `views/purchase_order_views.xml`
- `models/res_config_settings.py`
- `models/purchase_actual_report.py`
- `models/__init__.py`
- `models/purchase_order_line.py`
- `security/ir.model.access.csv`

### حقول معلنة

- `actual_qty_allow_over (Boolean)`
- `variance_warning_percent (Float)`
- `variance_critical_percent (Float)`
- `actual_qty_required (Boolean)`
- `order_id (Many2one)`
- `order_name (Char)`
- `order_date (Datetime)`
- `partner_id (Many2one)`
- `product_id (Many2one)`
- `product_tmpl_id (Many2one)`
- `product_category_id (Many2one)`
- `company_id (Many2one)`
- `currency_id (Many2one)`
- `buyer_id (Many2one)`
- `ordered_qty (Float)`
- `actual_qty (Float)`
- `variance_qty (Float)`
- `variance_percent (Float)`
- `purchase_value (Monetary)`
- `effective_unit_cost (Monetary)`
- `variance_status (Selection)`
- `actual_qty (Float)`
- `effective_price_unit (Float)`
- `variance_qty (Float)`
- `variance_percent (Float)`

### XML IDs

- `reports/purchase_actual_report.xml::action_purchase_actual_pdf`
- `reports/purchase_actual_report.xml::purchase_actual_report_document`
- `views/res_config_settings_views.xml::res_config_settings_view_purchase_actual_qty`
- `views/purchase_actual_report_views.xml::purchase_actual_report_list`
- `views/purchase_actual_report_views.xml::purchase_actual_report_pivot`
- `views/purchase_actual_report_views.xml::purchase_actual_report_graph`
- `views/purchase_actual_report_views.xml::purchase_actual_report_search`
- `views/purchase_order_views.xml::purchase_order_form_actual_qty`
- `data/ir_actions.xml::action_purchase_actual_dashboard`
- `data/ir_actions.xml::action_purchase_actual_report`
- `data/ir_actions.xml::menu_purchase_actual_dashboard`
- `data/ir_actions.xml::menu_purchase_actual_report`