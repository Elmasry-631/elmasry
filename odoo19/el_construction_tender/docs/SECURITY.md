# Construction Tendering

- **المسار والإصدار:** `odoo19/el_construction_tender` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Client Tenders (Bid Costing & Submission) + Subcontractor/Vendor RFQ & Bid Comparison

## الصلاحيات والحماية المكتشفة

### ACL

- access_construction_tender_opportunity_user: model=model_el_construction_tender_opportunity, group=el_construction_management.group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_tender_opportunity_manager: model=model_el_construction_tender_opportunity, group=el_construction_management.group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_tender_line_user: model=model_el_construction_tender_line, group=el_construction_management.group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_tender_line_manager: model=model_el_construction_tender_line, group=el_construction_management.group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_tender_rfq_user: model=model_el_construction_tender_rfq, group=el_construction_management.group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_tender_rfq_manager: model=model_el_construction_tender_rfq, group=el_construction_management.group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_tender_rfq_line_user: model=model_el_construction_tender_rfq_line, group=el_construction_management.group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_tender_rfq_line_manager: model=model_el_construction_tender_rfq_line, group=el_construction_management.group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_tender_rfq_vendor_user: model=model_el_construction_tender_rfq_vendor, group=el_construction_management.group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_tender_rfq_vendor_manager: model=model_el_construction_tender_rfq_vendor, group=el_construction_management.group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_tender_rfq_bid_line_user: model=model_el_construction_tender_rfq_bid_line, group=el_construction_management.group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_tender_rfq_bid_line_manager: model=model_el_construction_tender_rfq_bid_line, group=el_construction_management.group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_tender_rfq_compare_wizard: model=model_el_construction_tender_rfq_compare_wizard, group=el_construction_management.group_construction_user, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: `rule_tender_opportunity_company`, `rule_tender_line_company`, `rule_tender_rfq_company`, `rule_tender_rfq_line_company`, `rule_tender_rfq_vendor_company`, `rule_tender_rfq_bid_line_company`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/tender_opportunity.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.