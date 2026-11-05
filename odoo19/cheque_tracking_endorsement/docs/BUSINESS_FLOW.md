# Cheque Tracking Endorsement

- **المسار والإصدار:** `odoo19/cheque_tracking_endorsement` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Cheque endorsement workflow for cheque tracking

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Endorsements
- النموذج/الامتداد المعني: ResCompany: model _inherit
- النموذج/الامتداد المعني: ResConfigSettings: model _inherit
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: ChequeEndorsement: model _name
- النموذج/الامتداد المعني: ChequeCheque: model _inherit
- النموذج/الامتداد المعني: ChequeEndorseWizard: model _name
- العملية البرمجية المتاحة: `action_view_cheque` في `models/account_move.py`
- العملية البرمجية المتاحة: `create` في `models/cheque_endorsement.py`
- العملية البرمجية المتاحة: `create` في `models/cheque.py`
- العملية البرمجية المتاحة: `_compute_endorsement_count` في `models/cheque.py`
- العملية البرمجية المتاحة: `_compute_date_flags` في `models/cheque.py`
- العملية البرمجية المتاحة: `_create_endorsement_move` في `models/cheque.py`
- العملية البرمجية المتاحة: `_create_vendor_bill_for_endorsement` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_open_endorse_wizard` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_endorse` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_deposit` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_view_endorsements` في `models/cheque.py`
- العملية البرمجية المتاحة: `action_confirm` في `wizards/endorse_wizard.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
