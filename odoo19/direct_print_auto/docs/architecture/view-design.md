# View Design — `direct_print_auto`

## View inventory

| View XML ID | Type | Inherits | Purpose |
|-------------|------|----------|---------|
| `res_config_settings_view_form_direct_print` | Form (inherit) | `sale.res_config_settings_view_form_sale` | Adds Direct Print settings block |
| `view_order_form_direct_print` | Form (inherit) | `sale.view_order_form` | Adds Direct Print button to SO header |
| `view_move_form_direct_print` | Form (inherit) | `account.view_move_form` | Adds Direct Print button to invoice header |
| `view_picking_form_direct_print` | Form (inherit) | `stock.view_picking_form` | Adds Direct Print button to picking header |
| `purchase_order_form_direct_print` | Form (inherit) | `purchase.purchase_order_form` | Adds Direct Print button to PO header |

No new views are created — all are inherits that add a single button
or a single settings block to existing forms.

---

## Settings view — XPath strategy

```xml
<xpath expr="//app[@name='sale']" position="inside">
    <block title="Direct Print" name="direct_print_auto_settings_block">
        ...
    </block>
</xpath>
```

### Why `//app[@name='sale']` and not a more specific XPath?

The Odoo `res.config.settings` form is structured as:

```xml
<form>
    <app data-string="Sales" name="sale" string="Sales" ...>
        <block title="Quotations &amp; Orders" name="quotations_orders_setting">...</block>
        <block title="Pricing" name="pricing_setting">...</block>
        ...
    </app>
    <app data-string="Invoicing" name="account" ...>...</app>
    ...
</form>
```

The exact `name` attribute of each `<block>` can change between Odoo
versions. By targeting `//app[@name='sale']` with `position="inside"`,
we append our `<block>` as the last child of the Sales app — robust
against minor changes in upstream Odoo.

---

## Form view button — XPath strategy

All four form-view inherits use the same XPath:

```xml
<xpath expr="//header" position="inside">
    <button name="action_direct_print"
            type="object"
            string="Direct Print"
            class="oe_highlight"
            icon="fa-print"
            groups="direct_print_auto.group_direct_print_user"/>
</xpath>
```

### Why `//header` `position="inside"`?

The form view header typically contains workflow buttons (Confirm,
Validate, Post, etc.) and the statusbar. Adding `position="inside"`
appends our button at the end of the header — after any existing
buttons — which is the conventional location for secondary/utility
actions like "Direct Print".

### Why `groups=` on the button?

The Direct Print button is only meaningful for users who have the
`Direct Print User` group (which is implied by Sales / See All Leads).
Hiding the button for other users avoids cluttering the header for
users who can't use it.

### Why `class="oe_highlight"`?

`oe_highlight` is Odoo's standard CSS class for visually emphasizing a
button (makes it the primary action color — usually blue). This makes
the Direct Print button stand out from workflow buttons like "Confirm"
which use the default styling.

Per the user's confirmation in STEP 0, the button is **always visible**
(no `invisible=` domain) so the user can print draft quotes, etc., on
demand.

---

## Client action declaration

```xml
<record id="action_direct_print_client" model="ir.actions.client">
    <field name="name">Direct Print</field>
    <field name="tag">direct_print_auto</field>
    <field name="params">{}</field>
</record>
```

### Why declare an `ir.actions.client` if the OWL component is what renders?

Three reasons:

1. **Discoverability** — Having an XML ID for the client action means
   server actions, menus, or other modules can reference it via
   `direct_print_auto.action_direct_print_client`.

2. **Future-proofing** — If we later want to add a menu item that
   opens the Direct Print action (e.g. for batch printing), the
   action record already exists.

3. **Tag registration validation** — Odoo warns at install time if
   an `ir.actions.client` record references a `tag` that no OWL
   component has registered. Declaring the action here ensures the
   tag is exercised during install, surfacing any registration bugs
   immediately.

---

## Hidden menu record

```xml
<record id="menu_direct_print_root" model="ir.ui.menu">
    <field name="name">Direct Print</field>
    <field name="sequence">90</field>
    <field name="active" eval="False"/>
</record>
```

### Why a hidden menu?

The module is settings-driven — there's no need for a top-level menu
item. However, declaring the menu record (with `active=False`) gives
us a stable XML ID that other modules could enable if they want to
expose a Direct Print management UI. It's also a placeholder for
future features (e.g. a "Print Jobs" log).

If you don't want this placeholder, you can safely delete the file
`views/direct_print_menus.xml` and remove it from the manifest `data[]`
list.
