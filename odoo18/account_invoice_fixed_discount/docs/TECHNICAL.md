# Account Fixed Discount

- **المسار والإصدار:** `odoo18/account_invoice_fixed_discount` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Allows to apply fixed amount discounts in invoices.

## المكونات المكتشفة

- Python: 7 file(s)
- XML: 3 file(s)

### نماذج وامتدادات Odoo

- AccountMoveLine: model _inherit
- AccountTax: model _inherit

### الملفات المصدرية ذات الصلة

- `views/account_move_view.xml`
- `models/__init__.py`
- `models/account_move_line.py`
- `models/account_tax.py`
- `security/res_groups.xml`

### حقول معلنة

- `discount_fixed (Monetary)`

### XML IDs

- `reports/report_account_invoice.xml::report_invoice_document`
- `views/account_move_view.xml::view_move_form`
- `security/res_groups.xml::group_fixed_discount`
- `security/res_groups.xml::account.group_account_invoice`