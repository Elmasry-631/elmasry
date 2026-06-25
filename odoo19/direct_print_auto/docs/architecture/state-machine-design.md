# State Machine Design — `direct_print_auto`

## Summary

This module **introduces no new state machines**. All four target
models (`sale.order`, `account.move`, `stock.picking`,
`purchase.order`) have their own pre-existing state machines defined
by the standard Odoo `sale`, `account`, `stock`, and `purchase`
modules. The Direct Print module **hooks into the transitions** of
those existing state machines, but does **not** modify them.

---

## Where Direct Print hooks in

| Model | Standard transition | Direct Print hook | What we do |
|-------|---------------------|-------------------|------------|
| `sale.order` | `draft` → `sale` (via `action_confirm`) | Override `action_confirm` | Call `super()`, then optionally wrap return value with `direct_print_auto` client action |
| `account.move` | `draft` → `posted` (via `action_post`) | Override `action_post` | Same pattern — call `super()`, wrap return value if auto-print is on AND move_type is customer-facing |
| `stock.picking` | `assigned`/`confirmed` → `done` (via `button_validate`) | Override `button_validate` | Same pattern — wrap return value if auto-print is on AND picking is outgoing |
| `purchase.order` | `draft` → `purchase` (via `button_approve`) | Override `button_approve` | Same pattern — wrap return value if auto-print is on |

---

## Why we don't modify state transitions

Direct Print is a **presentation concern**, not a business-rule concern.
The state machine defines *when* a document is "confirmed" — Direct
Print just decides *what to show the user* after that confirmation
happens. Mixing the two would violate separation of concerns and make
the module harder to uninstall safely.

The override pattern is intentionally minimal:

```python
def action_confirm(self):
    action = super().action_confirm()   # ← standard state transition runs unchanged
    return self._trigger_direct_print_after(action)  # ← optionally wrap the return value
```

If `super().action_confirm()` raises an exception (e.g. the SO can't
be confirmed due to missing fields), our override never executes the
`_trigger_direct_print_after` call — the exception propagates as
usual. This means auto-print **only fires on successful confirmations**,
which is the correct behaviour.

---

## Behaviour matrix

| Scenario | Toggle | Result |
|----------|--------|--------|
| Single SO confirm, SO toggle on | ✅ on | Auto-print fires |
| Single SO confirm, SO toggle off | ❌ off | Standard confirm, no auto-print |
| Multi-SO confirm (5 SOs selected), SO toggle on | ✅ on | Standard multi-confirm, no auto-print (single-record check fails) |
| Single vendor bill post, invoice toggle on | ✅ on | Standard post, no auto-print (domain filter excludes in_invoice) |
| Single customer invoice post, invoice toggle on | ✅ on | Auto-print fires |
| Single customer invoice post, invoice toggle off | ❌ off | Standard post, no auto-print |
| Single outgoing picking validate, picking toggle on | ✅ on | Auto-print fires |
| Single incoming picking validate, picking toggle on | ✅ on | Standard validate, no auto-print (domain filter excludes non-outgoing) |
| Single PO approve, PO toggle on | ✅ on | Auto-print fires |
| Single PO approve, PO toggle off | ❌ off | Standard approve, no auto-print |
| Manual "Direct Print" button click (any state) | n/a | Print dialog opens immediately (button is always visible per STEP 0) |

---

## Manual button visibility

Per the user's confirmation in STEP 0, the **Direct Print button is
always visible** on the form view — no `invisible=` domain based on
state. This means the user can:

- Print a draft quotation before sending it to the customer
- Print a confirmed sales order for their records
- Print a cancelled invoice for audit purposes
- Print a done delivery slip for re-printing after the original was lost

The button does **not** depend on the auto-print toggle. It's a
standalone utility, available regardless of state or settings.
