# Archer Meta Lead Ads

Odoo CRM technical module for importing Meta Lead Ads submissions into `crm.lead`.

## Included

- Meta app credentials per company
- OAuth callback controller
- Meta pages and lead forms
- Form field mappings to `crm.lead`
- Incremental lead fetch and deduplication by Meta `leadgen_id`
- Sync issue logging
- CRM settings integration and scheduled jobs

## Source Inputs

This module was scaffolded from:

- `custom_addons/DESIGN.md`
- `custom_addons/META_API.md`
- `custom_addons/icon.jpeg`

## Notes

- Graph API version is fixed to `v19.0`
- The module is technical: no top-level desktop app icon
- UI lives under `CRM -> Configuration -> Meta Lead Ads`
