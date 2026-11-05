# Construction Tendering

- **المسار والإصدار:** `odoo19/el_construction_tender` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Client Tenders (Bid Costing & Submission) + Subcontractor/Vendor RFQ & Bid Comparison

## المكونات المكتشفة

- Python: 7 file(s)
- XML: 8 file(s)
- JavaScript/TypeScript: 1 file(s)

### نماذج وامتدادات Odoo

- ConstructionTenderRfq: model _name
- ConstructionTenderRfqLine: model _name
- ConstructionTenderRfqVendor: model _name
- ConstructionTenderRfqBidLine: model _name
- ConstructionTenderOpportunity: model _name
- ConstructionTenderLine: model _name
- ConstructionTenderRfqCompareWizard: model _name

### الملفات المصدرية ذات الصلة

- `views/menu_views.xml`
- `views/tender_opportunity_views.xml`
- `views/tender_rfq_views.xml`
- `models/tender_rfq.py`
- `models/tender_opportunity.py`
- `models/__init__.py`
- `security/ir.model.access.csv`
- `security/construction_tender_security.xml`
- `wizard/tender_compare_wizard_views.xml`
- `wizard/tender_compare_wizard.py`
- `wizard/__init__.py`

### حقول معلنة

- `name (Char)`
- `company_id (Many2one)`
- `project_id (Many2one)`
- `sub_project_id (Many2one)`
- `tender_opportunity_id (Many2one)`
- `work_type_id (Many2one)`
- `scope_description (Text)`
- `submission_deadline (Datetime)`
- `state (Selection)`
- `line_ids (One2many)`
- `vendor_ids (One2many)`
- `winner_vendor_id (Many2one)`
- `subcontract_id (Many2one)`
- `lowest_amount (Float)`
- `vendor_count (Integer)`
- `rfq_id (Many2one)`
- `boq_line_id (Many2one)`
- `product_id (Many2one)`
- `description (Char)`
- `quantity (Float)`
- `uom_id (Many2one)`
- `awarded_unit_price (Float)`
- `rfq_id (Many2one)`
- `partner_id (Many2one)`
- `state (Selection)`
- `submission_date (Date)`
- `bid_line_ids (One2many)`
- `total_amount (Float)`
- `notes (Text)`
- `rfq_vendor_id (Many2one)`
- `rfq_line_id (Many2one)`
- `unit_price (Float)`
- `amount (Float)`
- `is_lowest (Boolean)`
- `remarks (Char)`
- `name (Char)`
- `title (Char)`
- `client_id (Many2one)`
- `tender_type (Selection)`
- `reference_no (Char)`
- `company_id (Many2one)`
- `user_id (Many2one)`
- `submission_deadline (Datetime)`
- `site_visit_date (Datetime)`
- `bid_bond_required (Boolean)`
- `bid_bond_amount (Float)`
- `bid_bond_expiry (Date)`
- `state (Selection)`
- `line_ids (One2many)`
- `rfq_ids (One2many)`
- `rfq_count (Integer)`
- `total_cost (Float)`
- `total_price (Float)`
- `margin_amount (Float)`
- `margin_percent (Float)`
- `lost_reason (Text)`
- `won_date (Date)`
- `project_id (Many2one)`
- `sub_project_id (Many2one)`
- `notes (Text)`
- `tender_id (Many2one)`
- `work_type_id (Many2one)`
- `work_sub_type_id (Many2one)`
- `product_id (Many2one)`
- `description (Char)`
- `quantity (Float)`
- `uom_id (Many2one)`
- `cost_source_rfq_line_id (Many2one)`
- `cost_unit_manual (Float)`
- `cost_unit (Float)`
- `overhead_percent (Float)`
- `profit_percent (Float)`
- `unit_price (Float)`
- `cost_amount (Float)`
- `amount (Float)`
- `boq_line_id (Many2one)`
- `rfq_id (Many2one)`
- `vendor_ids (One2many)`
- `comparison_html (Html)`

### XML IDs

- `reports/tender_reports.xml::report_tender_opportunity_document`
- `reports/tender_reports.xml::report_tender_opportunity`
- `reports/tender_reports.xml::action_report_tender_opportunity`
- `reports/tender_reports.xml::report_tender_rfq_document`
- `reports/tender_reports.xml::report_tender_rfq`
- `reports/tender_reports.xml::action_report_tender_rfq`
- `views/menu_views.xml::menu_construction_tendering`
- `views/menu_views.xml::menu_construction_tender_opportunity`
- `views/menu_views.xml::menu_construction_tender_rfq`
- `views/tender_opportunity_views.xml::view_construction_tender_opportunity_list`
- `views/tender_opportunity_views.xml::view_construction_tender_opportunity_form`
- `views/tender_opportunity_views.xml::action_construction_tender_opportunity`
- `views/tender_rfq_views.xml::view_construction_tender_rfq_list`
- `views/tender_rfq_views.xml::view_construction_tender_rfq_form`
- `views/tender_rfq_views.xml::action_construction_tender_rfq`
- `views/tender_rfq_views.xml::view_construction_tender_rfq_vendor_form`
- `data/sequence_data.xml::seq_construction_tender_opportunity`
- `data/sequence_data.xml::seq_construction_tender_rfq`
- `security/construction_tender_security.xml::rule_tender_opportunity_company`
- `security/construction_tender_security.xml::rule_tender_line_company`
- `security/construction_tender_security.xml::rule_tender_rfq_company`
- `security/construction_tender_security.xml::rule_tender_rfq_line_company`
- `security/construction_tender_security.xml::rule_tender_rfq_vendor_company`
- `security/construction_tender_security.xml::rule_tender_rfq_bid_line_company`
- `wizard/tender_compare_wizard_views.xml::view_construction_tender_rfq_compare_wizard_form`
- `wizard/tender_compare_wizard_views.xml::action_construction_tender_rfq_compare_wizard`