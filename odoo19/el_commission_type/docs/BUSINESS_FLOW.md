# Commission Types

- **المسار والإصدار:** `odoo19/el_commission_type` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Manage sales commission types by team member role

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Commissions
- المستخدم يبدأ من قائمة: Commissions
- المستخدم يبدأ من قائمة: Commission Types
- النموذج/الامتداد المعني: ResPartner: model _inherit
- النموذج/الامتداد المعني: SalesCommission: model _name
- النموذج/الامتداد المعني: SalesCommissionType: model _name
- العملية البرمجية المتاحة: `_compute_name` في `models/sales_commission.py`
- العملية البرمجية المتاحة: `_compute_name` في `models/commission_type.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
