# Transaction Tracker

- **المسار والإصدار:** `odoo19/transaction_tracker` — Odoo 19
- **إصدار الحزمة:** `1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track all user transactions across every Odoo module

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Transaction Tracker
- المستخدم يبدأ من قائمة: Transaction Logs
- المستخدم يبدأ من قائمة: Dashboard
- المستخدم يبدأ من قائمة: Configuration
- المستخدم يبدأ من قائمة: Tracker Settings
- المستخدم يبدأ من قائمة: Reports
- المستخدم يبدأ من قائمة: Transaction Report
- النموذج/الامتداد المعني: TransactionLogReport: model _name
- النموذج/الامتداد المعني: TransactionTrackerConfig: model _name
- النموذج/الامتداد المعني: TransactionLog: model _name
- النموذج/الامتداد المعني: Base: model _inherit
- العملية البرمجية المتاحة: `_get_report_values` في `report/transaction_log_report.py`
- العملية البرمجية المتاحة: `create` في `models/tracker_config.py`
- العملية البرمجية المتاحة: `_invalidate_tracker_cache` في `models/tracker_config.py`
- العملية البرمجية المتاحة: `action_track_all` في `models/tracker_config.py`
- العملية البرمجية المتاحة: `action_untrack_all` في `models/tracker_config.py`
- العملية البرمجية المتاحة: `action_auto_populate_models` في `models/tracker_config.py`
- العملية البرمجية المتاحة: `_compute_record_ref` في `models/transaction_log.py`
- العملية البرمجية المتاحة: `create` في `models/transaction_log.py`
- العملية البرمجية المتاحة: `write` في `models/transaction_log.py`
- العملية البرمجية المتاحة: `unlink` في `models/transaction_log.py`
- العملية البرمجية المتاحة: `action_open_record` في `models/transaction_log.py`
- العملية البرمجية المتاحة: `action_export_pdf` في `models/transaction_log.py`
- العملية البرمجية المتاحة: `action_export_excel` في `models/transaction_log.py`
- العملية البرمجية المتاحة: `_log_operation` في `models/transaction_log.py`
- العملية البرمجية المتاحة: `_get_ip_address` في `models/transaction_log.py`
- العملية البرمجية المتاحة: `get_dashboard_data` في `models/transaction_log.py`
- العملية البرمجية المتاحة: `create` في `models/base_hook.py`
- العملية البرمجية المتاحة: `_track_create` في `models/base_hook.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
