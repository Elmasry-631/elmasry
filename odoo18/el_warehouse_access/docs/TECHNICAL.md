# Warehouse-Based Access Control

- **المسار والإصدار:** `odoo18/el_warehouse_access` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Control user access based on warehouse assignments - Global backend security enforcement

## المكونات المكتشفة

- Python: 13 file(s)
- XML: 5 file(s)

### نماذج وامتدادات Odoo

- ResUsers: model _inherit
- StockScrap: model _inherit
- StockMove: model _inherit
- StockQuant: model _inherit
- StockLocation: model _inherit
- StockPickingType: model _inherit
- SaleOrder: model _inherit
- StockPicking: model _inherit

### الملفات المصدرية ذات الصلة

- `views/menu.xml`
- `views/stock_picking_views.xml`
- `views/res_users_views.xml`
- `models/res_users_extension.py`
- `models/stock_scrap_extension.py`
- `models/__init__.py`
- `models/stock_move_extension.py`
- `models/stock_quant_extension.py`
- `models/stock_location_extension.py`
- `models/stock_picking_type_extension.py`
- `models/sale_order_extension.py`
- `models/stock_picking_extension.py`
- `security/groups.xml`
- `security/ir.model.access.csv`
- `security/ir.rule.xml`

### حقول معلنة

- `warehouse_ids (Many2many)`
- `warehouse_count (Integer)`
- `is_user_accessible (Boolean)`
- `warehouse_id (Many2one)`
- `is_user_accessible (Boolean)`
- `is_user_accessible (Boolean)`
- `warehouse_id (Many2one)`
- `is_user_accessible (Boolean)`
- `warehouse_id (Many2one)`
- `is_user_accessible (Boolean)`
- `warehouse_id (Many2one)`
- `is_user_accessible (Boolean)`
- `user_warehouse_count (Integer)`
- `is_single_warehouse_user (Boolean)`
- `location_dest_id (Many2one)`

### XML IDs

- `views/menu.xml::action_warehouse_access_matrix`
- `views/menu.xml::view_warehouse_access_pivot`
- `views/menu.xml::menu_warehouse_access_root`
- `views/menu.xml::menu_warehouse_user_assignment`
- `views/menu.xml::menu_warehouse_access_report`
- `views/stock_picking_views.xml::view_picking_form_warehouse_access`
- `views/res_users_views.xml::view_users_form_warehouse_access`
- `security/groups.xml::module_category_warehouse_access`
- `security/groups.xml::group_warehouse_user`
- `security/groups.xml::group_warehouse_manager`
- `security/ir.rule.xml::stock_picking_warehouse_rule`
- `security/ir.rule.xml::stock_move_warehouse_rule`
- `security/ir.rule.xml::stock_move_line_warehouse_rule`
- `security/ir.rule.xml::stock_quant_warehouse_rule`
- `security/ir.rule.xml::stock_location_warehouse_rule`
- `security/ir.rule.xml::stock_warehouse_visibility_rule`
- `security/ir.rule.xml::stock_picking_type_warehouse_rule`
- `security/ir.rule.xml::stock_scrap_warehouse_rule`
- `security/ir.rule.xml::sale_order_warehouse_rule`
- `security/ir.rule.xml::sale_order_line_warehouse_rule`