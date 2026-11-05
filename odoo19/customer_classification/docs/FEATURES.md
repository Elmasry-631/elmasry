# Customer Classification & Credit Control

- **المسار والإصدار:** `odoo19/customer_classification` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Classify customers into tiers (A-E) with inherited price lists, credit limits, and payment terms.

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Classify customers into tiers (A-E) with inherited price lists, credit limits, and payment terms.
- نموذج Odoo: ResPartner: model _inherit
- نموذج Odoo: CustomerClassification: model _name
- نموذج Odoo: AccountMove: model _inherit
- نموذج Odoo: ClassificationCriteria: model _name
- نموذج Odoo: SaleOrder: model _inherit
- قائمة واجهة: Customer Classification
- قائمة واجهة: Classifications

## التكوين والإضافات

الاعتماديات المعلنة: `sale`, `account`
