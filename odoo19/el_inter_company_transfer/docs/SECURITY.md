# Inter Company Transfer

- **المسار والإصدار:** `odoo19/el_inter_company_transfer` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automate inter-company stock, sale, purchase, and accounting documents

## الصلاحيات والحماية المكتشفة

### ACL

- access_stock_inter_company_transfer: model=model_stock_inter_company_transfer, group=all users, read/write/create/delete=1/1/1/1
- access_stock_inter_company_transfer_line: model=model_stock_inter_company_transfer_line, group=all users, read/write/create/delete=1/1/1/1
- access_return_inter_company_transfer: model=model_return_inter_company_transfer, group=all users, read/write/create/delete=1/1/1/1
- access_return_inter_company_transfer_line: model=model_return_inter_company_transfer_line, group=all users, read/write/create/delete=1/1/1/1
- access_inter_company_config: model=model_inter_company_config, group=all users, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_inter_company_transaction_manager`
- قواعد السجلات: `rule_stock_inter_company_transfer_multi_company`, `rule_stock_inter_company_transfer_line_multi_company`, `rule_return_inter_company_transfer_multi_company`, `rule_return_inter_company_transfer_line_multi_company`, `rule_inter_company_config_multi_company`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/purchase_order.py`
- `models/stock_inter_company_transfer.py`
- `models/sale_order.py`
- `models/return_inter_company_transfer.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.