# Inventory All In One Report Generator

- **المسار والإصدار:** `odoo19/inventory_report_generator` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Dynamic Inventory Report Generator for Odoo 17

## المكونات المكتشفة

- Python: 8 file(s)
- XML: 3 file(s)
- JavaScript/TypeScript: 1 file(s)

### نماذج وامتدادات Odoo

- InventoryPDFReport: model _name
- DynamicInventoryReport: model _name

### الملفات المصدرية ذات الصلة

- `report/inventory_pdf_report_templates.xml`
- `report/inventory_pdf_report.py`
- `report/__init__.py`
- `controllers/inventory_report_generator.py`
- `controllers/__init__.py`
- `views/inventory_report_views.xml`
- `models/dynamic_inventory_report.py`
- `models/__init__.py`
- `security/ir.model.access.csv`

### حقول معلنة

- `purchase_report (Char)`
- `date_from (Datetime)`
- `date_to (Datetime)`
- `report_type (Selection)`

### XML IDs

- `report/inventory_pdf_report_templates.xml::action_report_inventory_all_in_one`
- `report/inventory_pdf_report_templates.xml::inventory_pdf_report`
- `report/inventory_pdf_report_templates.xml::report_by_transfers`
- `report/inventory_pdf_report_templates.xml::report_by_categories`
- `report/inventory_pdf_report_templates.xml::report_by_warehouse`
- `report/inventory_pdf_report_templates.xml::report_by_location`
- `views/inventory_report_views.xml::inventory_all_report_action`
- `views/inventory_report_views.xml::inventory_all_in_one_report`
- `static/src/xml/inventory_report_templates.xml::pdf`
- `static/src/xml/inventory_report_templates.xml::xlsx`
- `static/src/xml/inventory_report_templates.xml::date_chose`
- `static/src/xml/inventory_report_templates.xml::date_from`
- `static/src/xml/inventory_report_templates.xml::date_to`
- `static/src/xml/inventory_report_templates.xml::dates`
- `static/src/xml/inventory_report_templates.xml::dropdownMenuLink`
- `static/src/xml/inventory_report_templates.xml::selection`
- `static/src/xml/inventory_report_templates.xml::report_res`
- `static/src/xml/inventory_report_templates.xml::apply_filter`
- `static/src/xml/inventory_report_templates.xml::table_toggle_btn`