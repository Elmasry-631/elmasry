# Prevent Negative Stock

- **المسار والإصدار:** `odoo19/el_prevent_negative_stock` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Prevent negative stock — block stock moves AND sales orders when stock is insufficient

## المكونات المكتشفة

- Python: 8 file(s)
- XML: 5 file(s)

### نماذج وامتدادات Odoo

- ElStockAlert: model _name
- StockMove: model _inherit
- SaleOrder: model _inherit

### الملفات المصدرية ذات الصلة

- `views/el_stock_alert_views.xml`
- `views/menus.xml`
- `models/el_stock_alert.py`
- `models/__init__.py`
- `models/stock_move.py`
- `models/sale_order.py`
- `security/el_prevent_negative_stock_groups.xml`
- `security/ir.model.access.csv`

### حقول معلنة

- `name (Char)`
- `product_id (Many2one)`
- `location_id (Many2one)`
- `requested_qty (Float)`
- `available_qty (Float)`
- `move_id (Many2one)`
- `user_id (Many2one)`
- `state (Selection)`
- `company_id (Many2one)`

### XML IDs

- `views/el_stock_alert_views.xml::view_el_stock_alert_form`
- `views/el_stock_alert_views.xml::view_el_stock_alert_list`
- `views/el_stock_alert_views.xml::view_el_stock_alert_search`
- `views/el_stock_alert_views.xml::action_el_stock_alert`
- `views/menus.xml::menu_el_stock_alert_root`
- `views/menus.xml::menu_el_stock_alert_all`
- `data/mail_template.xml::mail_template_negative_stock_alert`
- `data/sequence.xml::seq_el_stock_alert`
- `security/el_prevent_negative_stock_groups.xml::module_category_el_prevent_negative_stock`
- `security/el_prevent_negative_stock_groups.xml::group_alert_user`
- `security/el_prevent_negative_stock_groups.xml::group_alert_manager`