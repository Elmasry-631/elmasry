# Payroll WPS Export

- **المسار والإصدار:** `odoo19/el_payroll_wps` — Odoo 19
- **إصدار الحزمة:** `19.0.1.2.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Adds an 'Others' field to payslips and the bank salary file export (WPS)

## الصلاحيات والحماية المكتشفة

### ACL

- access_wps_export_wizard_user: model=model_wps_export_wizard, group=hr_payroll.group_hr_payroll_user, read/write/create/delete=1/1/1/1
- access_wps_export_wizard_admin: model=model_wps_export_wizard, group=base.group_system, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `tests/test_wps_export.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.