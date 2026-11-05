# PDF Print Preview

- **المسار والإصدار:** `odoo19/el_pdf_print_preview` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Preview PDF reports in-browser before printing — no download needed

## الاختبارات المرفقة

- `tests/test_pdf_preview.py`
- `tests/__init__.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i el_pdf_print_preview --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
