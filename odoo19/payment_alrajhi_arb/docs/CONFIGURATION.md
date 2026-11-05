# Al Rajhi Bank (ARB) Payment Gateway

- **المسار والإصدار:** `odoo19/payment_alrajhi_arb` — Odoo 19
- **إصدار الحزمة:** `19.0.1.4.12`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Official-style ARB integration: token API, encrypted trandata, bank-hosted redirect, KSA Card/Mada checkout (Odoo 19).

## الحقول ونقاط الإعداد الموجودة في المصدر

- `arb_resource_key (Char)`
- `arb_endpoint_url_test (Char)`
- `arb_endpoint_url_prod (Char)`
- `arb_return_token (Char)`

### إجراءات الإعداد

- `controllers/alrajhi_arb.py::_get_callback_params`
- `controllers/alrajhi_arb.py::_get_param`
- `controllers/alrajhi_arb.py::_get_any_param`
- `services/arb_client.py::create_payment_token`
- `models/payment_provider.py::action_test_alrajhi_connection`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
