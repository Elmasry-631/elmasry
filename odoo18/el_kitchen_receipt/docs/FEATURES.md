# Kitchen Receipt from Quotation

- **المسار والإصدار:** `odoo18/el_kitchen_receipt` — Odoo 18
- **إصدار الحزمة:** `18.0.4.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Print kitchen receipt from sales quotation with customer delivery info auto-fill + pilot name sync with delivery

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Print kitchen receipt from sales quotation with customer delivery info auto-fill + pilot name sync with delivery
- نموذج Odoo: ResPartner: model _inherit
- نموذج Odoo: AccountMove: model _inherit
- نموذج Odoo: StockPicking: model _inherit
- نموذج Odoo: XPilot: model _name
- نموذج Odoo: PilotReportWizard: model _name
- نموذج Odoo: SaleOrder: model _inherit
- قائمة واجهة: الطيارين
- قائمة واجهة: تقرير الطيار

## التكوين والإضافات

الاعتماديات المعلنة: `sale`, `sale_stock`, `account`, `stock`
