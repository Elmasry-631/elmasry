# AI Finance V1

- **المسار والإصدار:** `odoo19/test_AI_finance` — Odoo 19
- **إصدار الحزمة:** `1.8`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Advanced AI Finance Module: Virtual CFO & OCR Engine

## الحقول ونقاط الإعداد الموجودة في المصدر

- `journal_has_invalid_statements (Boolean)`
- `api_key (Char)`
- `api_base_url (Char)`
- `match_key_column (Selection)`
- `company_id (Many2one)`
- `company_id (Many2one)`

### إجراءات الإعداد

- `models/ai_credential.py::action_test_connection`
- `models/ai_config.py::default_get`
- `models/ai_config.py::get_config`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
