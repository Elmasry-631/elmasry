# Restrict Journal for Users (Whitelist)

- **المسار والإصدار:** `odoo18/el_restrict_journal` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Per-user journal whitelist — only allowed journals are visible

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: AccountJournal: model _inherit
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: ResUsers: model _inherit
- النموذج/الامتداد المعني: AccountPayment: model _inherit
- العملية البرمجية المتاحة: `test_02_move_create_blocked` في `tests/test_restrict_journal.py`
- العملية البرمجية المتاحة: `test_04_payment_create_blocked` في `tests/test_restrict_journal.py`
- العملية البرمجية المتاحة: `test_07_move_create_allowed` في `tests/test_restrict_journal.py`
- العملية البرمجية المتاحة: `test_08_payment_create_allowed` في `tests/test_restrict_journal.py`
- العملية البرمجية المتاحة: `_compute_allowed_user_count` في `models/account_journal.py`
- العملية البرمجية المتاحة: `create` في `models/account_move.py`
- العملية البرمجية المتاحة: `create` في `models/account_payment.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
