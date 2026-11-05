# Dashboard Builder

- **المسار والإصدار:** `odoo20/el_dashboard_builder` — Odoo 20
- **إصدار الحزمة:** `20.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Drag-and-drop dashboard builder with customizable widgets

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Dashboard Builder
- المستخدم يبدأ من قائمة: My Dashboards
- المستخدم يبدأ من قائمة: New Dashboard
- المستخدم يبدأ من قائمة: Favorites
- المستخدم يبدأ من قائمة: All Dashboards
- المستخدم يبدأ من قائمة: Widget Library
- المستخدم يبدأ من قائمة: Shared Dashboards
- المستخدم يبدأ من قائمة: Configuration
- المستخدم يبدأ من قائمة: Tags
- النموذج/الامتداد المعني: DashboardBuilderReport: model _name
- النموذج/الامتداد المعني: DashboardExportWizard: model _name
- النموذج/الامتداد المعني: Dashboard: model _name
- النموذج/الامتداد المعني: DashboardTag: model _name
- النموذج/الامتداد المعني: DashboardWidget: model _name
- النموذج/الامتداد المعني: DashboardItem: model _name
- النموذج/الامتداد المعني: DashboardShare: model _name
- النموذج/الامتداد المعني: DashboardItemConfigWizard: model _name
- العملية البرمجية المتاحة: `test_dashboard_export_import` في `tests/test_dashboard_builder.py`
- العملية البرمجية المتاحة: `test_dashboard_view_action` في `tests/test_dashboard_builder.py`
- العملية البرمجية المتاحة: `test_dashboard_edit_action` في `tests/test_dashboard_builder.py`
- العملية البرمجية المتاحة: `test_widget_test_action` في `tests/test_dashboard_builder.py`
- العملية البرمجية المتاحة: `generate_dashboard_pdf` في `report/report.py`
- العملية البرمجية المتاحة: `_generate_fallback_pdf` في `report/report.py`
- العملية البرمجية المتاحة: `generate_dashboard_excel` في `report/report.py`
- العملية البرمجية المتاحة: `action_export` في `report/report.py`
- العملية البرمجية المتاحة: `dashboard_export_json` في `controllers/controllers.py`
- العملية البرمجية المتاحة: `dashboard_export_pdf` في `controllers/controllers.py`
- العملية البرمجية المتاحة: `dashboard_export_excel` في `controllers/controllers.py`
- العملية البرمجية المتاحة: `create_item` في `controllers/controllers.py`
- العملية البرمجية المتاحة: `_data_DashboardActionButtons` في `controllers/controllers.py`
- العملية البرمجية المتاحة: `_compute_item_count` في `models/dashboard.py`
- العملية البرمجية المتاحة: `_compute_is_favorite` في `models/dashboard.py`
- العملية البرمجية المتاحة: `action_open_dashboard` في `models/dashboard.py`
- العملية البرمجية المتاحة: `action_edit_dashboard` في `models/dashboard.py`
- العملية البرمجية المتاحة: `action_duplicate` في `models/dashboard.py`
- العملية البرمجية المتاحة: `action_toggle_favorite` في `models/dashboard.py`
- العملية البرمجية المتاحة: `action_export_config` في `models/dashboard.py`
- العملية البرمجية المتاحة: `import_dashboard_config` في `models/dashboard.py`
- العملية البرمجية المتاحة: `_compute_dashboard_count` في `models/dashboard.py`
- العملية البرمجية المتاحة: `action_test_widget` في `models/dashboard.py`
- العملية البرمجية المتاحة: `action_configure` في `models/dashboard.py`
- العملية البرمجية المتاحة: `action_remove` في `models/dashboard.py`
- العملية البرمجية المتاحة: `action_duplicate` في `models/dashboard.py`
- العملية البرمجية المتاحة: `create` في `models/dashboard.py`
- العملية البرمجية المتاحة: `action_regenerate_token` في `models/dashboard.py`
- العملية البرمجية المتاحة: `_compute_config_fields` في `wizard/item_config_wizard.py`
- العملية البرمجية المتاحة: `action_save` في `wizard/item_config_wizard.py`
- العملية البرمجية المتاحة: `action_reset` في `wizard/item_config_wizard.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
