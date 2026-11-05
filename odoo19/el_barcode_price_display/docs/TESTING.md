# Barcode Price Display

- **المسار والإصدار:** `odoo19/el_barcode_price_display` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Standalone barcode scanner price display page — no login needed

## الاختبارات المرفقة

- `tests/test_price_display.py`
- `tests/__init__.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i el_barcode_price_display --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
