# Purchase Actual Quantity V2 — Odoo 18 Community

## Business rule
Example: Ordered 100 KG at 50 = 5,000. Actual physical quantity is 90 KG. The receipt quantity becomes 90 KG, while the total commercial/inventory value remains 5,000 by redistributing the unit cost to 55.555556.

## V2 features
- Actual Quantity on purchase lines.
- Effective Unit Cost.
- Quantity variance and variance percentage.
- Native Graph, Pivot, List and Search analysis.
- OWL dashboard with KPI cards.
- Dashboard periods: All, Month, Quarter, Year.
- Top vendors and products by variance.
- Native drill-down through the Analysis action.
- QWeb PDF report for selected analysis rows.
- CSV export compatible with Excel.
- Multi-company reporting scoped to allowed companies.
- Configurable rules for over-receipt and variance thresholds.
- Purchase user/manager access to reporting.

## Installation
Copy `el_purchase_actual_qty` into a custom addons path, restart Odoo, update Apps List, then install or upgrade the module.

```bash
./odoo-bin -d DB_NAME -u el_purchase_actual_qty --stop-after-init
```

## Important validation
Static Python/XML validation is included before delivery. Runtime validation requires an actual Odoo 18 instance with `purchase`, `purchase_stock` and `stock_account` installed. In production, validate AVCO/FIFO, returns, partial receipts, taxes, multi-currency, landed costs, Anglo-Saxon accounting and localization-specific vendor bill flows on staging.

## Git commit
`feat: add purchase actual quantity dashboard and reporting`
