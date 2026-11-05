# Foodics Connector

- **المسار والإصدار:** `odoo19/connector_foodics` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Bidirectional synchronization bridge between Odoo and Foodics POS

## الاختبارات المرفقة

- `tests/__init__.py`
- `tests/test_foodics_models.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i connector_foodics --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
