# Purchase Actual Quantity

- **المسار والإصدار:** `odoo18/el_purchase_actual_qty` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Actual purchase quantity with preserved value, dashboard and reporting

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Actual Quantity Dashboard
- المستخدم يبدأ من قائمة: Actual Quantity Analysis
- النموذج/الامتداد المعني: ResConfigSettings: model _inherit
- النموذج/الامتداد المعني: PurchaseActualReport: model _name
- النموذج/الامتداد المعني: PurchaseOrderLine: model _inherit
- العملية البرمجية المتاحة: `export_csv` في `controllers/purchase_actual_export.py`
- العملية البرمجية المتاحة: `_compute_effective_price_unit` في `models/purchase_order_line.py`
- العملية البرمجية المتاحة: `_compute_variance` في `models/purchase_order_line.py`
- العملية البرمجية المتاحة: `create` في `models/purchase_order_line.py`
- العملية البرمجية المتاحة: `_compute_qty_invoiced` في `models/purchase_order_line.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
