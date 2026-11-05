# Sales Order Contract Terms (AR/EN) - 4 Pages

- **المسار والإصدار:** `odoo18/sale_order_contract_terms` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Separate Sales Order report with bilingual contract terms (4 pages, AR/EN).

## الصلاحيات والحماية المكتشفة

### ACL

- access_res_partner_contract_terms: model=base.model_res_partner, group=base.group_user, read/write/create/delete=1/1/1/0
- access_res_company_contract_terms: model=base.model_res_company, group=base.group_user, read/write/create/delete=1/1/1/0

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.