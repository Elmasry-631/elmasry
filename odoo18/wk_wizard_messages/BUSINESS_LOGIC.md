# wk_wizard_messages — Business Logic & Functionality

**Author:** Webkul Software Pvt. Ltd.  
**Version:** 1.0.0  
**Category:** Extra Tools  
**Dependencies:** None (base Odoo only)

---

## Purpose

`wk_wizard_messages` is a small utility module that provides a reusable popup dialog for displaying HTML messages, warnings, and operation summaries inside Odoo. It has no e-commerce logic of its own.

It exists as a shared dependency for other Webkul modules — most notably `odoo_multi_channel_sale`, which uses it to show import/export results, connection test feedback, and error summaries.

---

## Core Model

### `wk.wizard.message` (TransientModel)

| Field | Type | Description |
|-------|------|-------------|
| `text` | Html | The message body shown to the user |

**Key method:** `genrated_message(message, name='Message/Summary')`

1. Creates a transient record with the given HTML message.
2. Returns a window action that opens the record in a modal popup (`target: new`).

---

## User Interface

- A simple form view with a read-only HTML field and a **Close** button.
- No buttons for confirmation or further action — display only.

---

## How Other Modules Use It

`odoo_multi_channel_sale` calls it via:

```python
self.env['wk.wizard.message'].genrated_message(message, 'Summary')
```

This is wrapped in `multi.channel.sale.display_message()` and used after:

- Import/export operations (`ApiTransaction`)
- Feed evaluation (products, orders, categories, partners)
- Connection tests
- Channel configuration actions

---

## Business Flow

```
Other module completes an operation
        │
        ▼
Builds HTML summary (success/error counts, alerts)
        │
        ▼
Calls genrated_message()
        │
        ▼
User sees popup with formatted result
        │
        ▼
User clicks Close → transient record discarded
```

---

## Scope & Limitations

- **No persistence** — records are transient and disappear after the dialog is closed.
- **No business rules** — no validation, workflow, or data transformation.
- **No API or cron jobs** — purely a UI helper.
- **Single responsibility** — show a message; nothing else.

---

## Summary

| Aspect | Detail |
|--------|--------|
| Role | Shared UI utility for HTML message popups |
| Main consumer | `odoo_multi_channel_sale` |
| Data stored | None (transient) |
| Configuration | None required |
| Standalone value | Minimal — install only as a dependency |
