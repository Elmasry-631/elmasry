# Advanced Accounting Reports

- **المسار والإصدار:** `odoo19/advanced_accounting_reports` — Odoo 19
- **إصدار الحزمة:** `1.20.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Advanced General Ledger, Trial Balance with Analytic Dimensions & Multi-Currency

## الصلاحيات والحماية المكتشفة

### ACL

- access_account_feature_readonly: model=model_account_feature, group=account.group_account_readonly, read/write/create/delete=1/0/0/0
- access_account_feature_user: model=model_account_feature, group=account.group_account_user, read/write/create/delete=1/1/1/0
- access_account_feature_manager: model=model_account_feature, group=account.group_account_manager, read/write/create/delete=1/1/1/1
- access_account_cost_center_readonly: model=model_account_cost_center, group=account.group_account_readonly, read/write/create/delete=1/0/0/0
- access_account_cost_center_user: model=model_account_cost_center, group=account.group_account_user, read/write/create/delete=1/1/1/0
- access_account_cost_center_manager: model=model_account_cost_center, group=account.group_account_manager, read/write/create/delete=1/1/1/1
- access_account_patch_number_readonly: model=model_account_patch_number, group=account.group_account_readonly, read/write/create/delete=1/0/0/0
- access_account_patch_number_user: model=model_account_patch_number, group=account.group_account_user, read/write/create/delete=1/1/1/0
- access_account_patch_number_manager: model=model_account_patch_number, group=account.group_account_manager, read/write/create/delete=1/1/1/1
- access_general_ledger_wizard_user: model=model_general_ledger_wizard, group=account.group_account_user, read/write/create/delete=1/1/1/0
- access_general_ledger_wizard_manager: model=model_general_ledger_wizard, group=account.group_account_manager, read/write/create/delete=1/1/1/1
- access_trial_balance_wizard_user: model=model_trial_balance_wizard, group=account.group_account_user, read/write/create/delete=1/1/1/0
- access_trial_balance_wizard_manager: model=model_trial_balance_wizard, group=account.group_account_manager, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: `rule_account_feature_multi_company`, `rule_account_cost_center_multi_company`, `rule_account_patch_number_multi_company`

### واجهات HTTP ورفع الصلاحيات

- '/advanced_accounting/reports/general_ledger' (auth=user)
- '/advanced_accounting/export/general_ledger_xlsx' (auth=user)
- '/advanced_accounting/export/trial_balance_xlsx' (auth=user)

مواضع `sudo()` المرصودة:

- `report/trial_balance_report.py`
- `report/general_ledger_report.py`
- `controllers/xlsx_export.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.