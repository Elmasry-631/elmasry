# Views Reference — `direct_print_auto`

## View inventory

| # | View XML ID | Type | Inherits | File |
|---|-------------|------|----------|------|
| 1 | `res_config_settings_view_form_direct_print` | Form (inherit) | `sale.res_config_settings_view_form_sale` | `views/res_config_settings_views.xml` |
| 2 | `view_order_form_direct_print` | Form (inherit) | `sale.view_order_form` | `views/sale_order_views.xml` |
| 3 | `view_move_form_direct_print` | Form (inherit) | `account.view_move_form` | `views/account_move_views.xml` |
| 4 | `view_picking_form_direct_print` | Form (inherit) | `stock.view_picking_form` | `views/stock_picking_views.xml` |
| 5 | `purchase_order_form_direct_print` | Form (inherit) | `purchase.purchase_order_form` | `views/purchase_order_views.xml` |
| 6 | `action_direct_print_client` | `ir.actions.client` record | — | `views/client_actions.xml` |
| 7 | `menu_direct_print_root` | `ir.ui.menu` record (hidden) | — | `views/direct_print_menus.xml` |

---

## 1. Settings view

**File:** `views/res_config_settings_views.xml`

Adds a new `<block>` titled "Direct Print" inside the `<app name="sale">`
section of the Sales settings tab.

### XPath used

```xml
<xpath expr="//app[@name='sale']" position="inside">
```

### Fields added

- `direct_print_invoice_auto` (Boolean)
- `direct_print_so_auto` (Boolean)
- `direct_print_picking_auto` (Boolean)
- `direct_print_po_auto` (Boolean)
- `direct_print_open_dialog` (Boolean)

Each field is wrapped in a Bootstrap-style `col-lg-6 o_setting_box`
div with a `<label>` and a `text-muted` description, following
Odoo's standard settings layout conventions.

---

## 2. Sales order form

**File:** `views/sale_order_views.xml`

Adds a "Direct Print" button to the `//header` of the SO form.

### XPath used

```xml
<xpath expr="//header" position="inside">
```

### Button added

```xml
<button name="action_direct_print"
        type="object"
        string="Direct Print"
        class="oe_highlight"
        icon="fa-print"
        groups="direct_print_auto.group_direct_print_user"/>
```

### Visibility

Always visible (no `invisible=` domain), per the user's STEP 0
confirmation. The button can be clicked in any SO state (draft,
sent, sale, done, cancelled).

---

## 3. Customer invoice form

**File:** `views/account_move_views.xml`

Same structure as #2 — adds a Direct Print button to the
`account.move` form header. Always visible.

**Note:** The button appears on ALL `account.move` form views
(invoices, refunds, vendor bills, journal entries). Clicking it on
a vendor bill will print the vendor bill report — this is correct
behaviour for the manual button (the user explicitly clicked it).
The auto-print filter (customer invoices only) applies only to the
auto-print-on-post flow, not to the manual button.

---

## 4. Delivery picking form

**File:** `views/stock_picking_views.xml`

Same structure — adds a Direct Print button to the `stock.picking`
form header. Always visible on all picking types (incoming,
internal, outgoing).

**Note:** Clicking the button on an incoming picking prints the
receipt report. The auto-print filter (outgoing only) applies only
to the auto-print-on-validate flow.

---

## 5. Purchase order form

**File:** `views/purchase_order_views.xml`

Same structure — adds a Direct Print button to the `purchase.order`
form header. Always visible.

---

## 6. Client action

**File:** `views/client_actions.xml`

Declares an `ir.actions.client` record with `tag=direct_print_auto`.
This is the bridge between the server-side action dict returned by
`action_direct_print()` / `_trigger_direct_print_after()` and the
OWL component registered under the same tag in
`static/src/js/direct_print_action.js`.

The `params` field is set to `{}` (empty dict) at the data level.
The actual params are populated dynamically by the Python methods
when they construct the action dict at runtime.

---

## 7. Hidden menu

**File:** `views/direct_print_menus.xml`

Declares a single `ir.ui.menu` record with `active=False` (hidden).
This is a placeholder for future features (e.g. a "Print Jobs" log
or a batch-printing UI). It has no `action=` ref and is not visible
anywhere in the Odoo menu.

If you don't want this placeholder, you can safely delete the file
and remove it from the manifest `data[]` list.

---

## Why all form inherits use `position="inside"` on `//header`

Odoo's form view header typically contains:

- Workflow buttons (Confirm, Validate, Post, Cancel)
- Statusbar (showing the current state)
- Action dropdown (Print, Actions, etc.)

Adding our button with `position="inside"` appends it as the last
child of the header — after any existing buttons. This is the
conventional location for secondary/utility actions and avoids
displacing the primary workflow buttons.

Alternative positions considered:
- `position="before"` — would push our button to the very front of
  the header, before any workflow buttons. Visually awkward.
- A custom XPath targeting a specific button — fragile, depends on
  the exact structure of the parent form which can change between
  Odoo versions.

`position="inside"` on `//header` is the most robust choice.
