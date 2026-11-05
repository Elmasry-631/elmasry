# Odoo Whatsapp Connector

- **المسار والإصدار:** `odoo19/whatsapp_mail_messaging` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Odoo18 Whatsapp, Whatsapp Odoo Integration, Odoo Whatsapp Connector,       Odoo Whatsapp, Whatsapp Connector, Whatsapp Integration, Odoo18, Whatsapp,      Odoo Apps

## الصلاحيات والحماية المكتشفة

### ACL

- access_whatsapp_send_message_user: model=model_whatsapp_send_message, group=base.group_user, read/write/create/delete=1/1/1/1
- access_selection_message_user: model=model_selection_message, group=base.group_user, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- '/whatsapp_message' (auth=public)
- '/mobile_number' (auth=public)

مواضع `sudo()` المرصودة:

- `controllers/whatsapp_mail_messaging.py`
- `model/account_move.py`
- `model/sale_order.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.