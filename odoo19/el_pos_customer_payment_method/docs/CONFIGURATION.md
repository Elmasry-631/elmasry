# POS Customer Payment Method

- **المسار والإصدار:** `odoo19/el_pos_customer_payment_method` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list.

## الحقول ونقاط الإعداد الموجودة في المصدر

- لا توجد عناصر معلنة في ملفات الموديول.

### إجراءات الإعداد

- `tests/test_payment_filter.py::test_05_pos_config_defaults_field_loaded`
- `tests/test_payment_filter.py::test_06_settings_related_field_roundtrip`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
