# Invoice From Stock Picking

- **المسار والإصدار:** `odoo18/stock_move_invoice` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Create invoice for stock picking

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: Settings: model _inherit
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: StockPicking: model _inherit
- النموذج/الامتداد المعني: StockReturnInvoicePicking: model _inherit
- النموذج/الامتداد المعني: PickingInvoice: model _name
- العملية البرمجية المتاحة: `_compute_invoice_count` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `action_create_invoice` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `action_create_bill` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `action_create_customer_credit` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `action_create_vendor_credit` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `action_open_picking_invoice` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `action_create_multi_invoice_for_multi_transfer` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `_create_returns` في `models/stock_return_picking.py`
- العملية البرمجية المتاحة: `action_picking_multi_invoice` في `wizard/picking_invoice.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
