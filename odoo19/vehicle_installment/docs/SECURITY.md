# Vehicle Installment Management

- **المسار والإصدار:** `odoo19/vehicle_installment` — Odoo 19
- **إصدار الحزمة:** `19.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Manage vehicle installments with automatic calculation

## الصلاحيات والحماية المكتشفة

### ACL

- access_vehicle_installment_user: model=model_vehicle_installment, group=vehicle_installment.group_vehicle_installment_user, read/write/create/delete=1/0/0/0
- access_vehicle_installment_line_user: model=model_vehicle_installment_line, group=vehicle_installment.group_vehicle_installment_user, read/write/create/delete=1/0/0/0
- access_vehicle_installment_manager: model=model_vehicle_installment, group=vehicle_installment.group_vehicle_installment_manager, read/write/create/delete=1/1/1/1
- access_vehicle_installment_line_manager: model=model_vehicle_installment_line, group=vehicle_installment.group_vehicle_installment_manager, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_vehicle_installment_user`, `group_vehicle_installment_manager`
- قواعد السجلات: `vehicle_installment_rule`, `vehicle_installment_see_own_company`, `vehicle_installment_line_see_own_company`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.