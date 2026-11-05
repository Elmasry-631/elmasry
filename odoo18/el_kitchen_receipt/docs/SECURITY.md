# Kitchen Receipt from Quotation

- **المسار والإصدار:** `odoo18/el_kitchen_receipt` — Odoo 18
- **إصدار الحزمة:** `18.0.4.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Print kitchen receipt from sales quotation with customer delivery info auto-fill + pilot name sync with delivery

## الصلاحيات والحماية المكتشفة

### ACL

- access_x_pilot_user: model=model_x_pilot, group=sales_team.group_sale_salesman, read/write/create/delete=1/1/1/0
- access_x_pilot_manager: model=model_x_pilot, group=sales_team.group_sale_manager, read/write/create/delete=1/1/1/1
- access_pilot_report_wizard_user: model=model_pilot_report_wizard, group=sales_team.group_sale_salesman, read/write/create/delete=1/0/1/0
- access_pilot_report_wizard_manager: model=model_pilot_report_wizard, group=sales_team.group_sale_manager, read/write/create/delete=1/0/1/0

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/account_move.py`
- `models/stock_picking.py`
- `models/sale_order.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.