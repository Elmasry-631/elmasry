# Dashboard Builder

- **المسار والإصدار:** `odoo20/el_dashboard_builder` — Odoo 20
- **إصدار الحزمة:** `20.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Drag-and-drop dashboard builder with customizable widgets

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Drag-and-drop dashboard builder with customizable widgets
- نموذج Odoo: DashboardBuilderReport: model _name
- نموذج Odoo: DashboardExportWizard: model _name
- نموذج Odoo: Dashboard: model _name
- نموذج Odoo: DashboardTag: model _name
- نموذج Odoo: DashboardWidget: model _name
- نموذج Odoo: DashboardItem: model _name
- نموذج Odoo: DashboardShare: model _name
- نموذج Odoo: DashboardItemConfigWizard: model _name
- قائمة واجهة: Dashboard Builder
- قائمة واجهة: My Dashboards
- قائمة واجهة: New Dashboard
- قائمة واجهة: Favorites
- قائمة واجهة: All Dashboards
- قائمة واجهة: Widget Library
- قائمة واجهة: Shared Dashboards
- قائمة واجهة: Configuration
- قائمة واجهة: Tags
- نقطة HTTP: '/dashboard/builder/<int:dashboard_id>' (auth=user)
- نقطة HTTP: '/dashboard/builder/<int:dashboard_id>/edit' (auth=user)
- نقطة HTTP: '/dashboard/builder/shared/<string:token>' (auth=public)
- نقطة HTTP: '/dashboard/builder/widget/test/<int:widget_id>' (auth=user)
- نقطة HTTP: '/dashboard/builder/export/<int:dashboard_id>' (auth=user)
- نقطة HTTP: '/dashboard/builder/export/pdf/<int:dashboard_id>' (auth=user)
- نقطة HTTP: '/dashboard/builder/export/excel/<int:dashboard_id>' (auth=user)
- نقطة HTTP: '/dashboard/builder/api/items/<int:item_id>/data' (auth=public)
- نقطة HTTP: '/dashboard/builder/api/widgets/<int:widget_id>/data' (auth=user)
- نقطة HTTP: '/dashboard/builder/api/items/<int:item_id>/configure' (auth=user)
- نقطة HTTP: '/dashboard/builder/api/items/<int:item_id>/update' (auth=user)
- نقطة HTTP: '/dashboard/builder/api/items/<int:item_id>/duplicate' (auth=user)
- نقطة HTTP: '/dashboard/builder/api/items/<int:item_id>/delete' (auth=user)
- نقطة HTTP: '/dashboard/builder/api/items/create' (auth=user)
- نقطة HTTP: '/dashboard/builder/api/items/reorder' (auth=user)
- نقطة HTTP: '/dashboard/builder/api/dashboard/<int:dashboard_id>/layout' (auth=user)
- نقطة HTTP: '/dashboard/builder/api/dashboard/<int:dashboard_id>/duplicate' (auth=user)
- نقطة HTTP: '/dashboard/builder/api/dashboard/<int:dashboard_id>/delete' (auth=user)

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `web`, `mail`, `base_setup`
