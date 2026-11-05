# Restrict Journal for Users (Whitelist)

- **المسار والإصدار:** `odoo18/el_restrict_journal` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Per-user journal whitelist — only allowed journals are visible

## المكونات المكتشفة

- Python: 9 file(s)
- XML: 4 file(s)

### نماذج وامتدادات Odoo

- AccountJournal: model _inherit
- AccountMove: model _inherit
- ResUsers: model _inherit
- AccountPayment: model _inherit

### الملفات المصدرية ذات الصلة

- `views/res_users_views.xml`
- `views/account_move_views.xml`
- `models/account_journal.py`
- `models/account_move.py`
- `models/__init__.py`
- `models/res_users.py`
- `models/account_payment.py`
- `security/ir.model.access.csv`
- `security/account_restrict_journal_rules.xml`
- `security/account_restrict_journal_groups.xml`

### حقول معلنة

- `allowed_user_count (Integer)`
- `allowed_journal_ids (Many2many)`

### XML IDs

- `views/res_users_views.xml::view_users_form_restrict_journal`
- `views/account_move_views.xml::view_account_move_form_restrict_journal`
- `security/account_restrict_journal_rules.xml::rule_journal_allowed_only`
- `security/account_restrict_journal_rules.xml::rule_move_allowed_only`
- `security/account_restrict_journal_rules.xml::rule_payment_allowed_only`
- `security/account_restrict_journal_groups.xml::module_category_restrict_journal`
- `security/account_restrict_journal_groups.xml::group_restrict_journal_user`
- `security/account_restrict_journal_groups.xml::group_restrict_journal_manager`