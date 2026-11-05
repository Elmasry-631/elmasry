# POS Customer Payment Method

- **المسار والإصدار:** `odoo19/el_pos_customer_payment_method` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list.

## الاختبارات المرفقة

- `tests/__init__.py`
- `tests/test_payment_filter.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i el_pos_customer_payment_method --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
