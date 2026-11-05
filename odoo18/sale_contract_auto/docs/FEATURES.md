# Sale Contract Auto

- **المسار والإصدار:** `odoo18/sale_contract_auto` — Odoo 18
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automatically generate contracts from sale orders

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Automatically generate contracts from sale orders
- نموذج Odoo: ContractDocument: model _name
- نموذج Odoo: SaleContract: model _name
- نموذج Odoo: AccountMove: model _inherit
- نموذج Odoo: ContractTitle: model _name
- نموذج Odoo: ContractAmendment: model _name
- نموذج Odoo: ContractTemplate: model _name
- نموذج Odoo: SaleOrder: model _inherit
- نموذج Odoo: ResPartner: model _inherit
- نموذج Odoo: SaleContractLine: model _name
- نموذج Odoo: ContractClause: model _name
- نموذج Odoo: ContractPaymentSchedule: model _name
- قائمة واجهة: Contract Templates
- قائمة واجهة: Contracts
- قائمة واجهة: Contracts
- قائمة واجهة: Contract Titles
- قائمة واجهة: Customers
- نقطة HTTP: ['/my/contracts/<int:contract_id>'] (auth=user)
- نقطة HTTP: ['/my/contracts/<int:contract_id>/sign'] (auth=user)

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `sale_management`, `account`, `portal`, `mail`
