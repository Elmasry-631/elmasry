# Payroll WPS Export

- **المسار والإصدار:** `odoo19/el_payroll_wps` — Odoo 19
- **إصدار الحزمة:** `19.0.1.2.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Adds an 'Others' field to payslips and the bank salary file export (WPS)

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: WPS Export
- النموذج/الامتداد المعني: HrPayslip: model _inherit
- النموذج/الامتداد المعني: WpsExportWizard: model _name
- العملية البرمجية المتاحة: `setUpClass` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `_make_employee` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `_validated_slip` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `_wizard` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `_export` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `test_others_field_is_the_other_allowances` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `test_bank_file_has_the_template_layout_and_correct_amounts` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `test_missing_bank_account_or_id_blocks_the_export` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `test_payslips_of_an_employee_in_the_month_are_added_together` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `test_draft_payslips_and_other_months_are_not_exported` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `test_csv_bank_file_has_the_bank_columns_and_correct_amounts` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `test_csv_export_is_blocked_like_the_excel_one` في `tests/test_wps_export.py`
- العملية البرمجية المتاحة: `_compute_x_others` في `models/hr_payslip.py`
- العملية البرمجية المتاحة: `compute_sheet` في `models/hr_payslip.py`
- العملية البرمجية المتاحة: `_period` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `_get_payslips` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `_get_employee_address` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `_get_bank_account` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `_get_bank_name` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `_collect_rows` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `_compute_preview` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `_build_xlsx` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `_build_csv` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `_export_rows` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `action_export` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `action_export_csv` في `wizard/wps_export_wizard.py`
- العملية البرمجية المتاحة: `_offer_file` في `wizard/wps_export_wizard.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
