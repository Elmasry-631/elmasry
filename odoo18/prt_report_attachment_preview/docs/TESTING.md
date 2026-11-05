# Open PDF Reports and PDF Attachments in Browser

- **المسار والإصدار:** `odoo18/prt_report_attachment_preview` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Preview reports and pdf attachments in browser instead of downloading them.     Open Report or PDF Attachment in new tab instead of downloading.

## الاختبارات المرفقة

- `tests/test_cx_report_controller.py`
- `tests/__init__.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i prt_report_attachment_preview --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 18 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
