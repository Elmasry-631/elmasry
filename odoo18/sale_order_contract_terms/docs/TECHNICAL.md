# Sales Order Contract Terms (AR/EN) - 4 Pages

- **المسار والإصدار:** `odoo18/sale_order_contract_terms` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Separate Sales Order report with bilingual contract terms (4 pages, AR/EN).

## المكونات المكتشفة

- Python: 6 file(s)
- XML: 3 file(s)

### نماذج وامتدادات Odoo

- ResPartner: model _inherit
- ResCompany: model _inherit
- SaleOrder: model _inherit
- SaleOrderContractTerms: model _inherit
- ProductTemplate: model _inherit

### الملفات المصدرية ذات الصلة

- `views/product_template_view.xml`
- `views/report_templates.xml`
- `views/report_actions.xml`
- `models/partner_company_fields.py`
- `models/__init__.py`
- `models/sale_order.py`
- `models/product_template.py`
- `security/ir.model.access.csv`

### حقول معلنة

- `x_id_no (Char)`
- `x_establishment_registration (Char)`
- `x_represented_by (Char)`
- `x_representative_id_no (Char)`
- `x_po_box (Char)`
- `technical_specification_id (Text)`
- `technical_specification_id (Text)`
- `technical_specification (Text)`

### XML IDs

- `views/product_template_view.xml::technical_specification_field`
- `views/product_template_view.xml::technical_specification_field_order_line`
- `views/report_templates.xml::contract_two_col_table`
- `views/report_templates.xml::report_saleorder_with_terms`
- `views/report_templates.xml::contract_terms_page_1`
- `views/report_templates.xml::contract_terms_page_2`
- `views/report_templates.xml::contract_terms_page_3`
- `views/report_templates.xml::contract_terms_page_4`
- `views/report_actions.xml::action_report_saleorder_with_terms`