# Account Fixed Discount

- **المسار والإصدار:** `odoo19/account_invoice_fixed_discount` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Allows to apply fixed amount discounts in invoices.

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: AccountMoveLine: model _inherit
- النموذج/الامتداد المعني: AccountTax: model _inherit
- العملية البرمجية المتاحة: `_create_invoice` في `tests/test_account_fixed_discount.py`
- العملية البرمجية المتاحة: `_compute_totals` في `models/account_move_line.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
