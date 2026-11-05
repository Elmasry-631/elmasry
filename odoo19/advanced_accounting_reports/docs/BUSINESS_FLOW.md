# Advanced Accounting Reports

- **المسار والإصدار:** `odoo19/advanced_accounting_reports` — Odoo 19
- **إصدار الحزمة:** `1.20.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Advanced General Ledger, Trial Balance with Analytic Dimensions & Multi-Currency

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Advanced Dimensions
- المستخدم يبدأ من قائمة: Features
- المستخدم يبدأ من قائمة: Cost Centers
- المستخدم يبدأ من قائمة: Patch Numbers
- المستخدم يبدأ من قائمة: General Ledger (Advanced)
- المستخدم يبدأ من قائمة: Trial Balance (Advanced)
- النموذج/الامتداد المعني: TrialBalanceReport: model _name
- النموذج/الامتداد المعني: GeneralLedgerReport: model _name
- النموذج/الامتداد المعني: ResCompany: model _inherit
- النموذج/الامتداد المعني: AccountFeature: model _name
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: AccountPatchNumber: model _name
- النموذج/الامتداد المعني: AccountMoveLine: model _inherit
- النموذج/الامتداد المعني: AccountCostCenter: model _name
- النموذج/الامتداد المعني: TrialBalanceWizard: model _name
- النموذج/الامتداد المعني: GeneralLedgerWizard: model _name
- العملية البرمجية المتاحة: `_get_header_format` في `controllers/xlsx_export.py`
- العملية البرمجية المتاحة: `_get_title_format` في `controllers/xlsx_export.py`
- العملية البرمجية المتاحة: `_get_number_format` في `controllers/xlsx_export.py`
- العملية البرمجية المتاحة: `_get_text_format` في `controllers/xlsx_export.py`
- العملية البرمجية المتاحة: `_get_total_format` في `controllers/xlsx_export.py`
- العملية البرمجية المتاحة: `_get_info_format` في `controllers/xlsx_export.py`
- العملية البرمجية المتاحة: `_get_info_value_format` في `controllers/xlsx_export.py`
- العملية البرمجية المتاحة: `_resolve_secondary_currency` في `controllers/xlsx_export.py`
- العملية البرمجية المتاحة: `export_general_ledger_xlsx` في `controllers/xlsx_export.py`
- العملية البرمجية المتاحة: `export_trial_balance_xlsx` في `controllers/xlsx_export.py`
- العملية البرمجية المتاحة: `_compute_debit_credit_balance` في `models/account_feature.py`
- العملية البرمجية المتاحة: `_compute_secondary_totals` في `models/account_move.py`
- العملية البرمجية المتاحة: `_compute_secondary_currency_symbol` في `models/account_move_line.py`
- العملية البرمجية المتاحة: `_compute_secondary_amounts` في `models/account_move_line.py`
- العملية البرمجية المتاحة: `_compute_secondary_balance` في `models/account_move_line.py`
- العملية البرمجية المتاحة: `_compute_debit_credit_balance` في `models/account_cost_center.py`
- العملية البرمجية المتاحة: `_compute_balances` في `wizard/trial_balance_wizard.py`
- العملية البرمجية المتاحة: `action_view_report` في `wizard/trial_balance_wizard.py`
- العملية البرمجية المتاحة: `action_export_excel` في `wizard/trial_balance_wizard.py`
- العملية البرمجية المتاحة: `action_export_pdf` في `wizard/trial_balance_wizard.py`
- العملية البرمجية المتاحة: `_compute_balances` في `wizard/general_ledger_wizard.py`
- العملية البرمجية المتاحة: `action_view_report` في `wizard/general_ledger_wizard.py`
- العملية البرمجية المتاحة: `action_export_excel` في `wizard/general_ledger_wizard.py`
- العملية البرمجية المتاحة: `action_export_pdf` في `wizard/general_ledger_wizard.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
