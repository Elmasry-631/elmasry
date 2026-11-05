# Stock Split Transfer

- **المسار والإصدار:** `odoo18/stock_split_transfer` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Two-step internal transfers with per-user location visibility

## المكونات المكتشفة

- Python: 5 file(s)
- XML: 1 file(s)

### نماذج وامتدادات Odoo

- StockPicking: model _inherit
- ResUsers: model _inherit

### الملفات المصدرية ذات الصلة

- `views/views.xml`
- `models/stock_picking.py`
- `models/__init__.py`
- `models/res_users.py`

### حقول معلنة

- `split_parent_id (Many2one)`
- `split_child_id (Many2one)`
- `split_visible (Boolean)`
- `is_split_transfer (Boolean)`
- `allowed_location_ids (Many2many)`

### XML IDs

- `views/views.xml::view_users_form_split_transfer`
- `views/views.xml::view_picking_form_split_transfer`
- `views/views.xml::view_picking_list_split_transfer`
- `views/views.xml::view_picking_search_split_transfer`