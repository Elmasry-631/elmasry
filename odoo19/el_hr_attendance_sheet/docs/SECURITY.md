# HR Attendance Sheet And Policies

- **المسار والإصدار:** `odoo19/el_hr_attendance_sheet` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Calculate overtime, lateness, absence from attendance and feed payslip

## الصلاحيات والحماية المكتشفة

### ACL

- access_hr_attendance_public_holiday_user: model=model_hr_attendance_public_holiday, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_public_holiday_officer: model=model_hr_attendance_public_holiday, group=group_hr_attendance_sheet_officer, read/write/create/delete=1/1/1/0
- access_hr_attendance_public_holiday_manager: model=model_hr_attendance_public_holiday, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_public_holiday_line_user: model=model_hr_attendance_public_holiday_line, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_public_holiday_line_officer: model=model_hr_attendance_public_holiday_line, group=group_hr_attendance_sheet_officer, read/write/create/delete=1/1/1/0
- access_hr_attendance_public_holiday_line_manager: model=model_hr_attendance_public_holiday_line, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_rule_overtime_user: model=model_hr_attendance_rule_overtime, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_rule_overtime_manager: model=model_hr_attendance_rule_overtime, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_rule_lateness_user: model=model_hr_attendance_rule_lateness, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_rule_lateness_manager: model=model_hr_attendance_rule_lateness, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_rule_lateness_step_user: model=model_hr_attendance_rule_lateness_step, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_rule_lateness_step_manager: model=model_hr_attendance_rule_lateness_step, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_rule_lateness_tier_user: model=model_hr_attendance_rule_lateness_tier, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_rule_lateness_tier_manager: model=model_hr_attendance_rule_lateness_tier, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_rule_absence_user: model=model_hr_attendance_rule_absence, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_rule_absence_manager: model=model_hr_attendance_rule_absence, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_rule_absence_step_user: model=model_hr_attendance_rule_absence_step, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_rule_absence_step_manager: model=model_hr_attendance_rule_absence_step, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_rule_absence_tier_user: model=model_hr_attendance_rule_absence_tier, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_rule_absence_tier_manager: model=model_hr_attendance_rule_absence_tier, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_policy_user: model=model_hr_attendance_policy, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_policy_manager: model=model_hr_attendance_policy, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_sheet_user: model=model_hr_attendance_sheet, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_sheet_officer: model=model_hr_attendance_sheet, group=group_hr_attendance_sheet_officer, read/write/create/delete=1/1/1/0
- access_hr_attendance_sheet_manager: model=model_hr_attendance_sheet, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_sheet_line_user: model=model_hr_attendance_sheet_line, group=group_hr_attendance_sheet_user, read/write/create/delete=1/0/0/0
- access_hr_attendance_sheet_line_officer: model=model_hr_attendance_sheet_line, group=group_hr_attendance_sheet_officer, read/write/create/delete=1/1/1/0
- access_hr_attendance_sheet_line_manager: model=model_hr_attendance_sheet_line, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_sheet_batch_officer: model=model_hr_attendance_sheet_batch, group=group_hr_attendance_sheet_officer, read/write/create/delete=1/1/1/0
- access_hr_attendance_sheet_batch_manager: model=model_hr_attendance_sheet_batch, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_sheet_batch_line_officer: model=model_hr_attendance_sheet_batch_line, group=group_hr_attendance_sheet_officer, read/write/create/delete=1/1/1/0
- access_hr_attendance_sheet_batch_line_manager: model=model_hr_attendance_sheet_batch_line, group=group_hr_attendance_sheet_manager, read/write/create/delete=1/1/1/1
- access_hr_attendance_change_data_wizard: model=model_hr_attendance_change_data_wizard, group=group_hr_attendance_sheet_officer, read/write/create/delete=1/1/1/1
- access_hr_attendance_sheet_batch_wizard: model=model_hr_attendance_sheet_batch_wizard, group=group_hr_attendance_sheet_officer, read/write/create/delete=1/1/1/1
- access_hr_attendance_create_payslip_wizard: model=model_hr_attendance_create_payslip_wizard, group=group_hr_attendance_sheet_officer, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_hr_attendance_sheet_user`, `group_hr_attendance_sheet_officer`, `group_hr_attendance_sheet_manager`
- قواعد السجلات: `rule_hr_attendance_sheet_company`, `rule_hr_attendance_policy_company`, `rule_hr_attendance_public_holiday_company`, `rule_hr_attendance_sheet_batch_company`, `rule_hr_attendance_rule_overtime_company`, `rule_hr_attendance_sheet_personal`, `rule_hr_attendance_sheet_line_company`, `rule_hr_attendance_sheet_batch_line_company`, `rule_hr_attendance_sheet_line_personal`, `rule_hr_attendance_sheet_officer_all`, `rule_hr_attendance_sheet_line_officer_all`, `rule_hr_attendance_sheet_batch_line_officer_all`, `rule_hr_attendance_public_holiday_line_company`, `rule_hr_attendance_rule_lateness_company`, `rule_hr_attendance_rule_lateness_tier_company`, `rule_hr_attendance_rule_lateness_step_company`, `rule_hr_attendance_rule_absence_company`, `rule_hr_attendance_rule_absence_tier_company`, `rule_hr_attendance_rule_absence_step_company`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.