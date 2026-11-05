# Sale Contract Auto

- **المسار والإصدار:** `odoo18/sale_contract_auto` — Odoo 18
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automatically generate contracts from sale orders

## الاختبارات المرفقة

- لا يحتوي الموديول على مجلد `tests/`؛ لذلك لا توجد اختبارات Odoo مرفقة.

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i sale_contract_auto --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 18 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
