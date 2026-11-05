# ie_costem_lead_form

- **المسار والإصدار:** `odoo17/ie_costem_lead_form` — Odoo 17
- **إصدار الحزمة:** `0.1`
- **الترخيص المعلن:** `غير محدد في manifest`
- **الملخص المعلن:** Short (1 phrase/line) summary of the module's purpose

## الصلاحيات والحماية المكتشفة

### ACL

- access_crm_lead_specification_line_user: model=model_crm_lead_specification_line, group=base.group_user, read/write/create/delete=1/1/1/1
- access_crm_lead_specification_line_manager: model=model_crm_lead_specification_line, group=base.group_system, read/write/create/delete=1/1/1/1
- access_res_users_sales: model=base.model_res_users, group=sales_team.group_sale_salesman, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.