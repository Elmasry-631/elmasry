# Prevent Negative Stock

- **المسار والإصدار:** `odoo19/el_prevent_negative_stock` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Prevent negative stock — block stock moves AND sales orders when stock is insufficient

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Negative Stock Alerts
- المستخدم يبدأ من قائمة: All Alerts
- النموذج/الامتداد المعني: ElStockAlert: model _name
- النموذج/الامتداد المعني: StockMove: model _inherit
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- العملية البرمجية المتاحة: `_create_picking` في `tests/test_negative_stock.py`
- العملية البرمجية المتاحة: `_create_sale_order` في `tests/test_negative_stock.py`
- العملية البرمجية المتاحة: `create` في `models/el_stock_alert.py`
- العملية البرمجية المتاحة: `_action_assign` في `models/stock_move.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/sale_order.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
