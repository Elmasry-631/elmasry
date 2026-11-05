# AI Finance V1

- **المسار والإصدار:** `odoo19/test_AI_finance` — Odoo 19
- **إصدار الحزمة:** `1.8`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Advanced AI Finance Module: Virtual CFO & OCR Engine

## الصلاحيات والحماية المكتشفة

### ACL

- access_test_ai_virtual_cfo_agent: model=model_test_ai_virtual_cfo_agent, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_cfo_conversation: model=model_test_ai_cfo_conversation, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_vendor_bill_wizard: model=model_test_ai_vendor_bill_wizard, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_cfo_query_wizard: model=model_test_ai_cfo_query_wizard, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_vendor_bill_wizard_line: model=model_test_ai_vendor_bill_wizard_line, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_credential: model=model_test_ai_credential, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_refund_tracking: model=model_test_ai_refund_tracking, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_vendor_statement: model=model_test_ai_vendor_statement, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_vendor_statement_line: model=model_test_ai_vendor_statement_line, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_bank_statement: model=model_test_ai_bank_statement, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_bank_statement_line: model=model_test_ai_bank_statement_line, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_vendor_bill_wizard_column: model=model_test_ai_vendor_bill_wizard_column, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_vendor_statement_column: model=model_test_ai_vendor_statement_column, group=base.group_user, read/write/create/delete=1/1/1/1
- access_test_ai_finance_dashboard: model=model_test_ai_finance_dashboard, group=base.group_user, read/write/create/delete=1/1/1/1

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