# Restrict Journal for Users (Whitelist)

- **المسار والإصدار:** `odoo18/el_restrict_journal` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Per-user journal whitelist — only allowed journals are visible

## الاختبارات المرفقة

- `tests/__init__.py`
- `tests/test_restrict_journal.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i el_restrict_journal --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 18 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
