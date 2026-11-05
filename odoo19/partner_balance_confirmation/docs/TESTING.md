# Balance Confirmation

- **المسار والإصدار:** `odoo19/partner_balance_confirmation` — Odoo 19
- **إصدار الحزمة:** `19.0.3.6.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Customer Balance Confirmation (Imdad / Namo templates)

## الاختبارات المرفقة

- لا يحتوي الموديول على مجلد `tests/`؛ لذلك لا توجد اختبارات Odoo مرفقة.

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i partner_balance_confirmation --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
