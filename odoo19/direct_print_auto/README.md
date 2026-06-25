# README — Direct Print Auto

**Version:** 19.0.1.0.0
**Author:** Ibrahim Elmasry
**License:** LGPL-3
**Category:** Sales / Sales
**Odoo target:** 19 (also forward-compatible with 19+ APIs)

---

## What this module does

**Direct Print Auto** adds two related capabilities to Odoo 19:

1. **Auto-print on confirm** — When a supported business document is confirmed
   (sales order), posted (customer invoice), validated (outgoing delivery
   picking), or approved (purchase order), the browser's native print dialog
   opens automatically with the relevant report pre-loaded — no extra click
   required.

2. **Manual Direct Print button** — A "Direct Print" button is added to the
   form header of each supported document type, so the user can print
   on-demand regardless of the auto-print toggle.

The print flow uses a **hidden iframe** pattern: the OWL client action
fetches the report HTML via Odoo's `/report/html/<ref>/<id>` route,
injects it into an off-screen iframe, waits for it to load, then calls
`iframe.contentWindow.print()`. This avoids printing the Odoo UI chrome
and lets the user pick any browser-connected printer (physical, PDF,
"Save to Google Drive", etc.).

### Why not just `window.print()` on the main window?

The main Odoo window contains the navbar, the form view, the chatter, etc.
Calling `window.print()` directly would print the entire UI, not just the
report. The iframe pattern ensures only the report HTML is printed.

### Why not just download a PDF?

Downloading a PDF requires an extra click ("Print" in the browser PDF
viewer) and breaks the workflow for users who print many documents in
sequence (e.g. warehouse staff confirming 30 delivery slips in a row).
Direct print auto-opens the native print dialog, where the user just hits
Enter to print and the document is logged as confirmed in the same
operation.

---

## Supported documents

| Document | Model | Confirm method | Report |
|----------|-------|----------------|--------|
| Sales order | `sale.order` | `action_confirm()` | `sale.action_report_saleorder` |
| Customer invoice / refund | `account.move` (out_invoice / out_refund only) | `action_post()` | `account.account_invoices` |
| Outgoing delivery | `stock.picking` (picking_type_code == outgoing only) | `button_validate()` | `stock.action_report_delivery` |
| Purchase order | `purchase.order` | `button_approve()` | `purchase.action_report_purchase_order` |

Vendor bills and incoming/internal pickings are deliberately excluded —
per the user's confirmation, only customer-facing and outgoing documents
qualify for auto-print.

---

## Configuration

1. Install the module.
2. Go to **Settings → Sales → Direct Print** (new section at the bottom
   of the Sales settings tab).
3. Toggle the per-document-type auto-print flags you want:

   - **Auto-print Customer Invoices** — fires on `action_post` for `out_invoice` and `out_refund`
   - **Auto-print Sales Orders** — fires on `action_confirm`
   - **Auto-print Delivery Slips** — fires on `button_validate` for outgoing pickings only
   - **Auto-print Purchase Orders** — fires on `button_approve`
   - **Open Print Dialog for Manual Button** — controls what the manual
     "Direct Print" button does:
     - True (default): opens the browser print dialog
     - False: downloads the PDF instead

4. Save settings.

All toggles default to **off** to avoid surprising users on upgrade.

---

## Usage

### Manual button

Open any supported document (sales order, customer invoice, outgoing
delivery, purchase order). In the form header, click the **Direct Print**
button (printer icon). The browser's print dialog opens immediately with
the report pre-loaded.

### Auto-print

When auto-print is enabled for a document type, the print dialog opens
**automatically** the moment the confirm/post/validate/approve action
completes. After the user closes the print dialog, Odoo's standard
follow-up action (typically returning to the form view in confirmed
state) executes as usual.

### Multi-record operations

Auto-print only fires for **single-record** operations. If the user
selects multiple sales orders and clicks Confirm, the auto-print is
skipped (the standard multi-confirm flow runs as usual). This is a
deliberate design choice to avoid opening 50 print dialogs in a row.

---

## Permissions

| Group | Implied by | Capabilities |
|-------|-----------|--------------|
| Direct Print User (group_direct_print_user) | Sales / See All Leads | Sees and can click the Direct Print button on forms |
| Direct Print Manager (group_direct_print_manager) | Direct Print User | Can change Direct Print settings |

By default, the admin user is a Direct Print Manager.

---

## Dependencies

- `base`
- `web`
- `sale_management`
- `account`
- `stock`
- `purchase`

---

## File map

```
direct_print_auto/
├── __init__.py
├── __manifest__.py
├── .gitignore
├── README.md (this file)
├── docs/
│   ├── icon-design.md
│   ├── build-report.md
│   ├── models.md
│   ├── security.md
│   ├── views.md
│   ├── testing.md
│   ├── configuration.md
│   ├── workflows.md
│   └── architecture/
│       ├── _inventories.md
│       ├── overview.md
│       ├── model-design.md
│       ├── view-design.md
│       ├── data-flow.md
│       ├── state-machine-design.md
│       ├── security-design.md
│       └── owl-component-design.md
├── i18n/                           (empty — translations via base terms)
├── models/
│   ├── __init__.py
│   ├── direct_print_mixin.py       (AbstractModel — shared logic)
│   ├── res_config_settings.py      (5 toggles)
│   ├── sale_order.py
│   ├── account_move.py
│   ├── stock_picking.py
│   └── purchase_order.py
├── security/
│   ├── direct_print_groups.xml     (2 groups)
│   └── ir.model.access.csv         (1 row — settings manager)
├── static/
│   ├── description/
│   │   └── icon.png                (256×256 PNG, 28.8 KB)
│   └── src/
│       ├── js/direct_print_action.js    (OWL client action)
│       └── xml/direct_print_templates.xml (bundle placeholder)
├── tests/
│   ├── __init__.py
│   ├── test_direct_print_mixin.py      (14 unit tests)
│   └── test_auto_print_flow.py         (2 integration tests)
└── views/
    ├── res_config_settings_views.xml
    ├── sale_order_views.xml
    ├── account_move_views.xml
    ├── stock_picking_views.xml
    ├── purchase_order_views.xml
    ├── client_actions.xml
    └── direct_print_menus.xml
```

---

## Uninstallation

The module cleanly uninstalls:

- No new models with persistent tables → no orphan tables.
- No new fields on existing models → no orphan columns.
- Inherited views are automatically removed by Odoo when the module is
  uninstalled.
- System parameters (`direct_print_auto.*`) are removed automatically
  when the module is uninstalled (they are owned by the module via the
  `config_parameter` field on `res.config.settings`).

---

## Compatibility notes

- **Odoo 19+** APIs used:
  - OWL component via `@odoo-module` tag
  - `useService("action")` from `@web/core/utils/hooks`
  - `actionRegistry.add(tag, Component)` from `@web/core/registry`
  - `_inherit = ["sale.order", "direct.print.mixin"]` pattern (multi-inherit with AbstractModel)
  - `res.config.settings` field with `config_parameter=` attribute

- **Not tested on Odoo ≤ 18.** The OWL component uses Odoo 19 module
  syntax (`/** @odoo-module **/`). If you need Odoo 18 compatibility,
  the JS file would need to be split into two files (component + template
  separately) and the registry import path adjusted.

---

## Author

**Ibrahim Elmasry** — Senior Odoo Developer, DevOps Engineer, and Odoo
Implementation Consultant.

For support, bug reports, or feature requests, please use the standard
Odoo Apps store channel or contact the author directly.

---

## Changelog

### 19.0.1.0.0 (initial release)

- Auto-print on confirm for sales orders
- Auto-print on post for customer invoices/refunds (vendor bills excluded)
- Auto-print on validate for outgoing delivery pickings (incoming/internal excluded)
- Auto-print on approve for purchase orders
- Manual "Direct Print" button on all four supported form views
- 5 toggles in Settings → Sales → Direct Print
- OWL client action using hidden iframe + `window.print()` pattern
- 16 unit + integration tests
- Full documentation (8 architecture docs + 6 user docs)
- 256×256 PNG module icon
