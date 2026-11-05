# El-Nmo - Credit Limit Approval Workflow

- **المسار والإصدار:** `odoo19/el_nmo_credit_approval` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Approval workflow for sale orders exceeding customer credit limits.

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Credit Approval
- المستخدم يبدأ من قائمة: Approval Requests
- المستخدم يبدأ من قائمة: Rejection Reasons
- النموذج/الامتداد المعني: CreditApprovalRequest: model _name
- النموذج/الامتداد المعني: CreditRejectionReason: model _name
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- النموذج/الامتداد المعني: CreditApprovalWizard: model _name
- العملية البرمجية المتاحة: `test_07_credit_policy_warning_allows_confirm` في `tests/test_credit_approval.py`
- العملية البرمجية المتاحة: `_compute_display_name` في `models/credit_approval_request.py`
- العملية البرمجية المتاحة: `create` في `models/credit_approval_request.py`
- العملية البرمجية المتاحة: `action_submit` في `models/credit_approval_request.py`
- العملية البرمجية المتاحة: `action_approve` في `models/credit_approval_request.py`
- العملية البرمجية المتاحة: `action_reject` في `models/credit_approval_request.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/credit_approval_request.py`
- العملية البرمجية المتاحة: `action_resubmit` في `models/credit_approval_request.py`
- العملية البرمجية المتاحة: `_create_from_sale_order` في `models/credit_approval_request.py`
- العملية البرمجية المتاحة: `_compute_is_credit_blocked` في `models/sale_order.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/sale_order.py`
- العملية البرمجية المتاحة: `_create_credit_activity` في `models/sale_order.py`
- العملية البرمجية المتاحة: `action_approve` في `wizard/credit_approval_wizard.py`
- العملية البرمجية المتاحة: `action_reject` في `wizard/credit_approval_wizard.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
