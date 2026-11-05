# Purchase Actual Quantity

- **المسار والإصدار:** `odoo18/el_purchase_actual_qty` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Actual purchase quantity with preserved value, dashboard and reporting

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Actual purchase quantity with preserved value, dashboard and reporting
- نموذج Odoo: ResConfigSettings: model _inherit
- نموذج Odoo: PurchaseActualReport: model _name
- نموذج Odoo: PurchaseOrderLine: model _inherit
- قائمة واجهة: Actual Quantity Dashboard
- قائمة واجهة: Actual Quantity Analysis
- نقطة HTTP: '/purchase_actual_qty/export/csv' (auth=user)

## التكوين والإضافات

الاعتماديات المعلنة: `purchase`, `purchase_stock`, `stock_account`
