# Invoice Tracking

- **المسار والإصدار:** `odoo19/invoice_tracking` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Brief description of the module

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Invoice Tracking
- المستخدم يبدأ من قائمة: Vendor Code
- المستخدم يبدأ من قائمة: Well Number
- المستخدم يبدأ من قائمة: Checks
- النموذج/الامتداد المعني: ResCompany: model _inherit
- النموذج/الامتداد المعني: InvoiceTracking: model _name
- النموذج/الامتداد المعني: PartnerCode: model _name
- النموذج/الامتداد المعني: ResPartner: model _inherit
- النموذج/الامتداد المعني: PurchaseOrder: model _inherit
- النموذج/الامتداد المعني: ResConfigSettings: model _inherit
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: Well: model _name
- النموذج/الامتداد المعني: CheckTracking: model _name
- العملية البرمجية المتاحة: `_compute_purchase_lines` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `_compute_rate_today` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `_compute_total_invoice_amount_egp` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `_compute_total_invoice_amount_usd` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `create` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `action_receive` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `action_del_to_administration` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `action_rec_from_administration` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `action_reset_to_draft` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `action_create_bill_from_invoice_tracking` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `action_view_purchase_order` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `action_view_vendor_bill` في `models/invoice_tracking.py`
- العملية البرمجية المتاحة: `action_create_invoice_tracking` في `models/purshase_order.py`
- العملية البرمجية المتاحة: `_compute_tracking_count` في `models/purshase_order.py`
- العملية البرمجية المتاحة: `action_view_invoice_tracking` في `models/purshase_order.py`
- العملية البرمجية المتاحة: `_compute_move_count` في `models/check_tracking.py`
- العملية البرمجية المتاحة: `_compute_secondary_amount` في `models/check_tracking.py`
- العملية البرمجية المتاحة: `_create_stage_entry` في `models/check_tracking.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/check_tracking.py`
- العملية البرمجية المتاحة: `action_deposit` في `models/check_tracking.py`
- العملية البرمجية المتاحة: `action_clear` في `models/check_tracking.py`
- العملية البرمجية المتاحة: `action_bounce` في `models/check_tracking.py`
- العملية البرمجية المتاحة: `action_issue` في `models/check_tracking.py`
- العملية البرمجية المتاحة: `action_cash` في `models/check_tracking.py`
- العملية البرمجية المتاحة: `action_view_entries` في `models/check_tracking.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
