# Customer Classification & Credit Control

- **المسار والإصدار:** `odoo19/customer_classification` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Classify customers into tiers (A-E) with inherited price lists, credit limits, and payment terms.

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Customer Classification
- المستخدم يبدأ من قائمة: Classifications
- النموذج/الامتداد المعني: ResPartner: model _inherit
- النموذج/الامتداد المعني: CustomerClassification: model _name
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: ClassificationCriteria: model _name
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- العملية البرمجية المتاحة: `_compute_product_pricelist` في `models/res_partner.py`
- العملية البرمجية المتاحة: `_compute_effective_credit_limit` في `models/res_partner.py`
- العملية البرمجية المتاحة: `_compute_effective_payment_term_id` في `models/res_partner.py`
- العملية البرمجية المتاحة: `_compute_display_name` في `models/customer_classification.py`
- العملية البرمجية المتاحة: `_compute_partner_count` في `models/customer_classification.py`
- العملية البرمجية المتاحة: `_compute_has_active_criteria` في `models/customer_classification.py`
- العملية البرمجية المتاحة: `action_apply_pricelist` في `models/customer_classification.py`
- العملية البرمجية المتاحة: `action_post` في `models/account_move.py`
- العملية البرمجية المتاحة: `_compute_display_name` في `models/classification_criteria.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/sale_order.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
