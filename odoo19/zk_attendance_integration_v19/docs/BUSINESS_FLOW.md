# TechScope | ZK Attendance Integration

- **المسار والإصدار:** `odoo19/zk_attendance_integration_v19` — Odoo 19
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `غير محدد في manifest`
- **الملخص المعلن:** Integration with ZK Attendance Machines

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Configuration
- المستخدم يبدأ من قائمة: ZK Attendance Machines
- المستخدم يبدأ من قائمة: ZK Attendance Machines
- المستخدم يبدأ من قائمة: Attendance Machines
- المستخدم يبدأ من قائمة: Attendance Logs
- النموذج/الامتداد المعني: ZKAttendanceSettings: model _inherit
- النموذج/الامتداد المعني: HrEmployee: model _inherit
- النموذج/الامتداد المعني: zk_attendance_tmp: model _name
- النموذج/الامتداد المعني: zk_attendance_machine: model _name
- النموذج/الامتداد المعني: HrAttendance: model _inherit
- العملية البرمجية المتاحة: `sudo_create_log` في `models/models.py`
- العملية البرمجية المتاحة: `_compute_user` في `models/models.py`
- العملية البرمجية المتاحة: `_compute_date` في `models/models.py`
- العملية البرمجية المتاحة: `_compute_local_date` في `models/models.py`
- العملية البرمجية المتاحة: `process_data` في `models/models.py`
- العملية البرمجية المتاحة: `create` في `models/models.py`
- العملية البرمجية المتاحة: `process` في `models/models.py`
- العملية البرمجية المتاحة: `_compute_hhmm_worked` في `models/models.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
