# HR Attendance Sheet And Policies

- **المسار والإصدار:** `odoo19/el_hr_attendance_sheet` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Calculate overtime, lateness, absence from attendance and feed payslip

## الاختبارات المرفقة

- `tests/test_hr_attendance_sheet.py`
- `tests/__init__.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i el_hr_attendance_sheet --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
