# POS Customer Payment Method

- **المسار والإصدار:** `odoo18/el_pos_customer_payment_method` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list.

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: ResPartner: model _inherit
- النموذج/الامتداد المعني: ResConfigSettings: model _inherit
- النموذج/الامتداد المعني: PosConfig: model _inherit

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
