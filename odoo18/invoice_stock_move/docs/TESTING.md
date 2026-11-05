# Stock Picking From Invoice

- **المسار والإصدار:** `odoo18/invoice_stock_move` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Stock Picking From Customer/Supplier Invoice

## الاختبارات المرفقة

- لا يحتوي الموديول على مجلد `tests/`؛ لذلك لا توجد اختبارات Odoo مرفقة.

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i invoice_stock_move --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 18 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
