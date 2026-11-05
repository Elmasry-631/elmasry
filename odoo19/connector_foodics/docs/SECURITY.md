# Foodics Connector

- **المسار والإصدار:** `odoo19/connector_foodics` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Bidirectional synchronization bridge between Odoo and Foodics POS

## الصلاحيات والحماية المكتشفة

### ACL

- access_foodics_connection_admin: model=model_foodics_connection, group=connector_foodics.group_foodics_admin, read/write/create/delete=1/1/1/1
- access_foodics_connection_operator: model=model_foodics_connection, group=connector_foodics.group_foodics_operator, read/write/create/delete=1/0/0/0
- access_foodics_mapping_admin: model=model_foodics_mapping, group=connector_foodics.group_foodics_admin, read/write/create/delete=1/1/1/1
- access_foodics_mapping_operator: model=model_foodics_mapping, group=connector_foodics.group_foodics_operator, read/write/create/delete=1/0/0/0
- access_foodics_branch_mapping_admin: model=model_foodics_branch_mapping, group=connector_foodics.group_foodics_admin, read/write/create/delete=1/1/1/1
- access_foodics_branch_mapping_operator: model=model_foodics_branch_mapping, group=connector_foodics.group_foodics_operator, read/write/create/delete=1/0/0/0
- access_foodics_sync_log_admin: model=model_foodics_sync_log, group=connector_foodics.group_foodics_admin, read/write/create/delete=1/1/1/1
- access_foodics_sync_log_operator: model=model_foodics_sync_log, group=connector_foodics.group_foodics_operator, read/write/create/delete=1/1/0/0
- access_foodics_webhook_event_admin: model=model_foodics_webhook_event, group=connector_foodics.group_foodics_admin, read/write/create/delete=1/1/1/1
- access_foodics_webhook_event_operator: model=model_foodics_webhook_event, group=connector_foodics.group_foodics_operator, read/write/create/delete=1/0/0/0
- access_foodics_webhook_log_admin: model=model_foodics_webhook_log, group=connector_foodics.group_foodics_admin, read/write/create/delete=1/1/1/1
- access_foodics_webhook_log_operator: model=model_foodics_webhook_log, group=connector_foodics.group_foodics_operator, read/write/create/delete=1/1/0/0
- access_foodics_test_connection_wizard: model=model_foodics_test_connection_wizard, group=connector_foodics.group_foodics_admin, read/write/create/delete=1/1/1/1
- access_foodics_resync_wizard: model=model_foodics_resync_wizard, group=connector_foodics.group_foodics_admin, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_foodics_operator`, `group_foodics_admin`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- '/foodics/webhook/<string:secret>' (auth=public, csrf=False)
- '/foodics/webhook/<string:secret>' (auth=public, csrf=False)

مواضع `sudo()` المرصودة:

- `controllers/webhook_controller.py`
- `models/foodics_connection.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.