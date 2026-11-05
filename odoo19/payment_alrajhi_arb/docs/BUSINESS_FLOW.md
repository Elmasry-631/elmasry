# Al Rajhi Bank (ARB) Payment Gateway

- **المسار والإصدار:** `odoo19/payment_alrajhi_arb` — Odoo 19
- **إصدار الحزمة:** `19.0.1.4.12`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Official-style ARB integration: token API, encrypted trandata, bank-hosted redirect, KSA Card/Mada checkout (Odoo 19).

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: PaymentProvider: model _inherit
- النموذج/الامتداد المعني: PaymentTransaction: model _inherit
- العملية البرمجية المتاحة: `_find_transaction` في `controllers/alrajhi_arb.py`
- العملية البرمجية المتاحة: `_get_processing_status_route` في `controllers/alrajhi_arb.py`
- العملية البرمجية المتاحة: `_render_processing_page` في `controllers/alrajhi_arb.py`
- العملية البرمجية المتاحة: `_process_final_or_wait` في `controllers/alrajhi_arb.py`
- العملية البرمجية المتاحة: `create_payment_token` في `services/arb_client.py`
- العملية البرمجية المتاحة: `inquire_transaction` في `services/arb_client.py`
- العملية البرمجية المتاحة: `action_test_alrajhi_connection` في `models/payment_provider.py`
- العملية البرمجية المتاحة: `_get_specific_processing_values` في `models/payment_transaction.py`
- العملية البرمجية المتاحة: `_get_specific_rendering_values` في `models/payment_transaction.py`
- العملية البرمجية المتاحة: `_search_by_reference` في `models/payment_transaction.py`
- العملية البرمجية المتاحة: `_extract_amount_data` في `models/payment_transaction.py`
- العملية البرمجية المتاحة: `_apply_updates` في `models/payment_transaction.py`
- العملية البرمجية المتاحة: `_get_base_url` في `models/payment_transaction.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
