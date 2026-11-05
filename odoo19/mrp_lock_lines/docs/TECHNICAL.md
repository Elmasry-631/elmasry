# MRP Lock Lines

- **المسار والإصدار:** `odoo19/mrp_lock_lines` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Lock all component lines in Manufacturing Order except the last one

## المكونات المكتشفة

- Python: 4 file(s)
- XML: 1 file(s)

### نماذج وامتدادات Odoo

- StockMoveLine: model _inherit
- StockMove: model _inherit

### الملفات المصدرية ذات الصلة

- `views/mrp_production_views.xml`
- `models/__init__.py`
- `models/stock_move_line.py`

### حقول معلنة

- `is_last_line (Boolean)`
- `is_last_line (Boolean)`

### XML IDs

- `views/mrp_production_views.xml::view_mrp_production_lock_lines`