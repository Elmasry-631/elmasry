# EL Readonly User Access

- **المسار والإصدار:** `odoo18/el_readonly_user` — Odoo 18
- **إصدار الحزمة:** `18.0.1.2.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Grant controlled read-only access to users

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: IrHttp: model _inherit
- النموذج/الامتداد المعني: IrUiMenu: model _inherit
- النموذج/الامتداد المعني: IrModelAccess: model _inherit
- النموذج/الامتداد المعني: IrRule: model _inherit
- العملية البرمجية المتاحة: `_compute_domain` في `models/ir_rule.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
