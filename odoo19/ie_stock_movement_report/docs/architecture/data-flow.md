# Data Flow — ie_stock_movement_report

## End-to-end data flow

```mermaid
sequenceDiagram
    actor U as User
    participant W as Wizard
    participant R as Report Handler
    participant M as stock.movement.report
    participant SML as stock.move.line
    participant PP as product.product
    participant Q as QWeb Template
    participant PDF as wkhtmltopdf

    U->>W: Open wizard, set filters
    W->>W: _check_dates() constraint
    U->>W: Click "Print PDF"
    W->>R: report_action(data)
    R->>M: get_report_data(date_from, ...)
    M->>SML: read_group(product_ids in period)
    M->>PP: read([cost, uom, categ, name, code])
    M->>SML: search_read(opening balance, date < from)
    M->>SML: search_read(period, with all fields)
    M->>M: in-memory balance computation
    M-->>R: payload dict
    R-->>Q: docs=[payload]
    Q->>PDF: render QWeb → PDF
    PDF-->>U: download PDF
```

## Performance strategy

1. **ONE query** for product IDs in period (read_group)
2. **ONE query** for product data (read() on small set)
3. **ONE query** for opening balance (search_read with date < from_date)
4. **ONE query** for period move lines (search_read with date in [from, to])
5. **TWO queries** for partner + location names (display_name prefetch)
6. **In-memory** defaultdict grouping + running balance computation

Total: ~6 SQL queries regardless of movement count. No ORM calls in loops.
