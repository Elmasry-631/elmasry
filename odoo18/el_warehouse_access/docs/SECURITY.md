# Warehouse-Based Access Control

- **المسار والإصدار:** `odoo18/el_warehouse_access` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Control user access based on warehouse assignments - Global backend security enforcement

## الصلاحيات والحماية المكتشفة

### ACL

- access_res_users_warehouse_user: model=base.model_res_users, group=el_warehouse_access.group_warehouse_user, read/write/create/delete=1/0/0/0
- access_res_users_warehouse_manager: model=base.model_res_users, group=el_warehouse_access.group_warehouse_manager, read/write/create/delete=1/1/0/0
- access_res_users_warehouse_admin: model=base.model_res_users, group=el_warehouse_access.group_warehouse_manager, read/write/create/delete=1/1/1/0
- access_stock_warehouse_warehouse_user: model=stock.model_stock_warehouse, group=el_warehouse_access.group_warehouse_user, read/write/create/delete=1/0/0/0
- access_stock_warehouse_warehouse_manager: model=stock.model_stock_warehouse, group=el_warehouse_access.group_warehouse_manager, read/write/create/delete=1/1/1/0
- access_stock_location_warehouse_user: model=stock.model_stock_location, group=el_warehouse_access.group_warehouse_user, read/write/create/delete=1/0/0/0
- access_stock_location_warehouse_manager: model=stock.model_stock_location, group=el_warehouse_access.group_warehouse_manager, read/write/create/delete=1/1/1/0
- access_stock_picking_warehouse_user: model=stock.model_stock_picking, group=el_warehouse_access.group_warehouse_user, read/write/create/delete=1/1/1/0
- access_stock_picking_warehouse_manager: model=stock.model_stock_picking, group=el_warehouse_access.group_warehouse_manager, read/write/create/delete=1/1/1/1
- access_stock_move_warehouse_user: model=stock.model_stock_move, group=el_warehouse_access.group_warehouse_user, read/write/create/delete=1/1/1/0
- access_stock_move_warehouse_manager: model=stock.model_stock_move, group=el_warehouse_access.group_warehouse_manager, read/write/create/delete=1/1/1/1
- access_stock_move_line_warehouse_user: model=stock.model_stock_move_line, group=el_warehouse_access.group_warehouse_user, read/write/create/delete=1/1/1/0
- access_stock_move_line_warehouse_manager: model=stock.model_stock_move_line, group=el_warehouse_access.group_warehouse_manager, read/write/create/delete=1/1/1/1
- access_stock_quant_warehouse_user: model=stock.model_stock_quant, group=el_warehouse_access.group_warehouse_user, read/write/create/delete=1/1/1/0
- access_stock_quant_warehouse_manager: model=stock.model_stock_quant, group=el_warehouse_access.group_warehouse_manager, read/write/create/delete=1/1/1/1
- access_stock_picking_type_warehouse_user: model=stock.model_stock_picking_type, group=el_warehouse_access.group_warehouse_user, read/write/create/delete=1/0/0/0
- access_stock_picking_type_warehouse_manager: model=stock.model_stock_picking_type, group=el_warehouse_access.group_warehouse_manager, read/write/create/delete=1/1/1/0
- access_stock_scrap_warehouse_user: model=stock.model_stock_scrap, group=el_warehouse_access.group_warehouse_user, read/write/create/delete=1/1/1/0
- access_stock_scrap_warehouse_manager: model=stock.model_stock_scrap, group=el_warehouse_access.group_warehouse_manager, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_warehouse_user`, `group_warehouse_manager`
- قواعد السجلات: `stock_picking_warehouse_rule`, `stock_move_warehouse_rule`, `stock_move_line_warehouse_rule`, `stock_quant_warehouse_rule`, `stock_location_warehouse_rule`, `stock_warehouse_visibility_rule`, `stock_picking_type_warehouse_rule`, `stock_scrap_warehouse_rule`, `sale_order_warehouse_rule`, `sale_order_line_warehouse_rule`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `tests/test_warehouse_access.py`
- `models/res_users_extension.py`
- `models/stock_quant_extension.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.