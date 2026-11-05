# Product Traceability Dashboard

- **المسار والإصدار:** `odoo18/el_product_traceability_dashboard` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Product traceability dashboard with returns, scrap and manufacturing genealogy

## المكونات المكتشفة

- Python: 6 file(s)
- XML: 6 file(s)
- JavaScript/TypeScript: 1 file(s)

### نماذج وامتدادات Odoo

- TraceabilityMovementReport: model _name
- TraceabilityManufacturingReport: model _name
- ProductTraceabilityReport: model _name
- ProductTraceabilityManufacturing: model _name
- ProductTraceabilityDashboard: model _name

### الملفات المصدرية ذات الصلة

- `report/traceability_report_templates.xml`
- `report/__init__.py`
- `report/traceability_reports.py`
- `views/product_traceability_report_views.xml`
- `views/product_traceability_views.xml`
- `views/product_traceability_menus.xml`
- `models/traceability_report.py`
- `models/__init__.py`
- `security/security.xml`
- `security/ir.model.access.csv`

### حقول معلنة

- `date (Datetime)`
- `company_id (Many2one)`
- `warehouse_id (Many2one)`
- `product_id (Many2one)`
- `product_tmpl_id (Many2one)`
- `categ_id (Many2one)`
- `lot_id (Many2one)`
- `move_line_id (Many2one)`
- `move_id (Many2one)`
- `picking_id (Many2one)`
- `production_id (Many2one)`
- `purchase_order_id (Many2one)`
- `purchase_line_id (Many2one)`
- `sale_order_id (Many2one)`
- `partner_id (Many2one)`
- `location_id (Many2one)`
- `location_dest_id (Many2one)`
- `uom_id (Many2one)`
- `operation_type (Selection)`
- `reference (Char)`
- `source_document (Char)`
- `quantity (Float)`
- `signed_quantity (Float)`
- `unit_cost (Float)`
- `total_value (Float)`
- `purchase_unit_price (Float)`
- `purchase_total_value (Float)`
- `date (Datetime)`
- `company_id (Many2one)`
- `production_id (Many2one)`
- `finished_product_id (Many2one)`
- `finished_uom_id (Many2one)`
- `finished_qty (Float)`
- `component_product_id (Many2one)`
- `component_uom_id (Many2one)`
- `component_qty (Float)`
- `component_value (Float)`
- `state (Char)`
- `reference (Char)`
- `company_id (Many2one)`
- `date_from (Date)`
- `date_to (Date)`

### XML IDs

- `report/traceability_report_templates.xml::action_report_traceability_movement_pdf`
- `report/traceability_report_templates.xml::movement_pdf_template`
- `report/traceability_report_templates.xml::action_report_traceability_manufacturing_pdf`
- `report/traceability_report_templates.xml::manufacturing_pdf_template`
- `views/product_traceability_report_views.xml::view_product_traceability_report_list`
- `views/product_traceability_report_views.xml::view_product_traceability_report_search`
- `views/product_traceability_report_views.xml::view_product_traceability_report_pivot`
- `views/product_traceability_report_views.xml::view_product_traceability_report_graph`
- `views/product_traceability_report_views.xml::action_product_traceability_report`
- `views/product_traceability_report_views.xml::view_product_traceability_manufacturing_list`
- `views/product_traceability_report_views.xml::view_product_traceability_manufacturing_search`
- `views/product_traceability_report_views.xml::action_product_traceability_manufacturing`
- `views/product_traceability_views.xml::action_product_traceability_dashboard_client`
- `views/product_traceability_menus.xml::menu_product_traceability_root`
- `views/product_traceability_menus.xml::menu_product_traceability_dashboard`
- `views/product_traceability_menus.xml::menu_product_traceability_movements`
- `views/product_traceability_menus.xml::menu_product_traceability_manufacturing`
- `security/security.xml::group_product_traceability_user`
- `security/security.xml::group_product_traceability_manager`