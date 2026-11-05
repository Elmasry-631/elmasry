# Hospital Management System

- **المسار والإصدار:** `odoo19/el_hospital` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Complete hospital management: patients, appointments, EMR, wards, lab, pharmacy, billing

## الاختبارات المرفقة

- `tests/test_hospital_admission.py`
- `tests/__init__.py`
- `tests/test_hospital_patient.py`
- `tests/test_hospital_billing.py`
- `tests/test_hospital_appointment.py`
- `tests/test_hospital_lab.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i el_hospital --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
