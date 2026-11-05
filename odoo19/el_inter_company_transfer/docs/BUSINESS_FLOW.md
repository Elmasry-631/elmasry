# Inter Company Transfer

- **المسار والإصدار:** `odoo19/el_inter_company_transfer` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automate inter-company stock, sale, purchase, and accounting documents

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: InterCompany Transaction
- المستخدم يبدأ من قائمة: InterCompany Transaction
- المستخدم يبدأ من قائمة: Return InterCompany Transaction
- المستخدم يبدأ من قائمة: Inventory Breakdown
- المستخدم يبدأ من قائمة: InterCompany Rules
- النموذج/الامتداد المعني: PurchaseOrder: model _inherit
- النموذج/الامتداد المعني: ResCompany: model _inherit
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: StockPicking: model _inherit
- النموذج/الامتداد المعني: StockInterCompanyTransfer: model _name
- النموذج/الامتداد المعني: StockInterCompanyTransferLine: model _name
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- النموذج/الامتداد المعني: InterCompanyConfig: model _name
- النموذج/الامتداد المعني: ReturnInterCompanyTransfer: model _name
- النموذج/الامتداد المعني: ReturnInterCompanyTransferLine: model _name
- العملية البرمجية المتاحة: `button_confirm` في `models/purchase_order.py`
- العملية البرمجية المتاحة: `_create_inter_company_transaction` في `models/purchase_order.py`
- العملية البرمجية المتاحة: `action_view_inter_company_transfer` في `models/purchase_order.py`
- العملية البرمجية المتاحة: `action_view_inter_company_sale_order` في `models/purchase_order.py`
- العملية البرمجية المتاحة: `action_view_inter_company_transfer` في `models/account_move.py`
- العملية البرمجية المتاحة: `action_view_inter_company_transfer` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `create` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_process` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_reverse` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `create_from_sale_order` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `create_from_purchase_order` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `_create_documents_from_manual` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `_create_purchase_order_from_sale` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `_create_sale_order_from_purchase` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `_create_sale_order` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `_create_purchase_order` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `_finalize_generated_documents` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `_validate_pickings` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `_create_invoices` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `_action_open_record` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_view_sale_order` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_view_purchase_order` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_view_delivery_picking` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_view_receipt_picking` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_view_customer_invoice` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_view_vendor_bill` في `models/stock_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/sale_order.py`
- العملية البرمجية المتاحة: `_create_inter_company_transaction` في `models/sale_order.py`
- العملية البرمجية المتاحة: `action_view_inter_company_transfer` في `models/sale_order.py`
- العملية البرمجية المتاحة: `action_view_inter_company_purchase_order` في `models/sale_order.py`
- العملية البرمجية المتاحة: `_compute_display_name` في `models/inter_company_config.py`
- العملية البرمجية المتاحة: `create` في `models/return_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_process` في `models/return_inter_company_transfer.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/return_inter_company_transfer.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
