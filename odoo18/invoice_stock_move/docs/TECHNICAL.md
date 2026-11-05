# Stock Picking From Invoice

- **المسار والإصدار:** `odoo18/invoice_stock_move` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Stock Picking From Customer/Supplier Invoice

## المكونات المكتشفة

- Python: 5 file(s)
- XML: 1 file(s)

### نماذج وامتدادات Odoo

- AccountMove: model _inherit
- AccountMoveLine: model _inherit

### الملفات المصدرية ذات الصلة

- `views/account_move_views.xml`
- `models/account_move.py`
- `models/__init__.py`
- `models/account_move_line.py`

### حقول معلنة

- `picking_count (Integer)`
- `invoice_picking_id (Many2one)`
- `picking_type_id (Many2one)`

### XML IDs

- `views/account_move_views.xml::view_move_form`