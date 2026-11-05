# Button Access Control

- **المسار والإصدار:** `odoo19/el_button_access_control` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Control button visibility per user group — show/hide buttons in any view without editing XML

## الاختبارات المرفقة

- `tests/__init__.py`
- `tests/test_button_access.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i el_button_access_control --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
