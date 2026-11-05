# Product Traceability Dashboard

- **المسار والإصدار:** `odoo18/el_product_traceability_dashboard` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Product traceability dashboard with returns, scrap and manufacturing genealogy

## الصلاحيات والحماية المكتشفة

### ACL

- access_product_traceability_report_user: model=model_el_product_traceability_report, group=el_product_traceability_dashboard.group_product_traceability_user, read/write/create/delete=1/0/0/0
- access_product_traceability_dashboard_user: model=model_el_product_traceability_dashboard, group=el_product_traceability_dashboard.group_product_traceability_user, read/write/create/delete=1/1/1/1
- access_product_traceability_manufacturing_user: model=model_el_product_traceability_manufacturing, group=el_product_traceability_dashboard.group_product_traceability_user, read/write/create/delete=1/0/0/0

### المجموعات وقواعد السجلات

- المجموعات: `group_product_traceability_user`, `group_product_traceability_manager`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.