# State Machine Design — ie_stock_movement_report

## No state machine required

This module has no persisted business records with state transitions. The
wizard is a transient form that opens, collects filters, and triggers a PDF.

## Wizard Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Open: User clicks menu
    Open --> Validating: User clicks "Print PDF"
    Validating --> Rendering: dates valid
    Validating --> Open: UserError (date_from > date_to)
    Rendering --> PDF_Delivered: QWeb renders
    PDF_Delivered --> [*]
    Open --> Cancelled: User clicks "Cancel"
    Cancelled --> [*]
```

## Stock Move Line State (consumed, not modified)

The report reads `stock.move.line` records in state `done` only:

```mermaid
stateDiagram-v2
    [*] --> draft: move created
    draft --> confirmed: confirmed
    confirmed --> assigned: reserved
    assigned --> done: validated
    done --> [*]: included in report
    draft --> cancelled
    cancelled --> [*]: excluded from report
```

Only `done` state lines are included — `draft`, `confirmed`, `assigned`,
`cancelled` are excluded via the domain filter `('state', '=', 'done')`.
