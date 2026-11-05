# IE Print Document Linked Order

- **المسار والإصدار:** `odoo17/ie_print_document_linked_order` — Odoo 17
- **إصدار الحزمة:** `0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Show all product attachments directly from Quotation.

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: SaleOrder: model _inherit
- النموذج/الامتداد المعني: IrAttachment: model _inherit
- العملية البرمجية المتاحة: `action_view_product_attachments` في `models/sale_order.py`
- العملية البرمجية المتاحة: `action_print_selected` في `models/sale_order.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
