# El-Nmo - Customer Classification

- **المسار والإصدار:** `odoo19/el_nmo_classification` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Customer classification tiers (A-E) with auto-classification criteria.

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Customer classification tiers (A-E) with auto-classification criteria.
- نموذج Odoo: ResPartner: model _inherit
- نموذج Odoo: CustomerClassification: model _name
- نموذج Odoo: AccountMove: model _inherit
- نموذج Odoo: ClassificationCriteria: model _name
- نموذج Odoo: SaleOrder: model _inherit
- قائمة واجهة: Customer Classification
- قائمة واجهة: Classifications

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `mail`, `sale`, `account`, `el_nmo_sale_payment_gateway`
