# Meta Lead Ads

- **المسار والإصدار:** `odoo19/archer_meta_lead_ads` — Odoo 19
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Import Meta lead ads into CRM leads

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Import Meta lead ads into CRM leads
- نموذج Odoo: MetaPage: model _name
- نموذج Odoo: CrmLead: model _inherit
- نموذج Odoo: MetaAppCredential: model _name
- نموذج Odoo: MetaLeadForm: model _name
- نموذج Odoo: ResConfigSettings: model _inherit
- نموذج Odoo: MetaSyncLog: model _name
- نموذج Odoo: MetaLeadFieldMapping: model _name
- قائمة واجهة: Meta Lead Ads
- قائمة واجهة: Credentials
- قائمة واجهة: Pages
- قائمة واجهة: Forms
- قائمة واجهة: Sync Issues
- نقطة HTTP: '/meta_lead_ads/oauth/callback' (auth=public, csrf=False)

## التكوين والإضافات

الاعتماديات المعلنة: `crm`, `mail`, `contacts`, `utm`
