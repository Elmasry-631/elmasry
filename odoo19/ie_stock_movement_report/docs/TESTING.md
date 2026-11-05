# Stock Movement Report

- **المسار والإصدار:** `odoo19/ie_stock_movement_report` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** PDF report of inventory movements with opening/closing balance and running value.

## الاختبارات المرفقة

- `tests/test_stock_movement_report.py`
- `tests/test_permissions.py`
- `tests/__init__.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i ie_stock_movement_report --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
