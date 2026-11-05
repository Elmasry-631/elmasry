# Transaction Tracker

- **المسار والإصدار:** `odoo19/transaction_tracker` — Odoo 19
- **إصدار الحزمة:** `1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track all user transactions across every Odoo module

## المكونات المكتشفة

- Python: 8 file(s)
- XML: 8 file(s)
- JavaScript/TypeScript: 1 file(s)

### نماذج وامتدادات Odoo

- TransactionLogReport: model _name
- TransactionTrackerConfig: model _name
- TransactionLog: model _name
- Base: model _inherit

### الملفات المصدرية ذات الصلة

- `report/transaction_log_report.py`
- `report/__init__.py`
- `report/transaction_log_report_template.xml`
- `report/transaction_log_report.xml`
- `views/dashboard_views.xml`
- `views/transaction_log_views.xml`
- `views/menu_views.xml`
- `views/tracker_config_views.xml`
- `models/tracker_config.py`
- `models/transaction_log.py`
- `models/__init__.py`
- `models/base_hook.py`
- `security/security.xml`
- `security/ir.model.access.csv`

### حقول معلنة

- `model_id (Many2one)`
- `model_name (Char)`
- `track_create (Boolean)`
- `track_write (Boolean)`
- `track_unlink (Boolean)`
- `track_read (Boolean)`
- `active (Boolean)`
- `company_id (Many2one)`
- `name (Char)`
- `user_id (Many2one)`
- `model_name (Char)`
- `res_id (Integer)`
- `record_display_name (Char)`
- `operation (Selection)`
- `module_name (Char)`
- `old_values (Text)`
- `new_values (Text)`
- `changed_fields (Char)`
- `ip_address (Char)`
- `company_id (Many2one)`
- `is_suspicious (Boolean)`
- `note (Text)`
- `record_ref (Char)`

### XML IDs

- `report/transaction_log_report_template.xml::report_transaction_log_document`
- `report/transaction_log_report_template.xml::report_transaction_log`
- `report/transaction_log_report.xml::action_report_transaction_log`
- `report/transaction_log_report.xml::action_report_transaction_log_menu`
- `views/dashboard_views.xml::action_transaction_dashboard`
- `views/transaction_log_views.xml::view_transaction_log_form`
- `views/transaction_log_views.xml::view_transaction_log_list`
- `views/transaction_log_views.xml::view_transaction_log_search`
- `views/transaction_log_views.xml::view_transaction_log_pivot`
- `views/transaction_log_views.xml::view_transaction_log_graph`
- `views/transaction_log_views.xml::view_transaction_log_kanban`
- `views/transaction_log_views.xml::action_transaction_log`
- `views/menu_views.xml::menu_transaction_tracker_root`
- `views/menu_views.xml::menu_transaction_log`
- `views/menu_views.xml::menu_transaction_dashboard`
- `views/menu_views.xml::menu_transaction_tracker_config`
- `views/menu_views.xml::menu_tracker_config`
- `views/menu_views.xml::menu_transaction_reports`
- `views/menu_views.xml::menu_transaction_log_report`
- `views/tracker_config_views.xml::view_tracker_config_form`
- `views/tracker_config_views.xml::view_tracker_config_list`
- `views/tracker_config_views.xml::view_tracker_config_search`
- `views/tracker_config_views.xml::action_tracker_config`
- `data/default_config.xml::seq_transaction_log`
- `security/security.xml::group_transaction_tracker_manager`
- `security/security.xml::group_transaction_tracker_user`
- `security/security.xml::transaction_log_manager_rule`
- `security/security.xml::transaction_log_user_rule`
- `security/security.xml::tracker_config_manager_rule`