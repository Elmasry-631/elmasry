# Inter Company Internal Transfer

- **المسار والإصدار:** `odoo20/el_inter_company_transfer` — Odoo 20
- **إصدار الحزمة:** `20.0.1.0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Request stock transfers between warehouses of different companies

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Inter Company Transfers
- المستخدم يبدأ من قائمة: Transfer Requests
- النموذج/الامتداد المعني: StockWarehouse: model _inherit
- النموذج/الامتداد المعني: InterCompanyTransferRequest: model _name
- النموذج/الامتداد المعني: InterCompanyTransferRequestLine: model _name
- العملية البرمجية المتاحة: `_compute_is_draft` في `models/transfer_request.py`
- العملية البرمجية المتاحة: `_compute_can_confirm` في `models/transfer_request.py`
- العملية البرمجية المتاحة: `create` في `models/transfer_request.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/transfer_request.py`
- العملية البرمجية المتاحة: `_create_outgoing_picking` في `models/transfer_request.py`
- العملية البرمجية المتاحة: `_create_incoming_picking` في `models/transfer_request.py`
- العملية البرمجية المتاحة: `action_done` في `models/transfer_request.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/transfer_request.py`
- العملية البرمجية المتاحة: `action_reset_to_draft` في `models/transfer_request.py`
- العملية البرمجية المتاحة: `action_view_picking` في `models/transfer_request.py`
- العملية البرمجية المتاحة: `action_view_incoming_picking` في `models/transfer_request.py`
- العملية البرمجية المتاحة: `_compute_available_qty` في `models/transfer_request_line.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
