# Construction Management

- **المسار والإصدار:** `odoo19/el_construction_management` — Odoo 19
- **إصدار الحزمة:** `19.0.1.24.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Construction Management \| Job Costing \| BOQ \| Work Orders \| RA Billing \| Material Requisition \| Subcontracting \| Budget

## الاختبارات المرفقة

- `tests/test_mreq.py`
- `tests/test_billing.py`
- `tests/test_task.py`
- `tests/test_budget_methods.py`
- `tests/__init__.py`
- `tests/test_quality_check.py`
- `tests/test_budget_costing.py`
- `tests/test_hardening.py`
- `tests/test_round2_hardening.py`
- `tests/test_workflow.py`

## تشغيل اختبارات Odoo

`./odoo-bin -d <test_database> -i el_construction_management --test-enable --stop-after-init`

## فحوص المصدر

- تحقق من أن ملفات Python قابلة للتحليل وأن XML صالح.
- اختبر التثبيت على Odoo 19 مع dependencies والطبعة نفسها.
- لا تعتبر وجود ملفات tests دليلًا على نجاح تشغيلها؛ سجل النتيجة والبيئة عند التنفيذ.
