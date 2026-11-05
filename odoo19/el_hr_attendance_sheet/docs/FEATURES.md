# HR Attendance Sheet And Policies

- **المسار والإصدار:** `odoo19/el_hr_attendance_sheet` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Calculate overtime, lateness, absence from attendance and feed payslip

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Calculate overtime, lateness, absence from attendance and feed payslip
- نموذج Odoo: HrAttendanceSheetReport: model _name
- نموذج Odoo: HrPayrollStructure: model _inherit
- نموذج Odoo: HrAttendanceSheetBatch: model _name
- نموذج Odoo: HrAttendanceSheetBatchLine: model _name
- نموذج Odoo: HrPayslip: model _inherit
- نموذج Odoo: HrAttendancePublicHoliday: model _name
- نموذج Odoo: HrAttendancePublicHolidayLine: model _name
- نموذج Odoo: HrContract: model _inherit
- نموذج Odoo: HrEmployee: model _inherit
- نموذج Odoo: HrAttendancePolicy: model _name
- نموذج Odoo: HrAttendanceRuleOvertime: model _name
- نموذج Odoo: HrAttendanceRuleLateness: model _name
- نموذج Odoo: HrAttendanceRuleLatenessTier: model _name
- نموذج Odoo: HrAttendanceRuleLatenessStep: model _name
- نموذج Odoo: HrAttendanceRuleAbsence: model _name
- نموذج Odoo: HrAttendanceRuleAbsenceTier: model _name
- نموذج Odoo: HrAttendanceRuleAbsenceStep: model _name
- نموذج Odoo: HrAttendanceSheet: model _name
- نموذج Odoo: HrAttendanceSheetLine: model _name
- نموذج Odoo: HrAttendanceSheetBatchWizard: model _name
- نموذج Odoo: HrAttendanceChangeDataWizard: model _name
- نموذج Odoo: HrAttendanceCreatePayslipWizard: model _name
- قائمة واجهة: Attendance Sheets
- قائمة واجهة: Attendance Sheets
- قائمة واجهة: Batches
- قائمة واجهة: Configuration
- قائمة واجهة: Public Holidays
- قائمة واجهة: Rules
- قائمة واجهة: Overtime Rules
- قائمة واجهة: Lateness Rules
- قائمة واجهة: Absence Rules
- قائمة واجهة: Attendance Policies

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `hr_attendance`, `hr`, `hr_payroll`, `hr_holidays`, `mail`, `calendar`
