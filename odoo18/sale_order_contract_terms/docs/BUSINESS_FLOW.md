# Sales Order Contract Terms (AR/EN) - 4 Pages

- **المسار والإصدار:** `odoo18/sale_order_contract_terms` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Separate Sales Order report with bilingual contract terms (4 pages, AR/EN).

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: ResPartner: model _inherit
- النموذج/الامتداد المعني: ResCompany: model _inherit
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- النموذج/الامتداد المعني: SaleOrderContractTerms: model _inherit
- النموذج/الامتداد المعني: ProductTemplate: model _inherit
- العملية البرمجية المتاحة: `_compute_technical_specification_id` في `models/sale_order.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
