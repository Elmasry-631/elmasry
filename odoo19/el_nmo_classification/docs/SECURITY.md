# El-Nmo - Customer Classification

- **المسار والإصدار:** `odoo19/el_nmo_classification` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Customer classification tiers (A-E) with auto-classification criteria.

## الصلاحيات والحماية المكتشفة

### ACL

- access_customer_classification_manager: model=model_customer_classification, group=sales_team.group_sale_manager, read/write/create/delete=1/1/1/1
- access_customer_classification_user: model=model_customer_classification, group=sales_team.group_sale_salesman, read/write/create/delete=1/0/0/0
- access_classification_criteria_manager: model=model_classification_criteria, group=sales_team.group_sale_manager, read/write/create/delete=1/1/1/1
- access_classification_criteria_user: model=model_classification_criteria, group=sales_team.group_sale_salesman, read/write/create/delete=1/0/0/0

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/account_move.py`
- `models/sale_order.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.