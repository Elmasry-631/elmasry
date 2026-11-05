# HR Attendance Sheet and Policies

- **المسار والإصدار:** `odoo19/rm_hr_attendance_sheet` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Attendance sheets, policies, overtime, lateness, absence, and payroll links

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Attendance Sheets
- المستخدم يبدأ من قائمة: Attendance Sheets
- المستخدم يبدأ من قائمة: Batch Attendance Sheets
- المستخدم يبدأ من قائمة: Attendance Policies
- المستخدم يبدأ من قائمة: Attendance Policies
- المستخدم يبدأ من قائمة: Overtime Rules
- المستخدم يبدأ من قائمة: Lateness Rules
- المستخدم يبدأ من قائمة: Absence Rules
- المستخدم يبدأ من قائمة: Public Holidays
- النموذج/الامتداد المعني: HrPayslip: model _inherit
- النموذج/الامتداد المعني: RmAttendanceSheet: model _name
- النموذج/الامتداد المعني: RmAttendanceSheetLine: model _name
- النموذج/الامتداد المعني: RmAttendancePolicy: model _name
- النموذج/الامتداد المعني: ResourceCalendarLeaves: model _inherit
- النموذج/الامتداد المعني: RmLatenessRule: model _name
- النموذج/الامتداد المعني: RmLatenessStep: model _name
- النموذج/الامتداد المعني: RmAbsenceRule: model _name
- النموذج/الامتداد المعني: RmAbsenceStep: model _name
- النموذج/الامتداد المعني: HrSalaryRule: model _inherit
- النموذج/الامتداد المعني: HrVersion: model _inherit
- النموذج/الامتداد المعني: RmOvertimeRule: model _name
- النموذج/الامتداد المعني: RmAttendanceSheetChangeWizard: model _name
- النموذج/الامتداد المعني: RmAttendanceSheetBatchWizard: model _name
- العملية البرمجية المتاحة: `_compute_name` في `models/rm_attendance_sheet.py`
- العملية البرمجية المتاحة: `_compute_totals` في `models/rm_attendance_sheet.py`
- العملية البرمجية المتاحة: `action_calculate` في `models/rm_attendance_sheet.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/rm_attendance_sheet.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/rm_attendance_sheet.py`
- العملية البرمجية المتاحة: `action_draft` في `models/rm_attendance_sheet.py`
- العملية البرمجية المتاحة: `action_open_change_wizard` في `models/rm_attendance_sheet.py`
- العملية البرمجية المتاحة: `action_create_payslip` في `models/rm_attendance_sheet.py`
- العملية البرمجية المتاحة: `_generate_sheet_lines` في `models/rm_attendance_sheet.py`
- العملية البرمجية المتاحة: `_compute_name` في `models/rm_attendance_sheet.py`
- العملية البرمجية المتاحة: `_compute_day_name` في `models/rm_attendance_sheet.py`
- العملية البرمجية المتاحة: `_compute_name` في `models/rm_lateness_rule.py`
- العملية البرمجية المتاحة: `_compute_name` في `models/rm_absence_rule.py`
- العملية البرمجية المتاحة: `action_apply` في `wizards/rm_attendance_sheet_change.py`
- العملية البرمجية المتاحة: `action_create_sheets` في `wizards/rm_attendance_sheet_batch.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
