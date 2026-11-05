# Customer Classification & Credit Control

- **المسار والإصدار:** `odoo19/customer_classification` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Classify customers into tiers (A-E) with inherited price lists, credit limits, and payment terms.

## الحقول ونقاط الإعداد الموجودة في المصدر

- `override_credit_limit (Boolean)`
- `classification_credit_limit (Float)`
- `effective_credit_limit (Float)`
- `credit_limit (Float)`
- `company_id (Many2one)`
- `partner_effective_credit_limit (Float)`
- `partner_effective_credit_limit (Float)`

### إجراءات الإعداد

- لا توجد عناصر معلنة في ملفات الموديول.

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
