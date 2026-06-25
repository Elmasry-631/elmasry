# Configuration Guide — `direct_print_auto`

## Installation

1. Drop the `direct_print_auto` folder into your Odoo `addons` directory.
2. Restart the Odoo server.
3. Go to **Apps**, search for "Direct Print Auto", click **Install**.

The module depends on `base`, `web`, `sale_management`, `account`,
`stock`, and `purchase`. If any of these are not yet installed, Odoo
will install them automatically as part of the Direct Print Auto
installation.

---

## Post-installation setup

### Step 1 — Grant the Direct Print User group

By default, the admin user is a Direct Print Manager. Other users
need to be granted the Direct Print User group to see the Direct
Print button on form views.

1. Go to **Settings → Users → Manage Users**.
2. Open each user who needs Direct Print access.
3. Under the **Direct Print** group category (new), check
   "Direct Print User" (or "Direct Print Manager" for users who
   should also be able to change settings).
4. Save.

> **Tip:** The "Direct Print User" group is implied by the standard
> "Sales / See All Leads" group, so any salesperson will
> automatically be a Direct Print User once you install the module.
> You only need to manage this group for non-sales users (e.g.
> warehouse staff, purchase managers).

### Step 2 — Configure the auto-print toggles

1. Go to **Settings → Sales**.
2. Scroll down to the new **Direct Print** section.
3. Toggle the desired auto-print behaviours:

| Toggle | Effect |
|--------|--------|
| Auto-print Customer Invoices | Opens the print dialog when a customer invoice/refund is posted |
| Auto-print Sales Orders | Opens the print dialog when a sales order is confirmed |
| Auto-print Delivery Slips | Opens the print dialog when an outgoing delivery picking is validated |
| Auto-print Purchase Orders | Opens the print dialog when a purchase order is approved |
| Open Print Dialog for Manual Button | Controls the manual button: True = open print dialog (default), False = download PDF |

4. Click **Save**.

All toggles default to **off** (except the manual-button behaviour,
which defaults to "open print dialog"). This ensures the module
doesn't change behaviour for existing users until you explicitly
opt in.

---

## Per-document-type behaviour summary

| Document type | Auto-print trigger | Domain filter | Default |
|---------------|--------------------|---------------|---------|
| Sales order | `action_confirm()` | (none — any SO) | OFF |
| Customer invoice | `action_post()` | `move_type in ('out_invoice', 'out_refund')` | OFF |
| Outgoing delivery | `button_validate()` | `picking_type_id.code == 'outgoing'` | OFF |
| Purchase order | `button_approve()` | (none — any PO) | OFF |

The manual Direct Print button is **always available** on all four
form types, regardless of these toggles. The toggles only control
the auto-print-on-confirm/post/validate/approve flow.

---

## Browser configuration

### Allow popups for the Odoo domain

Most modern browsers block `iframe.contentWindow.print()` calls if
the iframe was loaded via JavaScript (rather than the user clicking
a link). To ensure the Direct Print client action works:

1. In Chrome: **Settings → Privacy and security → Site Settings →
   Pop-ups and redirects → Allow** → add your Odoo domain.
2. In Firefox: **Settings → Privacy & Security → Permissions →
   Block pop-up windows → Exceptions** → add your Odoo domain.
3. In Edge: **Settings → Cookies and site permissions → Pop-ups and
   redirects → Allow** → add your Odoo domain.

If popups are blocked, the Direct Print client action will show the
loading spinner indefinitely. The user would then need to allow
popups and retry.

### Default printer

The print dialog uses the browser's default printer. To change
which printer is selected by default:

1. In Chrome: open `chrome://settings/printing` and set the
   default printer.
2. In Firefox: open `about:preferences#general`, scroll to
   "Applications", find "Portable Document Format (PDF)", and
   configure the default behaviour.
3. In Edge: open `edge://settings/printing` and set the default
   printer.

### Paper size and orientation

The print dialog inherits the report's CSS `@page` rules. Odoo's
default reports use A4 portrait. If your printer defaults to Letter
landscape, you'll need to either:

- Change the printer's default paper size in the OS printer settings, OR
- Modify the report template's `@page` rule (out of scope for this module)

---

## Production deployment tips

### Performance

Direct Print adds negligible overhead:

- The mixin methods are O(1) per record.
- The auto-print check reads one `ir.config_parameter` row per
  confirm/post/validate call — cached by Odoo's ORM.
- The OWL client action loads the report HTML in a hidden iframe —
  this is the same HTTP request the standard "Print" menu would
  make, just delivered to an iframe instead of a new tab.

No database indexes, no extra tables, no background jobs.

### Rollback

If you need to disable Direct Print temporarily without
uninstalling:

1. Go to **Settings → Sales → Direct Print**.
2. Turn off all four auto-print toggles.
3. Save.

The manual Direct Print button will still be visible (you can hide
it by removing the `direct_print_auto.group_direct_print_user`
group from all users), but auto-print is fully disabled.

To completely remove the module, use **Apps → Uninstall**. The
uninstall is clean (no orphan records — see `docs/security.md`
for details).

### Upgrade

The module uses only public Odoo APIs and standard OWL patterns.
Future Odoo upgrades (19.x → 20.x) should require no changes to
the module code. If Odoo changes the OWL module system or the
`/report/html/<ref>/<id>` route, the JS file would need to be
updated — but no data migration is required.

---

## Troubleshooting

### "The Direct Print button doesn't appear on the form"

Check:
1. Is the user in the `Direct Print User` group?
2. Is the module actually installed? (Check Apps list)
3. Did the inherited view load correctly? (Go to Settings →
   Technical → User Interface → Views, search for
   `view_order_form_direct_print` — it should exist and be active)

### "Clicking Direct Print shows a loading spinner that never ends"

This is almost always a popup blocker issue. Check:
1. Are popups allowed for the Odoo domain in the browser?
2. Open the browser's developer tools console — are there any
   errors?
3. Check the Network tab — did the `/report/html/...` request
   succeed (200) or fail (403/404)?

### "The print dialog opens but shows the wrong report"

Check the report XML ID returned by `_get_direct_print_report_ref()`
for the model. If you've installed a custom report module that
overrides the standard report (e.g. a custom invoice template),
you may want to override `_get_direct_print_report_ref()` in your
custom module to return the custom report's XML ID instead.

### "Auto-print doesn't fire on confirm"

Check:
1. Is the relevant toggle ON in Settings → Sales → Direct Print?
2. Is the user confirming a single record (not multi-select)?
3. For invoices: is the move_type `out_invoice` or `out_refund`?
   (Vendor bills don't auto-print)
4. For pickings: is the picking type `outgoing`? (Incoming/internal
   don't auto-print)
5. Check the Odoo server logs — are there any exceptions during
   the confirm call?

### "After printing, the form view doesn't reload"

The Direct Print client action dispatches `next_action` after the
print dialog closes. If `next_action` is the standard confirm
action (e.g. `{'type': 'ir.actions.act_window', ...}`), the form
should reload. If it doesn't:

1. Check the browser console — are there any errors after the
   print dialog closes?
2. Try increasing the 400ms post-print delay in
   `static/src/js/direct_print_action.js` (`_dispatchNext()`
   call) to 800ms or 1000ms — some browsers need more time to
   clean up the print pipeline.
