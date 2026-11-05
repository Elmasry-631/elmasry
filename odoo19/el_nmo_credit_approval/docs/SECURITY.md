# El-Nmo - Credit Limit Approval Workflow

- **المسار والإصدار:** `odoo19/el_nmo_credit_approval` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Approval workflow for sale orders exceeding customer credit limits.

## الصلاحيات والحماية المكتشفة

### ACL

- access_credit_rejection_reason_manager: model=model_credit_rejection_reason, group=el_nmo_credit_approval.group_credit_approval_manager, read/write/create/delete=1/1/1/1
- access_credit_rejection_reason_supervisor: model=model_credit_rejection_reason, group=el_nmo_credit_approval.group_credit_approval_supervisor, read/write/create/delete=1/0/0/0
- access_credit_rejection_reason_salesperson: model=model_credit_rejection_reason, group=el_nmo_credit_approval.group_credit_approval_salesperson, read/write/create/delete=1/0/0/0
- access_credit_approval_request_manager: model=model_credit_approval_request, group=el_nmo_credit_approval.group_credit_approval_manager, read/write/create/delete=1/1/1/1
- access_credit_approval_request_supervisor: model=model_credit_approval_request, group=el_nmo_credit_approval.group_credit_approval_supervisor, read/write/create/delete=1/1/0/0
- access_credit_approval_request_salesperson: model=model_credit_approval_request, group=el_nmo_credit_approval.group_credit_approval_salesperson, read/write/create/delete=1/0/1/0
- access_credit_approval_wizard_manager: model=model_credit_approval_wizard, group=el_nmo_credit_approval.group_credit_approval_manager, read/write/create/delete=1/1/1/1
- access_credit_approval_wizard_supervisor: model=model_credit_approval_wizard, group=el_nmo_credit_approval.group_credit_approval_supervisor, read/write/create/delete=1/1/1/1
- access_credit_approval_wizard_salesperson: model=model_credit_approval_wizard, group=el_nmo_credit_approval.group_credit_approval_salesperson, read/write/create/delete=1/0/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_credit_approval_salesperson`, `group_credit_approval_supervisor`, `group_credit_approval_manager`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/credit_approval_request.py`
- `models/sale_order.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.