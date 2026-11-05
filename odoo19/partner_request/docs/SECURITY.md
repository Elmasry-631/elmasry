# Partner Request

- **المسار والإصدار:** `odoo19/partner_request` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Approval workflow for creating new customers via sales requests.

## الصلاحيات والحماية المكتشفة

### ACL

- access_partner_request_manager: model=model_partner_request, group=partner_request.group_partner_request_manager, read/write/create/delete=1/1/1/1
- access_partner_request_user: model=model_partner_request, group=partner_request.group_partner_request_user, read/write/create/delete=1/1/1/0

### المجموعات وقواعد السجلات

- المجموعات: `group_partner_request_user`, `sales_team.group_sale_salesman`, `group_partner_request_manager`, `sales_team.group_sale_manager`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.