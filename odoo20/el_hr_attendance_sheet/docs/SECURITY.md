# HR Attendance Sheet And Policies

- **المسار والإصدار:** `odoo20/el_hr_attendance_sheet` — Odoo 20
- **إصدار الحزمة:** `20.0.1.0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Calculate overtime, lateness, absence from attendance and feed payslip

## الصلاحيات والحماية المكتشفة

### ACL

- لا توجد عناصر معلنة في ملفات الموديول.

### المجموعات وقواعد السجلات

- المجموعات: `group_hr_attendance_sheet_user`, `group_hr_attendance_sheet_officer`, `group_hr_attendance_sheet_manager`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.