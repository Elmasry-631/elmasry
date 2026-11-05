# Sale Contract Auto

- **المسار والإصدار:** `odoo18/sale_contract_auto` — Odoo 18
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automatically generate contracts from sale orders

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Contract Templates
- المستخدم يبدأ من قائمة: Contracts
- المستخدم يبدأ من قائمة: Contracts
- المستخدم يبدأ من قائمة: Contract Titles
- المستخدم يبدأ من قائمة: Customers
- النموذج/الامتداد المعني: ContractDocument: model _name
- النموذج/الامتداد المعني: SaleContract: model _name
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: ContractTitle: model _name
- النموذج/الامتداد المعني: ContractAmendment: model _name
- النموذج/الامتداد المعني: ContractTemplate: model _name
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- النموذج/الامتداد المعني: ResPartner: model _inherit
- النموذج/الامتداد المعني: SaleContractLine: model _name
- النموذج/الامتداد المعني: ContractClause: model _name
- النموذج/الامتداد المعني: ContractPaymentSchedule: model _name
- العملية البرمجية المتاحة: `_compute_uploaded` في `models/contract_document.py`
- العملية البرمجية المتاحة: `_compute_subtotal_total` في `models/sale_contract.py`
- العملية البرمجية المتاحة: `create` في `models/sale_contract.py`
- العملية البرمجية المتاحة: `action_set_active` في `models/sale_contract.py`
- العملية البرمجية المتاحة: `action_financial_approve` في `models/sale_contract.py`
- العملية البرمجية المتاحة: `action_legal_approve` في `models/sale_contract.py`
- العملية البرمجية المتاحة: `action_finish` في `models/sale_contract.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/sale_contract.py`
- العملية البرمجية المتاحة: `action_reset_to_draft` في `models/sale_contract.py`
- العملية البرمجية المتاحة: `_compute_access_url` في `models/sale_contract.py`
- العملية البرمجية المتاحة: `action_send_contract_link` في `models/sale_contract.py`
- العملية البرمجية المتاحة: `_compute_second_party_address` في `models/sale_contract.py`
- العملية البرمجية المتاحة: `create` في `models/contract_amendment.py`
- العملية البرمجية المتاحة: `_compute_contract_count` في `models/sale_order.py`
- العملية البرمجية المتاحة: `_compute_contract` في `models/sale_order.py`
- العملية البرمجية المتاحة: `action_view_contract` في `models/sale_order.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/sale_order.py`
- العملية البرمجية المتاحة: `_compute_subtotal` في `models/sale_contract_line.py`
- العملية البرمجية المتاحة: `action_create_installment_invoice` في `models/payment_schedule.py`
- العملية البرمجية المتاحة: `_cron_auto_create_invoices` في `models/payment_schedule.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
