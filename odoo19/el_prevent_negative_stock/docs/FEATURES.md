# Prevent Negative Stock

- **المسار والإصدار:** `odoo19/el_prevent_negative_stock` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Prevent negative stock — block stock moves AND sales orders when stock is insufficient

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Prevent negative stock — block stock moves AND sales orders when stock is insufficient
- نموذج Odoo: ElStockAlert: model _name
- نموذج Odoo: StockMove: model _inherit
- نموذج Odoo: SaleOrder: model _inherit
- قائمة واجهة: Negative Stock Alerts
- قائمة واجهة: All Alerts

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `stock`, `mail`, `sale_management`, `nmo_sale_order_approval_workflow`, `nmo_stock_user_restriction`
