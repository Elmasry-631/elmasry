# Inter Company Transfer

- **المسار والإصدار:** `odoo19/el_inter_company_transfer` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automate inter-company stock, sale, purchase, and accounting documents

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Automate inter-company stock, sale, purchase, and accounting documents
- نموذج Odoo: PurchaseOrder: model _inherit
- نموذج Odoo: ResCompany: model _inherit
- نموذج Odoo: AccountMove: model _inherit
- نموذج Odoo: StockPicking: model _inherit
- نموذج Odoo: StockInterCompanyTransfer: model _name
- نموذج Odoo: StockInterCompanyTransferLine: model _name
- نموذج Odoo: SaleOrder: model _inherit
- نموذج Odoo: InterCompanyConfig: model _name
- نموذج Odoo: ReturnInterCompanyTransfer: model _name
- نموذج Odoo: ReturnInterCompanyTransferLine: model _name
- قائمة واجهة: InterCompany Transaction
- قائمة واجهة: InterCompany Transaction
- قائمة واجهة: Return InterCompany Transaction
- قائمة واجهة: Inventory Breakdown
- قائمة واجهة: InterCompany Rules

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `mail`, `stock`, `sale_management`, `sale_stock`, `purchase`, `purchase_stock`, `account`
