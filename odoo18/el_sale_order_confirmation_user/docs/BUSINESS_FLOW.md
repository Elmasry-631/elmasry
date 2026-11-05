# Sale Order Confirmation User

- **المسار والإصدار:** `odoo18/el_sale_order_confirmation_user` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track which user actually confirmed each sales order

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: SaleOrder: model _inherit
- العملية البرمجية المتاحة: `setUpClass` في `tests/test_sale_order_confirmation_user.py`
- العملية البرمجية المتاحة: `_create_order` في `tests/test_sale_order_confirmation_user.py`
- العملية البرمجية المتاحة: `test_01_confirmed_by_set_to_confirming_user` في `tests/test_sale_order_confirmation_user.py`
- العملية البرمجية المتاحة: `test_02_group_by_and_filter_confirmed_by` في `tests/test_sale_order_confirmation_user.py`
- العملية البرمجية المتاحة: `test_03_confirmed_by_readonly_via_write` في `tests/test_sale_order_confirmation_user.py`
- العملية البرمجية المتاحة: `test_04_confirmed_by_not_copied` في `tests/test_sale_order_confirmation_user.py`
- العملية البرمجية المتاحة: `test_05_batch_confirmation` في `tests/test_sale_order_confirmation_user.py`
- العملية البرمجية المتاحة: `test_06_programmatic_confirmation` في `tests/test_sale_order_confirmation_user.py`
- العملية البرمجية المتاحة: `test_07_reconfirmation_after_cancel` في `tests/test_sale_order_confirmation_user.py`
- العملية البرمجية المتاحة: `test_08_idempotent_confirm_does_not_overwrite` في `tests/test_sale_order_confirmation_user.py`
- العملية البرمجية المتاحة: `test_09_pre_existing_order_not_backfilled` في `tests/test_sale_order_confirmation_user.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/sale_order.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
