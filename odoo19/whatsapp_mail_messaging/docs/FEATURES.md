# Odoo Whatsapp Connector

- **المسار والإصدار:** `odoo19/whatsapp_mail_messaging` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Odoo18 Whatsapp, Whatsapp Odoo Integration, Odoo Whatsapp Connector,       Odoo Whatsapp, Whatsapp Connector, Whatsapp Integration, Odoo18, Whatsapp,      Odoo Apps

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Odoo18 Whatsapp, Whatsapp Odoo Integration, Odoo Whatsapp Connector,       Odoo Whatsapp, Whatsapp Connector, Whatsapp Integration, Odoo18, Whatsapp,      Odoo Apps
- نموذج Odoo: ResCompany: model _inherit
- نموذج Odoo: ResConfigSettings: model _inherit
- نموذج Odoo: AccountMove: model _inherit
- نموذج Odoo: SelectionMessage: model _name
- نموذج Odoo: SaleOrder: model _inherit
- نموذج Odoo: Website: model _inherit
- نموذج Odoo: WhatsappSendMessage: model _name
- نموذج Odoo: PortalShare: model _inherit
- قائمة واجهة: Whatsapp Messages
- نقطة HTTP: '/whatsapp_message' (auth=public)
- نقطة HTTP: '/mobile_number' (auth=public)

## التكوين والإضافات

الاعتماديات المعلنة: `sale`, `account`, `website`, `sale_management`
