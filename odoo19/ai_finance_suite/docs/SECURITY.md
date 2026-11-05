# AI Finance

- **المسار والإصدار:** `odoo19/ai_finance_suite` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** AI-Powered Finance Suite: Virtual CFO, OCR Engine & Smart Reconciliation for Odoo 19

## الصلاحيات والحماية المكتشفة

### ACL

- access_af_virtual_cfo_agent: model=model_af_virtual_cfo_agent, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_cfo_conversation: model=model_af_cfo_conversation, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_vendor_bill_wizard: model=model_af_vendor_bill_wizard, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_cfo_query_wizard: model=model_af_cfo_query_wizard, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_vendor_bill_wizard_line: model=model_af_vendor_bill_wizard_line, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_credential_user: model=model_af_credential, group=account.group_account_manager, read/write/create/delete=1/1/1/1
- access_af_credential_admin: model=model_af_credential, group=base.group_system, read/write/create/delete=1/1/1/1
- access_af_refund_tracking: model=model_af_refund_tracking, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_vendor_statement: model=model_af_vendor_statement, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_vendor_statement_line: model=model_af_vendor_statement_line, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_bank_statement: model=model_af_bank_statement, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_bank_statement_line: model=model_af_bank_statement_line, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_vendor_bill_wizard_column: model=model_af_vendor_bill_wizard_column, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_vendor_statement_column: model=model_af_vendor_statement_column, group=base.group_user, read/write/create/delete=1/1/1/1
- access_af_finance_dashboard: model=model_af_finance_dashboard, group=base.group_user, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/ai_config.py`
- `models/virtual_cfo_agent.py`
- `wizards/vendor_bill_wizard.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.