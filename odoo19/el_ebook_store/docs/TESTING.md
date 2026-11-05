# E-Book Store

- **المسار والإصدار:** `odoo19/el_ebook_store` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Sell e-books with unique access codes — online reader + download

## الاختبارات المرفقة

- `tests/__init__.py`
- `tests/test_ebook_store.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i el_ebook_store --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
