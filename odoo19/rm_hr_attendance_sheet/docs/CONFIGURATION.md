# HR Attendance Sheet and Policies

- **المسار والإصدار:** `odoo19/rm_hr_attendance_sheet` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Attendance sheets, policies, overtime, lateness, absence, and payroll links

## الحقول ونقاط الإعداد الموجودة في المصدر

- `company_id (Many2one)`
- `company_id (Many2one)`
- `company_id (Many2one)`
- `company_id (Many2one)`
- `company_id (Many2one)`

### إجراءات الإعداد

- `models/hr_salary_rule.py::_rm_configure_attendance_basic_rule`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
