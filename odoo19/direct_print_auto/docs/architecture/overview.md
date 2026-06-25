# Architecture Overview — `direct_print_auto`

## Purpose

This document gives a bird's-eye view of the module's design and the
decisions behind it. For a complete inventory of models / views / actions
/ buttons, see `_inventories.md`.

## Design goals

1. **Browser-only, no server-side printer** — The user explicitly chose
   the browser-only print path. This avoids CUPS / IoT Box dependencies
   and works in any Odoo deployment (Odoo.sh, on-prem, Docker).

2. **Auto-print on confirm + manual button** — Both behaviours coexist.
   The manual button is always available; auto-print is opt-in per
   document type.

3. **One mixin, four implementations** — The shared print logic lives
   in `direct.print.mixin` (AbstractModel). Each concrete model
   (`sale.order`, `account.move`, `stock.picking`, `purchase.order`)
   inherits the mixin and provides two overrides:
   - `_get_direct_print_report_ref()` → returns the XML ID of the
     report to print
   - `_should_direct_print_auto()` → returns `True` when auto-print
     should fire for this specific record (considering both the
     settings toggle AND the record's domain filter, e.g. customer
     invoices only)

4. **Settings-driven** — All toggles are stored as `ir.config_parameter`
   entries via the `config_parameter=` field attribute on
   `res.config.settings`. This survives module upgrades and can be
   overridden per-database via the standard `ir.config_parameter` menu.

5. **OWL client action** — The actual printing happens in the browser
   via an OWL client action (tag=`direct_print_auto`). The server
   returns a client action dict with `params={report_ref, res_model,
   res_ids, next_action}`, and the OWL component fetches the report
   HTML and opens the print dialog.

## Layered architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Settings layer (res.config.settings)                           │
│  ─ 5 boolean toggles, all stored in ir.config_parameter         │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ read
                              │
┌─────────────────────────────────────────────────────────────────┐
│  Mixin layer (direct.print.mixin — AbstractModel)               │
│  ─ action_direct_print()          (manual button entry point)   │
│  ─ _trigger_direct_print_after()  (auto-print helper)           │
│  ─ _get_direct_print_report_ref() (abstract — overridden)       │
│  ─ _should_direct_print_auto()    (abstract — overridden)       │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ inherit
                              │
┌──────────────────────┬──────────────────────┬────────────────────────┬──────────────────────┐
│  sale.order          │  account.move        │  stock.picking         │  purchase.order      │
│  ─ action_confirm()  │  ─ action_post()     │  ─ button_validate()   │  ─ button_approve()  │
│    override + wrap   │    override + wrap   │    override + wrap     │    override + wrap   │
└──────────────────────┴──────────────────────┴────────────────────────┴──────────────────────┘
                              │
                              │ returns client action dict
                              │
┌─────────────────────────────────────────────────────────────────┐
│  OWL client action (direct_print_auto tag)                      │
│  ─ reads params.report_ref, params.res_ids                      │
│  ─ builds URL: /report/html/<report_ref>/<ids>                  │
│  ─ loads URL into hidden iframe                                 │
│  ─ on iframe load: iframe.contentWindow.print()                 │
│  ─ after print dialog closes: dispatch params.next_action       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP GET /report/html/...
                              │
┌─────────────────────────────────────────────────────────────────┐
│  Odoo backend (ir.actions.report — unchanged)                   │
│  ─ renders the QWeb report as HTML                              │
│  ─ enforces ACL (user must have read on res_model/res_ids)      │
└─────────────────────────────────────────────────────────────────┘
```

## Key design decisions

### 1. Why wrap `super().action_confirm()` instead of using `@api.onchange` or a server action?

`@api.onchange` only fires on form view field changes, not on button
clicks. Server actions cannot return client actions to the browser
(they only modify records). The only way to inject a print dialog
**after** the user clicks "Confirm" is to override the confirm method,
call `super()`, capture its return value (an action dict), and return
a different action dict (the direct_print_auto client action) that
wraps the original as `next_action`.

### 2. Why a hidden iframe instead of `window.print()` directly?

The main Odoo window's DOM contains the navbar, the form view, the
chatter — printing it directly would print the UI chrome, not the
report. A hidden iframe with the report HTML as its only content
ensures the browser's print engine sees only the report.

### 3. Why fetch `/report/html/...` instead of `/report/pdf/...`?

The PDF route returns binary content that the browser would download
or open in a separate viewer — bypassing the print dialog entirely.
The HTML route returns rendered HTML that can be loaded into an
iframe and printed via `iframe.contentWindow.print()`, which gives
the user the native browser print dialog (with all their saved
printers, paper sizes, etc.).

### 4. Why only single-record auto-print?

If the user selects 30 sales orders and clicks Confirm, opening 30
print dialogs in a row would be unusable. Auto-print is reserved for
the common case: user confirms a single document and wants a printed
copy immediately. Multi-record operations go through the standard
Odoo flow (user can still use the regular "Print" menu afterwards).

### 5. Why exclude vendor bills and incoming/internal pickings?

Per the user's explicit choice in STEP 0. The rationale is that
auto-print is for documents you'd typically print for a customer
(invoices, delivery slips) or for internal approval routing (SOs, POs).
Vendor bills are usually received by email and entered into Odoo, so
there's no need to print them. Internal and incoming pickings happen
in the warehouse and don't typically need a printed copy at the
moment of validation.

### 6. Why `position="inside"` on `//header` instead of `position="before"`?

Odoo's form header has dynamic content (status bar, workflow buttons).
Adding `position="before"` would push our button to the very front of
the header (before any workflow buttons), which is visually awkward.
`position="inside"` appends our button at the end of the header, after
any existing buttons — which is where secondary/utility actions
conventionally live.
