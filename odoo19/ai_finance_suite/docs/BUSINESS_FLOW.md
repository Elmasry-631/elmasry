# AI Finance

- **المسار والإصدار:** `odoo19/ai_finance_suite` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** AI-Powered Finance Suite: Virtual CFO, OCR Engine & Smart Reconciliation for Odoo 19

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: AI Finance
- المستخدم يبدأ من قائمة: Dashboard
- المستخدم يبدأ من قائمة: Analytics
- المستخدم يبدأ من قائمة: OCR Engine
- المستخدم يبدأ من قائمة: Virtual CFO (Chatbot)
- المستخدم يبدأ من قائمة: Reconciliation
- المستخدم يبدأ من قائمة: Partner Statements
- المستخدم يبدأ من قائمة: Bank Statements
- المستخدم يبدأ من قائمة: Configuration
- المستخدم يبدأ من قائمة: AI Credentials
- المستخدم يبدأ من قائمة: Settings
- النموذج/الامتداد المعني: AccountBankStatementFix: model _inherit
- النموذج/الامتداد المعني: BankStatement: model _name
- النموذج/الامتداد المعني: BankStatementLine: model _name
- النموذج/الامتداد المعني: AICredential: model _name
- النموذج/الامتداد المعني: VendorStatement: model _name
- النموذج/الامتداد المعني: VendorStatementLine: model _name
- النموذج/الامتداد المعني: VendorStatementColumn: model _name
- النموذج/الامتداد المعني: VirtualCFOAgent: model _name
- النموذج/الامتداد المعني: CFOConversation: model _name
- النموذج/الامتداد المعني: VendorBillWizard: model _name
- النموذج/الامتداد المعني: VendorBillWizardLine: model _name
- النموذج/الامتداد المعني: VendorBillWizardColumn: model _name
- العملية البرمجية المتاحة: `_compute_journal_has_invalid_statements` في `models/account_bank_statement.py`
- العملية البرمجية المتاحة: `_compute_summary` في `models/bank_statement.py`
- العملية البرمجية المتاحة: `create` في `models/bank_statement.py`
- العملية البرمجية المتاحة: `_compute_odoo_balance` في `models/bank_statement.py`
- العملية البرمجية المتاحة: `_compute_difference` في `models/bank_statement.py`
- العملية البرمجية المتاحة: `action_match_lines` في `models/bank_statement.py`
- العملية البرمجية المتاحة: `action_confirm_matches` في `models/bank_statement.py`
- العملية البرمجية المتاحة: `action_rematch` في `models/bank_statement.py`
- العملية البرمجية المتاحة: `action_print_report` في `models/bank_statement.py`
- العملية البرمجية المتاحة: `action_test_connection` في `models/ai_credential.py`
- العملية البرمجية المتاحة: `_compute_summary` في `models/vendor_statement.py`
- العملية البرمجية المتاحة: `create` في `models/vendor_statement.py`
- العملية البرمجية المتاحة: `_compute_odoo_total` في `models/vendor_statement.py`
- العملية البرمجية المتاحة: `_compute_difference` في `models/vendor_statement.py`
- العملية البرمجية المتاحة: `action_match_lines` في `models/vendor_statement.py`
- العملية البرمجية المتاحة: `action_confirm_matches` في `models/vendor_statement.py`
- العملية البرمجية المتاحة: `action_rematch` في `models/vendor_statement.py`
- العملية البرمجية المتاحة: `action_print_report` في `models/vendor_statement.py`
- العملية البرمجية المتاحة: `_compute_display_label` في `models/vendor_statement.py`
- العملية البرمجية المتاحة: `create` في `models/virtual_cfo_agent.py`
- العملية البرمجية المتاحة: `_compute_stats` في `models/virtual_cfo_agent.py`
- العملية البرمجية المتاحة: `action_new_conversation` في `models/virtual_cfo_agent.py`
- العملية البرمجية المتاحة: `action_view_recommendations` في `models/virtual_cfo_agent.py`
- العملية البرمجية المتاحة: `action_generate_insights` في `models/virtual_cfo_agent.py`
- العملية البرمجية المتاحة: `action_select_type` في `wizards/vendor_bill_wizard.py`
- العملية البرمجية المتاحة: `action_back_to_type` في `wizards/vendor_bill_wizard.py`
- العملية البرمجية المتاحة: `action_process_file` في `wizards/vendor_bill_wizard.py`
- العملية البرمجية المتاحة: `_create_bill_direct` في `wizards/vendor_bill_wizard.py`
- العملية البرمجية المتاحة: `_create_refund_direct` في `wizards/vendor_bill_wizard.py`
- العملية البرمجية المتاحة: `_process_with_gemini_vision` في `wizards/vendor_bill_wizard.py`
- العملية البرمجية المتاحة: `_process_statement_with_gemini` في `wizards/vendor_bill_wizard.py`
- العملية البرمجية المتاحة: `_process_statement_excel` في `wizards/vendor_bill_wizard.py`
- العملية البرمجية المتاحة: `_create_statement_direct` في `wizards/vendor_bill_wizard.py`
- العملية البرمجية المتاحة: `_create_and_match_statement` في `wizards/vendor_bill_wizard.py`
- العملية البرمجية المتاحة: `_process_bank_statement_with_gemini` في `wizards/vendor_bill_wizard.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
