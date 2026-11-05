# Cheque Tracking

- **المسار والإصدار:** `odoo19/cheque_tracking` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track received and issued cheques with accounting lifecycle entries

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Cheque Tracking
- المستخدم يبدأ من قائمة: Operations
- المستخدم يبدأ من قائمة: Received Cheques
- المستخدم يبدأ من قائمة: Issued Cheques
- المستخدم يبدأ من قائمة: All Cheques
- المستخدم يبدأ من قائمة: Deposits
- المستخدم يبدأ من قائمة: Returns
- المستخدم يبدأ من قائمة: Reporting
- المستخدم يبدأ من قائمة: Cheque Analysis
- المستخدم يبدأ من قائمة: Configuration
- المستخدم يبدأ من قائمة: Return Reasons
- المستخدم يبدأ من قائمة: Settings
- النموذج/الامتداد المعني: ResCompany: model _inherit
- النموذج/الامتداد المعني: ResPartner: model _inherit
- النموذج/الامتداد المعني: ChequeDeposit: model _name
- النموذج/الامتداد المعني: ChequeReturn: model _name
- النموذج/الامتداد المعني: ResConfigSettings: model _inherit
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: ChequeReturnReason: model _name
- النموذج/الامتداد المعني: ChequeCheque: model _name
- النموذج/الامتداد المعني: ChequeDepositWizard: model _name
- النموذج/الامتداد المعني: ChequeReturnWizard: model _name
- النموذج/الامتداد المعني: ChequePrintWizard: model _name
- العملية البرمجية المتاحة: `_compute_cheque_stats` في `models/res_partner.py`
- العملية البرمجية المتاحة: `action_view_received_cheques` في `models/res_partner.py`
- العملية البرمجية المتاحة: `action_view_issued_cheques` في `models/res_partner.py`
- العملية البرمجية المتاحة: `_action_view_cheques` في `models/res_partner.py`
- العملية البرمجية المتاحة: `create` في `models/deposit.py`
- العملية البرمجية المتاحة: `_compute_total_amount` في `models/deposit.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/deposit.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/deposit.py`
- العملية البرمجية المتاحة: `action_print_deposit_slip` في `models/deposit.py`
- العملية البرمجية المتاحة: `create` في `models/cheque_return.py`
- العملية البرمجية المتاحة: `create` في `models/cheque.py`
- العملية البرمجية المتاحة: `_compute_amount_company_currency` في `models/cheque.py`
- العملية البرمجية المتاحة: `_compute_date_flags` في `models/cheque.py`
- العملية البرمجية المتاحة: `_compute_move_count` في `models/cheque.py`
- العملية البرمجية المتاحة: `_compute_days` في `models/cheque.py`
- العملية البرمجية المتاحة: `_compute_return_info` في `models/cheque.py`
- العملية البرمجية المتاحة: `_create_move` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_submit` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_approve` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_deposit` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_clear` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_mark_cashed` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_hand_over` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_void` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_open_return_wizard` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_print_cheque` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_view_entries` في `models/cheque.py`
- العملية البرمجية المتاحة: `_create_high_value_activity` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_create_deposit` في `wizards/deposit_wizard.py`
- العملية البرمجية المتاحة: `action_return_cheque` في `wizards/return_wizard.py`
- العملية البرمجية المتاحة: `action_print` في `wizards/print_wizard.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
