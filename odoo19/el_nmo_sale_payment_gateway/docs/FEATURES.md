# Sale Payment Gateway

- **المسار والإصدار:** `odoo19/el_nmo_sale_payment_gateway` — Odoo 19
- **إصدار الحزمة:** `19.0.1.2.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Payment Gateway on Sales/Invoice/Delivery + auto-sync Receivable & Payable accounts from gateway to partner

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Payment Gateway on Sales/Invoice/Delivery + auto-sync Receivable & Payable accounts from gateway to partner
- نموذج Odoo: ResPartner: model _inherit
- نموذج Odoo: AccountMove: model _inherit
- نموذج Odoo: StockPicking: model _inherit
- نموذج Odoo: StockMove: model _inherit
- نموذج Odoo: SalePaymentGateway: model _name
- نموذج Odoo: SaleOrder: model _inherit
- قائمة واجهة: Payment Gateways

## التكوين والإضافات

الاعتماديات المعلنة: `sale_management`, `account`, `stock`, `delivery`
