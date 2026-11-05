# Sale Payment Gateway

- **المسار والإصدار:** `odoo19/el_nmo_sale_payment_gateway` — Odoo 19
- **إصدار الحزمة:** `19.0.1.2.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Payment Gateway on Sales/Invoice/Delivery + auto-sync Receivable & Payable accounts from gateway to partner

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Payment Gateways
- النموذج/الامتداد المعني: ResPartner: model _inherit
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: StockPicking: model _inherit
- النموذج/الامتداد المعني: StockMove: model _inherit
- النموذج/الامتداد المعني: SalePaymentGateway: model _name
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- العملية البرمجية المتاحة: `create` في `models/res_partner.py`
- العملية البرمجية المتاحة: `_sync_gateway_accounts` في `models/res_partner.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
