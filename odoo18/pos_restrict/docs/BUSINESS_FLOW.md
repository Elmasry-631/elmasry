# POS User Restrict

- **المسار والإصدار:** `odoo18/pos_restrict` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Restricts User access to pos and orders.

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: PosConfig: model _inherit
- النموذج/الامتداد المعني: ResUsers: model _inherit
- العملية البرمجية المتاحة: `_compute_users_allowed` في `models/pos_config.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
