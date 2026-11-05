# Warehouse-Based Access Control

- **المسار والإصدار:** `odoo18/el_warehouse_access` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Control user access based on warehouse assignments - Global backend security enforcement

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Warehouse Access Control
- المستخدم يبدأ من قائمة: User Warehouse Assignments
- المستخدم يبدأ من قائمة: Warehouse Access Matrix
- النموذج/الامتداد المعني: ResUsers: model _inherit
- النموذج/الامتداد المعني: StockScrap: model _inherit
- النموذج/الامتداد المعني: StockMove: model _inherit
- النموذج/الامتداد المعني: StockQuant: model _inherit
- النموذج/الامتداد المعني: StockLocation: model _inherit
- النموذج/الامتداد المعني: StockPickingType: model _inherit
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- النموذج/الامتداد المعني: StockPicking: model _inherit
- العملية البرمجية المتاحة: `test_11_no_warehouse_user_cannot_create_picking` في `tests/test_warehouse_access.py`
- العملية البرمجية المتاحة: `_compute_warehouse_count` في `models/res_users_extension.py`
- العملية البرمجية المتاحة: `action_view_warehouses` في `models/res_users_extension.py`
- العملية البرمجية المتاحة: `_compute_is_user_accessible` في `models/stock_scrap_extension.py`
- العملية البرمجية المتاحة: `_compute_warehouse_id` في `models/stock_scrap_extension.py`
- العملية البرمجية المتاحة: `create` في `models/stock_scrap_extension.py`
- العملية البرمجية المتاحة: `action_validate` في `models/stock_scrap_extension.py`
- العملية البرمجية المتاحة: `_compute_is_user_accessible` في `models/stock_move_extension.py`
- العملية البرمجية المتاحة: `create` في `models/stock_move_extension.py`
- العملية البرمجية المتاحة: `_compute_is_user_accessible` في `models/stock_quant_extension.py`
- العملية البرمجية المتاحة: `create` في `models/stock_quant_extension.py`
- العملية البرمجية المتاحة: `_get_quants_action` في `models/stock_quant_extension.py`
- العملية البرمجية المتاحة: `action_view_inventory` في `models/stock_quant_extension.py`
- العملية البرمجية المتاحة: `_compute_is_user_accessible` في `models/stock_location_extension.py`
- العملية البرمجية المتاحة: `_compute_warehouse_id` في `models/stock_location_extension.py`
- العملية البرمجية المتاحة: `_compute_is_user_accessible` في `models/stock_picking_type_extension.py`
- العملية البرمجية المتاحة: `create` في `models/stock_picking_type_extension.py`
- العملية البرمجية المتاحة: `create` في `models/sale_order_extension.py`
- العملية البرمجية المتاحة: `_compute_user_warehouse_count` في `models/stock_picking_extension.py`
- العملية البرمجية المتاحة: `_compute_is_user_accessible` في `models/stock_picking_extension.py`
- العملية البرمجية المتاحة: `create` في `models/stock_picking_extension.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
