# Vehicle Installment Management

- **المسار والإصدار:** `odoo19/vehicle_installment` — Odoo 19
- **إصدار الحزمة:** `19.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Manage vehicle installments with automatic calculation

## المكونات المكتشفة

- Python: 6 file(s)
- XML: 2 file(s)

### نماذج وامتدادات Odoo

- HrPayslip: model _inherit
- VehicleInstallmentLine: model _name
- VehicleInstallment: model _name

### الملفات المصدرية ذات الصلة

- `views/vehicle_installment_views.xml`
- `models/hr_payslip.py`
- `models/vehicle_installment_line.py`
- `models/vehicle_installment.py`
- `models/__init__.py`
- `security/security.xml`
- `security/ir.model.access.csv`

### حقول معلنة

- `installment_id (Many2one)`
- `vehicle_id (Many2one)`
- `employee_id (Many2one)`
- `payment_date (Date)`
- `amount (Monetary)`
- `state (Selection)`
- `installment_state (Selection)`
- `company_id (Many2one)`
- `currency_id (Many2one)`
- `note (Html)`
- `vehicle_id (Many2one)`
- `employee_id (Many2one)`
- `date (Date)`
- `vehicle_price (Monetary)`
- `rate_percentage (Float)`
- `monthly_payment (Monetary)`
- `total_amount (Monetary)`
- `calculated_months (Float)`
- `full_months (Integer)`
- `last_payment_amount (Monetary)`
- `installment_lines (One2many)`
- `reason (Text)`
- `company_id (Many2one)`
- `state (Selection)`
- `currency_id (Many2one)`

### XML IDs

- `views/vehicle_installment_views.xml::vehicle_installment_form_view`
- `views/vehicle_installment_views.xml::vehicle_installment_list_view`
- `views/vehicle_installment_views.xml::vehicle_installment_view_search`
- `views/vehicle_installment_views.xml::vehicle_installment_action_window`
- `views/vehicle_installment_views.xml::vehicle_installment_line_list_view`
- `views/vehicle_installment_views.xml::vehicle_installment_line_action_window`
- `views/vehicle_installment_views.xml::menu_vehicle_installment_root`
- `views/vehicle_installment_views.xml::menu_vehicle_installment_main`
- `views/vehicle_installment_views.xml::menu_vehicle_installment_lines`
- `security/security.xml::vehicle_installment.module_category_vehicle_installment`
- `security/security.xml::res_groups_privilege_vehicle_installment`
- `security/security.xml::group_vehicle_installment_user`
- `security/security.xml::group_vehicle_installment_manager`
- `security/security.xml::vehicle_installment_rule`
- `security/security.xml::vehicle_installment_see_own_company`
- `security/security.xml::vehicle_installment_line_see_own_company`