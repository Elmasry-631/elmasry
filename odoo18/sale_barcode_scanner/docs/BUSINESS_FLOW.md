# Sale Order Barcode Scanner

- **المسار والإصدار:** `odoo18/sale_barcode_scanner` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Scan products by Barcode/QRCode in sales orders using mobile camera or webcam

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: SaleOrder: model _inherit
- العملية البرمجية المتاحة: `action_open_barcode_scanner` في `models/sale_order.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
