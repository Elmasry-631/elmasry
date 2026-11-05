# E-Book Store

- **المسار والإصدار:** `odoo19/el_ebook_store` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Sell e-books with unique access codes — online reader + download

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Sell e-books with unique access codes — online reader + download
- نموذج Odoo: EbookCode: model _name
- نموذج Odoo: EbookAccessLog: model _name
- نموذج Odoo: SaleOrder: model _inherit
- نموذج Odoo: EbookLibrary: model _name
- نموذج Odoo: ProductTemplate: model _inherit
- نموذج Odoo: GenerateCodesWizard: model _name
- قائمة واجهة: E-Book Store
- قائمة واجهة: Access Codes
- قائمة واجهة: Customer Libraries
- قائمة واجهة: Access Logs
- نقطة HTTP: '/my/library' (auth=user)
- نقطة HTTP: '/my/ebook/<int:library_id>/read' (auth=user)
- نقطة HTTP: '/my/ebook/<int:library_id>/download' (auth=user)

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `sale`, `sale_management`, `website_sale`, `payment`, `portal`, `mail`
