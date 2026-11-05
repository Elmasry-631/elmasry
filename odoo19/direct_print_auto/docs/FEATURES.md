# Direct Print Auto

- **المسار والإصدار:** `odoo19/direct_print_auto` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Auto-print invoices, SOs, delivery slips and POs to the browser's print dialog when confirmed, plus a manual Direct Print button on each form.

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Auto-print invoices, SOs, delivery slips and POs to the browser's print dialog when confirmed, plus a manual Direct Print button on each form.
- نموذج Odoo: PurchaseOrder: model _name
- نموذج Odoo: ResConfigSettings: model _inherit
- نموذج Odoo: AccountMove: model _name
- نموذج Odoo: StockPicking: model _name
- نموذج Odoo: SaleOrder: model _name
- نموذج Odoo: DirectPrintMixin: model _name

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `web`, `sale_management`, `account`, `stock`, `purchase`
