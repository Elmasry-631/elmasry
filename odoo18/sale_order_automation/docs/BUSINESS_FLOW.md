# Sale Order Automation

- **المسار والإصدار:** `odoo18/sale_order_automation` — Odoo 18
- **إصدار الحزمة:** `1.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Enable auto sale workflow with sale order confirmation. Include operations like Auto Create Invoice, Auto Validate Invoice and Auto Transfer Delivery Order.

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: StockWarehouse: model _inherit
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- العملية البرمجية المتاحة: `action_confirm` في `models/sale_order.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
