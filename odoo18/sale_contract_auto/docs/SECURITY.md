# Sale Contract Auto

- **المسار والإصدار:** `odoo18/sale_contract_auto` — Odoo 18
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automatically generate contracts from sale orders

## الصلاحيات والحماية المكتشفة

### ACL

- access_sale_contract_user: model=model_sale_contract, group=base.group_user, read/write/create/delete=1/0/0/0
- access_sale_contract_manager: model=model_sale_contract, group=sales_team.group_sale_manager, read/write/create/delete=1/1/1/1
- access_sale_contract_account_manager: model=model_sale_contract, group=account.group_account_manager, read/write/create/delete=1/1/1/1
- access_sale_contract_portal: model=model_sale_contract, group=base.group_portal, read/write/create/delete=1/1/0/0
- access_sale_contract_line_user: model=model_sale_contract_line, group=base.group_user, read/write/create/delete=1/0/0/0
- access_sale_contract_line_manager: model=model_sale_contract_line, group=sales_team.group_sale_manager, read/write/create/delete=1/1/1/1
- access_sale_contract_line_account_manager: model=model_sale_contract_line, group=account.group_account_manager, read/write/create/delete=1/1/1/1
- access_contract_template_user: model=model_contract_template, group=base.group_user, read/write/create/delete=1/0/0/0
- access_contract_template_manager: model=model_contract_template, group=sales_team.group_sale_manager, read/write/create/delete=1/1/1/1
- access_sale_contract_title: model=model_sale_contract_title, group=all users, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- ['/my/contracts/<int:contract_id>'] (auth=user)
- ['/my/contracts/<int:contract_id>/sign'] (auth=user)

مواضع `sudo()` المرصودة:

- `controllers/controllers.py`
- `models/sale_contract.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.