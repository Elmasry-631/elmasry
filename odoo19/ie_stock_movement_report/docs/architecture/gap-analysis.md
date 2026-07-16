# GAP Analysis — ie_stock_movement_report

## Requirement → Standard Module Mapping

| # | Requirement                          | Standard Module | Coverage      | Custom Work Needed? |
|---|--------------------------------------|-----------------|---------------|---------------------|
| 1 | Inventory movement report            | `stock`         | ⚠ Basic       | ✅ YES — stock.report.stock.history exists but lacks opening/running balance + per-product pages |
| 2 | Opening balance before period        | None            | ❌ None        | ✅ YES — must compute from stock.move.line |
| 3 | Running balance after each movement  | None            | ❌ None        | ✅ YES — in-memory computation |
| 4 | Per-product pages in PDF             | `web` (QWeb)    | ⚠ Framework only | ✅ YES — custom QWeb template |
| 5 | IN/OUT/BALANCE × Qty/Unit/Price/Total| None            | ❌ None        | ✅ YES — custom table layout |
| 6 | A4 Landscape orientation             | `web`           | ✅ Full       | ❌ NO — paperformat config |
| 7 | Multi-language (EN/AR + RTL)         | `base`          | ✅ Full       | ❌ NO — use _() + ar.po |
| 8 | Date range filter                    | None            | ❌ None        | ✅ YES — custom wizard |
| 9 | Warehouse/location/product filter    | None            | ❌ None        | ✅ YES — wizard + domain builder |
| 10| Performance for thousands of moves   | None            | ❌ None        | ✅ YES — batch fetch + in-memory |

## Build Scope (Custom Work)

Based on GAP analysis, the actual custom build scope is:

1. **Models to build:**
   - `stock.movement.report` (AbstractModel — business logic)
   - `stock.movement.report.wizard` (TransientModel — filters)
   - `report.stock.movement.report` (AbstractModel — QWeb handler)
2. **Models to extend:** None
3. **Standard modules to depend on:** base, stock, stock_account, web
4. **Configuration-only (no code):** paperformat A4 Landscape

## Why not use stock.report.stock.history?

Odoo ships `stock.report.stock.history` (the "Inventory at Date" report) but:
- It shows snapshot at ONE date, not a period
- No opening/closing/running balance
- No per-product page layout
- No IN/OUT/BALANCE breakdown with unit price
- No multi-language RTL support out of the box

Hence custom build is justified.

## Dependency Decision

| Module          | Action  | Reason                                          |
|-----------------|---------|-------------------------------------------------|
| `base`          | depend  | Required for all modules                        |
| `stock`         | depend  | Source data (stock.move.line, stock.location)   |
| `stock_account` | depend  | Product cost (standard_price) + valuation       |
| `web`           | depend  | QWeb report infrastructure                      |
| `stock_account_pond` | ❌ NOT depend | Enterprise-only (FIFO/LIFO) — breaks CE    |

## Estimated Effort Reduction

- Requirements that standard Odoo covers: 2/10 (paper format, i18n framework)
- Effort saved: ~20% (no need to rebuild QWeb infra or i18n)
- Actual custom scope: 3 models + 1 wizard view + 1 QWeb template + 1 paperformat + security
