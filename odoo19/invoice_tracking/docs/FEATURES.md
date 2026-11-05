# Invoice Tracking

- **المسار والإصدار:** `odoo19/invoice_tracking` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Brief description of the module

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Brief description of the module
- نموذج Odoo: ResCompany: model _inherit
- نموذج Odoo: InvoiceTracking: model _name
- نموذج Odoo: PartnerCode: model _name
- نموذج Odoo: ResPartner: model _inherit
- نموذج Odoo: PurchaseOrder: model _inherit
- نموذج Odoo: ResConfigSettings: model _inherit
- نموذج Odoo: AccountMove: model _inherit
- نموذج Odoo: Well: model _name
- نموذج Odoo: CheckTracking: model _name
- قائمة واجهة: Invoice Tracking
- قائمة واجهة: Vendor Code
- قائمة واجهة: Well Number
- قائمة واجهة: Checks
- نقطة HTTP: '/public/partner/image/<int:partner_id>' (auth=public)

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `mail`, `account`, `purchase`
