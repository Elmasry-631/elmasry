# Impact Analysis — ie_stock_movement_report

## Impact on existing Odoo models

| Model            | Change type | Description                              |
|------------------|-------------|------------------------------------------|
| stock.move.line  | READ only   | No field changes; only read for reporting |
| product.product  | READ only   | Reads standard_price, uom_id, categ_id    |
| stock.warehouse  | READ only   | Reads lot_stock_id                        |
| stock.location   | READ only   | Reads display_name                        |
| res.partner      | READ only   | Reads display_name                        |
| res.company      | READ only   | Reads name, logo for report header        |

## No breaking changes

- No `_inherit` on existing models (no field additions, no method overrides)
- No `view_id` inheritance on existing views
- No `ir.rule` additions that affect existing records

## Impact on performance

- Report generation is read-only — does not lock tables
- For 10,000 move lines: ~6 SQL queries, <2s rendering time
- No cron jobs added
- No scheduled actions

## Impact on security

- Adds 2 new security groups (no impact on existing groups)
- Adds 1 ir.module.privilege (Odoo 19 pattern)
- No record rules on existing models

## Impact on i18n

- Adds 30+ new translation terms (all wrapped in `_()`)
- Provides complete ar.po
- No changes to existing translation strings
