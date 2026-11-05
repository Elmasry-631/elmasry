# Warehouse-Based Access Control

- **المسار والإصدار:** `odoo18/el_warehouse_access` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Control user access based on warehouse assignments - Global backend security enforcement

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Control user access based on warehouse assignments - Global backend security enforcement
- نموذج Odoo: ResUsers: model _inherit
- نموذج Odoo: StockScrap: model _inherit
- نموذج Odoo: StockMove: model _inherit
- نموذج Odoo: StockQuant: model _inherit
- نموذج Odoo: StockLocation: model _inherit
- نموذج Odoo: StockPickingType: model _inherit
- نموذج Odoo: SaleOrder: model _inherit
- نموذج Odoo: StockPicking: model _inherit
- قائمة واجهة: Warehouse Access Control
- قائمة واجهة: User Warehouse Assignments
- قائمة واجهة: Warehouse Access Matrix

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `stock`, `sale_stock`
