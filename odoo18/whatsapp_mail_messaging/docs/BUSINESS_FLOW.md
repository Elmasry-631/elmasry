# Odoo Whatsapp Connector

- **المسار والإصدار:** `odoo18/whatsapp_mail_messaging` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Odoo18 Whatsapp, Whatsapp Odoo Integration, Odoo Whatsapp Connector,       Odoo Whatsapp, Whatsapp Connector, Whatsapp Integration, Odoo18, Whatsapp,      Odoo Apps

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Whatsapp Messages
- النموذج/الامتداد المعني: ResCompany: model _inherit
- النموذج/الامتداد المعني: ResConfigSettings: model _inherit
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: SelectionMessage: model _name
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- النموذج/الامتداد المعني: Website: model _inherit
- النموذج/الامتداد المعني: WhatsappSendMessage: model _name
- النموذج/الامتداد المعني: PortalShare: model _inherit
- العملية البرمجية المتاحة: `action_send_whatsapp` في `model/account_move.py`
- العملية البرمجية المتاحة: `action_whatsapp_multi` في `model/account_move.py`
- العملية البرمجية المتاحة: `action_send_whatsapp` في `model/sale_order.py`
- العملية البرمجية المتاحة: `action_whatsapp_multi` في `model/sale_order.py`
- العملية البرمجية المتاحة: `action_send_whatsapp` في `wizard/portal_share.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
