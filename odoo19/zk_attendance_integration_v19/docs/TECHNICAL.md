# TechScope | ZK Attendance Integration

- **المسار والإصدار:** `odoo19/zk_attendance_integration_v19` — Odoo 19
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `غير محدد في manifest`
- **الملخص المعلن:** Integration with ZK Attendance Machines

## المكونات المكتشفة

- Python: 7 file(s)
- XML: 2 file(s)

### نماذج وامتدادات Odoo

- ZKAttendanceSettings: model _inherit
- HrEmployee: model _inherit
- zk_attendance_tmp: model _name
- zk_attendance_machine: model _name
- HrAttendance: model _inherit

### الملفات المصدرية ذات الصلة

- `controllers/__init__.py`
- `controllers/controllers.py`
- `views/views.xml`
- `models/zk_attendance.py`
- `models/models.py`
- `models/__init__.py`
- `security/ir.model.access.csv`

### حقول معلنة

- `no_checkout_mode (Selection)`
- `deflt_time (Float)`
- `api_ip (Char)`
- `api_port (Char)`
- `zk_emp_id (Char)`
- `machine_id (Many2one)`
- `user_number (Char)`
- `user (Many2one)`
- `date (Datetime)`
- `local_date (Datetime)`
- `date_temp (Date)`
- `inoutmode (Char)`
- `logged (Boolean)`
- `reversed (Boolean)`
- `machine_number (Integer)`
- `name (Char)`
- `ip (Char)`
- `port (Integer)`
- `sync (Boolean)`
- `model (Char)`
- `date_sync (Datetime)`
- `date_sync_success (Datetime)`
- `manual_upload_sync_date (Datetime)`
- `sync_error (Text)`
- `last_download_log (Datetime)`
- `no_checkout (Boolean)`
- `missing_check (Boolean)`
- `no_check_in (Boolean)`
- `local_check_in (Datetime)`
- `local_check_out (Datetime)`
- `hhmm_worked (Char)`

### XML IDs

- `views/views.xml::ir_cron_attendance_process`
- `views/views.xml::attendance_machine_logs_tree_view`
- `views/views.xml::zk_config`
- `views/views.xml::hr_atten_settings_action`
- `views/views.xml::zk_conf`
- `views/views.xml::zk_conf_settings`
- `views/views.xml::attendance_machine_tree_view`
- `views/views.xml::inherit_hr_employee`
- `views/views.xml::attendance_machine_form_view`
- `views/views.xml::missing_in_out_tree_inherit`
- `views/views.xml::act_attendance_machine`
- `views/views.xml::act_attendance_logs`
- `views/views.xml::attendance_zk_main_menu`
- `views/views.xml::attendance_machine_menu`
- `views/views.xml::attendance_log_menu`