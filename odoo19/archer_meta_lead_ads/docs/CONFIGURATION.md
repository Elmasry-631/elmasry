# Meta Lead Ads

- **المسار والإصدار:** `odoo19/archer_meta_lead_ads` — Odoo 19
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Import Meta lead ads into CRM leads

## الحقول ونقاط الإعداد الموجودة في المصدر

- `company_id (Many2one)`
- `page_access_token (Text)`
- `company_id (Many2one)`
- `app_secret (Char)`
- `user_access_token (Text)`
- `token_expiry_date (Datetime)`
- `company_id (Many2one)`
- `company_id (Many2one)`
- `company_id (Many2one)`
- `meta_field_key (Char)`

### إجراءات الإعداد

- `models/meta_app_credential.py::action_generate_token`
- `models/meta_app_credential.py::action_test_connection`
- `models/meta_app_credential.py::_cron_check_token_expiry`
- `models/res_config_settings.py::action_open_meta_lead_ads`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
