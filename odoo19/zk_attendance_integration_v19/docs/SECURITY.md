# TechScope | ZK Attendance Integration

- **المسار والإصدار:** `odoo19/zk_attendance_integration_v19` — Odoo 19
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `غير محدد في manifest`
- **الملخص المعلن:** Integration with ZK Attendance Machines

## الصلاحيات والحماية المكتشفة

### ACL

- access_hr_attendance_zk_temp: model=model_hr_attendance_zk_temp, group=all users, read/write/create/delete=1/1/1/1
- access_hr_attendance_zk_machine: model=model_hr_attendance_zk_machine, group=all users, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/zk_attendance.py`
- `models/models.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.