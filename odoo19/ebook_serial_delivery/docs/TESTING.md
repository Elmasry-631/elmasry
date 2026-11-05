# eBook Serial Delivery

- **المسار والإصدار:** `odoo19/ebook_serial_delivery` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Deliver eBook licenses using standard Inventory Serial Numbers (stock.lot) — no custom "activation code" model.

## الاختبارات المرفقة

- `tests/__init__.py`
- `tests/test_serial_mail_template.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i ebook_serial_delivery --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
