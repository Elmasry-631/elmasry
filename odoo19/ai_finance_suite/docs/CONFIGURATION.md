# AI Finance

- **المسار والإصدار:** `odoo19/ai_finance_suite` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** AI-Powered Finance Suite: Virtual CFO, OCR Engine & Smart Reconciliation for Odoo 19

## الحقول ونقاط الإعداد الموجودة في المصدر

- `journal_has_invalid_statements (Boolean)`
- `api_key (Char)`
- `api_base_url (Char)`
- `match_key_column (Selection)`
- `company_id (Many2one)`

### إجراءات الإعداد

- `models/ai_credential.py::action_test_connection`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
