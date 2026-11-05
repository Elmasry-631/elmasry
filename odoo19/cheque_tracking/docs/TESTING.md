# Cheque Tracking

- **المسار والإصدار:** `odoo19/cheque_tracking` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track received and issued cheques with accounting lifecycle entries

## الاختبارات المرفقة

- لا يحتوي الموديول على مجلد `tests/`؛ لذلك لا توجد اختبارات Odoo مرفقة.

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i cheque_tracking --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
