# Direct Print Auto

- **المسار والإصدار:** `odoo19/direct_print_auto` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Auto-print invoices, SOs, delivery slips and POs to the browser's print dialog when confirmed, plus a manual Direct Print button on each form.

## المكونات المكتشفة

- Python: 12 file(s)
- XML: 9 file(s)
- JavaScript/TypeScript: 1 file(s)

### نماذج وامتدادات Odoo

- PurchaseOrder: model _name
- ResConfigSettings: model _inherit
- AccountMove: model _name
- StockPicking: model _name
- SaleOrder: model _name
- DirectPrintMixin: model _name

### الملفات المصدرية ذات الصلة

- `views/stock_picking_views.xml`
- `views/res_config_settings_views.xml`
- `views/sale_order_views.xml`
- `views/client_actions.xml`
- `views/account_move_views.xml`
- `views/purchase_order_views.xml`
- `views/direct_print_menus.xml`
- `models/purchase_order.py`
- `models/res_config_settings.py`
- `models/account_move.py`
- `models/stock_picking.py`
- `models/__init__.py`
- `models/sale_order.py`
- `models/direct_print_mixin.py`
- `security/ir.model.access.csv`
- `security/direct_print_groups.xml`

### حقول معلنة

- `direct_print_invoice_auto (Boolean)`
- `direct_print_so_auto (Boolean)`
- `direct_print_picking_auto (Boolean)`
- `direct_print_po_auto (Boolean)`
- `direct_print_open_dialog (Boolean)`

### XML IDs

- `views/stock_picking_views.xml::view_picking_form_direct_print`
- `views/res_config_settings_views.xml::res_config_settings_view_form_direct_print`
- `views/res_config_settings_views.xml::direct_print_auto_settings`
- `views/sale_order_views.xml::view_order_form_direct_print`
- `views/client_actions.xml::action_direct_print_client`
- `views/account_move_views.xml::view_move_form_direct_print`
- `views/purchase_order_views.xml::purchase_order_form_direct_print`
- `views/direct_print_menus.xml::menu_direct_print_root`
- `security/direct_print_groups.xml::module_category_direct_print`
- `security/direct_print_groups.xml::res_groups_privilege_direct_print`
- `security/direct_print_groups.xml::group_direct_print_user`
- `security/direct_print_groups.xml::group_direct_print_manager`