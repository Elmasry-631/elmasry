# EL Readonly User Access

- **المسار والإصدار:** `odoo18/el_readonly_user` — Odoo 18
- **إصدار الحزمة:** `18.0.1.2.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Grant controlled read-only access to users

## الاختبارات المرفقة

- لا يحتوي الموديول على مجلد `tests/`؛ لذلك لا توجد اختبارات Odoo مرفقة.

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i el_readonly_user --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 18 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
