# Direct Print Auto

- **المسار والإصدار:** `odoo19/direct_print_auto` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Auto-print invoices, SOs, delivery slips and POs to the browser's print dialog when confirmed, plus a manual Direct Print button on each form.

## الصلاحيات والحماية المكتشفة

### ACL

- access_direct_print_user_settings: model=model_res_config_settings, group=group_direct_print_manager, read/write/create/delete=1/1/1/0

### المجموعات وقواعد السجلات

- المجموعات: `group_direct_print_user`, `group_direct_print_manager`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `tests/test_auto_print_flow.py`
- `tests/test_direct_print_mixin.py`
- `models/purchase_order.py`
- `models/account_move.py`
- `models/stock_picking.py`
- `models/sale_order.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.