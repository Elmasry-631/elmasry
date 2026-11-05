# Sale Stock Restrict

- **المسار والإصدار:** `odoo18/sale_stock_restrict` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Module helps to restrict out of stock products

## المكونات المكتشفة

- Python: 5 file(s)
- XML: 2 file(s)

### نماذج وامتدادات Odoo

- ResConfigSettings: model _inherit
- SaleOrderLine: model _inherit
- SaleOrder: model _inherit

### الملفات المصدرية ذات الصلة

- `views/res_config_settings_views.xml`
- `views/sale_order.xml`
- `models/res_config_settings.py`
- `models/__init__.py`
- `models/sale_order.py`

### حقول معلنة

- `product_restriction (Boolean)`
- `check_stock (Selection)`
- `qty_available (Float)`
- `forecast_quantity (Float)`
- `onhand_check (Boolean)`
- `forecast_check (Boolean)`

### XML IDs

- `views/res_config_settings_views.xml::res_config_settings_view_form`
- `views/res_config_settings_views.xml::stock_product_restriction`
- `views/res_config_settings_views.xml::product_restriction`
- `views/res_config_settings_views.xml::out_of_stock_product_restriction`
- `views/sale_order.xml::view_order_form`