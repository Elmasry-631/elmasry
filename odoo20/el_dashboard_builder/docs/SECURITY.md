# Dashboard Builder

- **المسار والإصدار:** `odoo20/el_dashboard_builder` — Odoo 20
- **إصدار الحزمة:** `20.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Drag-and-drop dashboard builder with customizable widgets

## الصلاحيات والحماية المكتشفة

### ACL

- access_dashboard_builder_user: model=model_dashboard_builder, group=base.group_user, read/write/create/delete=1/1/1/1
- access_dashboard_builder_manager: model=model_dashboard_builder, group=dashboard_builder.group_dashboard_manager, read/write/create/delete=1/1/1/1
- access_dashboard_item_user: model=model_dashboard_builder_item, group=base.group_user, read/write/create/delete=1/1/1/1
- access_dashboard_item_manager: model=model_dashboard_builder_item, group=dashboard_builder.group_dashboard_manager, read/write/create/delete=1/1/1/1
- access_dashboard_widget_user: model=model_dashboard_builder_widget, group=base.group_user, read/write/create/delete=1/0/0/0
- access_dashboard_widget_manager: model=model_dashboard_builder_widget, group=dashboard_builder.group_dashboard_manager, read/write/create/delete=1/1/1/1
- access_dashboard_share_user: model=model_dashboard_builder_share, group=base.group_user, read/write/create/delete=1/1/1/1
- access_dashboard_share_manager: model=model_dashboard_builder_share, group=dashboard_builder.group_dashboard_manager, read/write/create/delete=1/1/1/1
- access_dashboard_tag_user: model=model_dashboard_builder_tag, group=base.group_user, read/write/create/delete=1/0/0/0
- access_dashboard_tag_manager: model=model_dashboard_builder_tag, group=dashboard_builder.group_dashboard_manager, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_dashboard_user`, `group_dashboard_manager`, `group_dashboard_admin`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- '/dashboard/builder/<int:dashboard_id>' (auth=user)
- '/dashboard/builder/<int:dashboard_id>/edit' (auth=user)
- '/dashboard/builder/shared/<string:token>' (auth=public)
- '/dashboard/builder/widget/test/<int:widget_id>' (auth=user)
- '/dashboard/builder/export/<int:dashboard_id>' (auth=user)
- '/dashboard/builder/export/pdf/<int:dashboard_id>' (auth=user)
- '/dashboard/builder/export/excel/<int:dashboard_id>' (auth=user)
- '/dashboard/builder/api/items/<int:item_id>/data' (auth=public)
- '/dashboard/builder/api/widgets/<int:widget_id>/data' (auth=user)
- '/dashboard/builder/api/items/<int:item_id>/configure' (auth=user)
- '/dashboard/builder/api/items/<int:item_id>/update' (auth=user)
- '/dashboard/builder/api/items/<int:item_id>/duplicate' (auth=user)
- '/dashboard/builder/api/items/<int:item_id>/delete' (auth=user)
- '/dashboard/builder/api/items/create' (auth=user)
- '/dashboard/builder/api/items/reorder' (auth=user)
- '/dashboard/builder/api/dashboard/<int:dashboard_id>/layout' (auth=user)
- '/dashboard/builder/api/dashboard/<int:dashboard_id>/duplicate' (auth=user)
- '/dashboard/builder/api/dashboard/<int:dashboard_id>/delete' (auth=user)

مواضع `sudo()` المرصودة:

- `controllers/controllers.py`
- `models/dashboard.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.