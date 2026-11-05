# HR Attendance Sheet and Policies

- **المسار والإصدار:** `odoo19/rm_hr_attendance_sheet` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Attendance sheets, policies, overtime, lateness, absence, and payroll links

## الصلاحيات والحماية المكتشفة

### ACL

- access_rm_overtime_rule_user: model=model_rm_overtime_rule, group=group_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_rm_overtime_rule_manager: model=model_rm_overtime_rule, group=group_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_rm_lateness_rule_user: model=model_rm_lateness_rule, group=group_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_rm_lateness_rule_manager: model=model_rm_lateness_rule, group=group_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_rm_lateness_step_user: model=model_rm_lateness_step, group=group_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_rm_lateness_step_manager: model=model_rm_lateness_step, group=group_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_rm_absence_rule_user: model=model_rm_absence_rule, group=group_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_rm_absence_rule_manager: model=model_rm_absence_rule, group=group_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_rm_absence_step_user: model=model_rm_absence_step, group=group_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_rm_absence_step_manager: model=model_rm_absence_step, group=group_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_rm_attendance_policy_user: model=model_rm_attendance_policy, group=group_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_rm_attendance_policy_manager: model=model_rm_attendance_policy, group=group_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_rm_attendance_sheet_user: model=model_rm_attendance_sheet, group=group_attendance_sheet_user, read/write/create/delete=1/1/1/0
- access_rm_attendance_sheet_manager: model=model_rm_attendance_sheet, group=group_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_rm_attendance_sheet_line_user: model=model_rm_attendance_sheet_line, group=group_attendance_sheet_user, read/write/create/delete=1/1/1/0
- access_rm_attendance_sheet_line_manager: model=model_rm_attendance_sheet_line, group=group_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_rm_attendance_sheet_change_wizard: model=model_rm_attendance_sheet_change_wizard, group=group_attendance_sheet_user, read/write/create/delete=1/1/1/1
- access_rm_attendance_sheet_batch_wizard: model=model_rm_attendance_sheet_batch_wizard, group=group_attendance_sheet_user, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_attendance_sheet_user`, `group_attendance_sheet_manager`
- قواعد السجلات: `rule_attendance_sheet_company`, `rule_attendance_sheet_line_company`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.