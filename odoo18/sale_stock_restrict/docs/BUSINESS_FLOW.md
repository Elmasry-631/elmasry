# Sale Stock Restrict

- **المسار والإصدار:** `odoo18/sale_stock_restrict` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Module helps to restrict out of stock products

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: ResConfigSettings: model _inherit
- النموذج/الامتداد المعني: SaleOrderLine: model _inherit
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- العملية البرمجية المتاحة: `action_confirm` في `models/sale_order.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
