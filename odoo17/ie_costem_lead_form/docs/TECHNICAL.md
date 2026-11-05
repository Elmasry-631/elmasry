# ie_costem_lead_form

- **المسار والإصدار:** `odoo17/ie_costem_lead_form` — Odoo 17
- **إصدار الحزمة:** `0.1`
- **الترخيص المعلن:** `غير محدد في manifest`
- **الملخص المعلن:** Short (1 phrase/line) summary of the module's purpose

## المكونات المكتشفة

- Python: 8 file(s)
- XML: 4 file(s)

### نماذج وامتدادات Odoo

- CheckBoxFields: model _inherit
- AssignmentUser: model _inherit
- ProjectTask: model _inherit

### الملفات المصدرية ذات الصلة

- `controllers/__init__.py`
- `controllers/controllers.py`
- `views/form_site_visit_view.xml`
- `views/check_box_fields_view.xml`
- `views/assignment_user_view.xml`
- `models/check_box_fields.py`
- `models/assignment_user.py`
- `models/__init__.py`
- `models/form_site_visit.py`
- `security/ir.model.access.csv`

### حقول معلنة

- `GetSpecifications (Selection)`
- `GetProjectLocation (Selection)`
- `SiteVisit (Selection)`
- `GetConsultantName (Selection)`
- `GetSystemSupplierName (Selection)`
- `FollowUpTechnicalOffer (Selection)`
- `FollowUpConsultantApproval (Selection)`
- `FollowUpSystemSupplierApproval (Selection)`
- `FinancialOfferFollowUp (Selection)`
- `Specifications (Many2many)`
- `notes (Text)`
- `assignment_username (Many2many)`
- `sales_eng (Char)`
- `company_reference (Char)`
- `date (Date)`
- `site_company_name (Char)`
- `site_project_name (Char)`
- `site_project_address (Char)`
- `contractor_name (Char)`
- `contractor_mobile (Char)`
- `contractor_email (Char)`
- `consultant_name (Char)`
- `consultant_email (Char)`
- `consultant_site_name (Char)`
- `consultant_site_mobile (Char)`
- `consultant_site_email (Char)`
- `supervisor_name (Char)`
- `supervisor_mobile (Char)`
- `supervisor_email (Char)`
- `fire_alarm_supplier (Char)`
- `fire_alarm_engineer (Char)`
- `fire_alarm_mobile (Char)`
- `public_address_supplier (Char)`
- `public_address_engineer (Char)`
- `public_address_mobile (Char)`
- `data_system_supplier (Char)`
- `data_system_engineer (Char)`
- `data_system_mobile (Char)`
- `access_control_supplier (Char)`
- `access_control_engineer (Char)`
- `access_control_mobile (Char)`
- `bms_supplier (Char)`
- `bms_engineer (Char)`
- `bms_mobile (Char)`
- `cctv_supplier (Char)`
- `cctv_engineer (Char)`
- `cctv_mobile (Char)`
- `matv_supplier (Char)`
- `matv_engineer (Char)`
- `matv_mobile (Char)`
- `other_supplier (Char)`
- `other_engineer (Char)`
- `other_mobile (Char)`
- `fire_alarm_note (Text)`
- `fire_alarm_requirement (Text)`
- `public_address_note (Text)`
- `public_address_requirement (Text)`
- `data_system_note (Text)`
- `data_system_requirement (Text)`
- `access_control_note (Text)`
- `access_control_requirement (Text)`
- `bms_note (Text)`
- `bms_requirement (Text)`
- `cctv_note (Text)`
- `cctv_requirement (Text)`
- `matv_note (Text)`
- `matv_requirement (Text)`
- `other_note (Text)`
- `other_requirement (Text)`
- `site_signature (Binary)`
- `company_name (Char)`
- `tax_id (Char)`
- `address (Char)`
- `telephone (Char)`
- `company_email (Char)`
- `general_manager_name (Char)`
- `general_manager_mobile (Char)`
- `general_manager_email (Char)`
- `projects_manager_name (Char)`
- `projects_manager_mobile (Char)`
- `projects_manager_email (Char)`
- `electrical_manager_name (Char)`
- `electrical_manager_mobile (Char)`
- `electrical_manager_email (Char)`
- `purchasing_manager_name (Char)`
- `purchasing_manager_mobile (Char)`
- `purchasing_manager_email (Char)`
- `financial_manager_name (Char)`
- `financial_manager_mobile (Char)`
- `financial_manager_email (Char)`
- `project_name_1 (Char)`
- `location_1 (Char)`
- `consultant_1 (Char)`
- `site_eng_1 (Char)`
- `mobile_1 (Char)`
- `specifications_1 (Text)`
- `project_name_2 (Char)`
- `location_2 (Char)`
- `consultant_2 (Char)`
- `site_eng_2 (Char)`

### XML IDs

- `views/form_site_visit_view.xml::view_task_form_tab_request_form_force`
- `views/check_box_fields_view.xml::view_check_box_form_force`
- `views/check_box_fields_view.xml::view_crm_opportunity_tree_inherit`
- `views/assignment_user_view.xml::assignment_username_view_form`