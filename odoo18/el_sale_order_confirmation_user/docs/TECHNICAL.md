# Sale Order Confirmation User

- **المسار والإصدار:** `odoo18/el_sale_order_confirmation_user` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track which user actually confirmed each sales order

## المكونات المكتشفة

- Python: 6 file(s)
- XML: 1 file(s)

### نماذج وامتدادات Odoo

- SaleOrder: model _inherit

### الملفات المصدرية ذات الصلة

- `views/sale_order_views.xml`
- `models/__init__.py`
- `models/sale_order.py`

### حقول معلنة

- `confirmed_by_id (Many2one)`

### XML IDs

- `views/sale_order_views.xml::view_order_form_inherit_confirmed_by`
- `views/sale_order_views.xml::view_sales_order_filter_inherit_confirmed_by`