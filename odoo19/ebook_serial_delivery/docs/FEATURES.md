# eBook Serial Delivery

- **المسار والإصدار:** `odoo19/ebook_serial_delivery` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Deliver eBook licenses using standard Inventory Serial Numbers (stock.lot) — no custom "activation code" model.

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Deliver eBook licenses using standard Inventory Serial Numbers (stock.lot) — no custom "activation code" model.
- نموذج Odoo: ResCompany: model _inherit
- نموذج Odoo: ResConfigSettings: model _inherit
- نموذج Odoo: StockPicking: model _inherit
- نموذج Odoo: StockMove: model _inherit
- نموذج Odoo: SaleOrder: model _inherit
- نموذج Odoo: ProductTemplate: model _inherit
- نموذج Odoo: StockPickingJawalySms: model _name

## التكوين والإضافات

الاعتماديات المعلنة: `website_sale`, `sale_stock`, `mail`
