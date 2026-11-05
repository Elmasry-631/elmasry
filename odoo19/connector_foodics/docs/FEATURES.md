# Foodics Connector

- **المسار والإصدار:** `odoo19/connector_foodics` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Bidirectional synchronization bridge between Odoo and Foodics POS

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Bidirectional synchronization bridge between Odoo and Foodics POS
- نموذج Odoo: ResPartner: model _inherit
- نموذج Odoo: FoodicsBaseAdapter: model _name
- نموذج Odoo: FoodicsProductAdapter: model _name
- نموذج Odoo: FoodicsCategoryAdapter: model _name
- نموذج Odoo: FoodicsCustomerAdapter: model _name
- نموذج Odoo: FoodicsOrderAdapter: model _name
- نموذج Odoo: FoodicsInventoryAdapter: model _name
- نموذج Odoo: FoodicsTaxAdapter: model _name
- نموذج Odoo: ProductCategory: model _inherit
- نموذج Odoo: ProductProduct: model _inherit
- نموذج Odoo: ProductTemplate: model _inherit
- نموذج Odoo: FoodicsMapping: model _name
- نموذج Odoo: FoodicsBranchMapping: model _name
- نموذج Odoo: FoodicsWebhookEvent: model _name
- نموذج Odoo: FoodicsWebhookLog: model _name
- نموذج Odoo: FoodicsSyncLog: model _name
- نموذج Odoo: AccountTax: model _inherit
- نموذج Odoo: FoodicsConnection: model _name
- نموذج Odoo: FoodicsApiClient: model _name
- نموذج Odoo: FoodicsTestConnectionWizard: model _name
- نموذج Odoo: FoodicsResyncWizard: model _name
- قائمة واجهة: Reports
- قائمة واجهة: Stock Reconciliation
- قائمة واجهة: Monitoring
- قائمة واجهة: Sync Logs
- قائمة واجهة: Customers
- قائمة واجهة: Dashboard
- قائمة واجهة: Webhook Events
- قائمة واجهة: Webhook Logs
- قائمة واجهة: Synchronized Data
- قائمة واجهة: Products
- قائمة واجهة: Field Mappings
- قائمة واجهة: Foodics Connector
- قائمة واجهة: Configuration
- قائمة واجهة: Connections
- قائمة واجهة: Full Resync
- نقطة HTTP: '/foodics/webhook/<string:secret>' (auth=public, csrf=False)
- نقطة HTTP: '/foodics/webhook/<string:secret>' (auth=public, csrf=False)

## التكوين والإضافات

الاعتماديات المعلنة: `account`, `contacts`, `mail`, `point_of_sale`, `product`, `sale_management`, `stock`
