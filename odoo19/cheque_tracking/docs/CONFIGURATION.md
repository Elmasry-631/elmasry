# Cheque Tracking

- **المسار والإصدار:** `odoo19/cheque_tracking` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track received and issued cheques with accounting lifecycle entries

## الحقول ونقاط الإعداد الموجودة في المصدر

- `bank_journal_id (Many2one)`
- `journal_entry_id (Many2one)`
- `company_id (Many2one)`
- `company_id (Many2one)`
- `company_id (Many2one)`
- `company_currency_id (Many2one)`
- `amount_company_currency (Monetary)`
- `journal_entry_id (Many2one)`
- `company_id (Many2one)`
- `bank_journal_id (Many2one)`

### إجراءات الإعداد

- لا توجد عناصر معلنة في ملفات الموديول.

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
