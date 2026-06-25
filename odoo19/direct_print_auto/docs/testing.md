# Testing Plan — `direct_print_auto`

## Overview

This document describes the test plan for the `direct_print_auto`
module. It includes:

1. Automated tests shipped with the module (in `tests/`)
2. Manual test scenarios for the user to execute after installation
3. Edge-case coverage

**Note:** Automated tests cover the Python-side logic (mixin API,
auto-print gating, action dict construction). The OWL client
action's iframe-based printing cannot be meaningfully unit-tested
(it requires a real browser with a real print dialog) — that part
is covered by the manual test scenarios below.

---

## Automated tests

### `tests/test_direct_print_mixin.py` — 14 unit tests

| Test # | Description |
|--------|-------------|
| 01 | `sale.order._get_direct_print_report_ref()` returns `"sale.action_report_saleorder"` |
| 02 | `account.move._get_direct_print_report_ref()` returns `"account.account_invoices"` |
| 03 | `stock.picking._get_direct_print_report_ref()` returns `"stock.action_report_delivery"` |
| 04 | `purchase.order._get_direct_print_report_ref()` returns `"purchase.action_report_purchase_order"` |
| 10 | SO auto-print disabled by default (toggle off) → `_should_direct_print_auto()` returns `False` |
| 11 | SO auto-print enabled (toggle on) → `_should_direct_print_auto()` returns `True` |
| 12 | Invoice auto-print customer-only: customer invoice returns `True`, vendor bill returns `False` (even with toggle on) |
| 13 | Picking auto-print outgoing-only: outgoing returns `True`, incoming returns `False` (even with toggle on) |
| 20 | Manual button: `action_direct_print()` returns a client action dict with the correct `tag`, `report_ref`, `res_model`, `res_ids` |

### `tests/test_auto_print_flow.py` — 2 integration tests

| Test # | Description |
|--------|-------------|
| 30 | SO confirm with auto-print on: `action_confirm()` returns a `direct_print_auto` client action wrapping the original confirm action as `next_action` |
| 31 | SO confirm with auto-print off: `action_confirm()` returns the standard confirm action (not a direct_print_auto client action) |

### How to run the automated tests

```bash
# From the Odoo server, with the database ready and the module installed:
odoo --test-enable --test-tags=/direct_print_auto --stop-after-init -d <your_db>

# Or via the Odoo shell:
odoo-shell -d <your_db> --test-enable --test-tags=/direct_print_auto
```

---

## Manual test scenarios

After installing the module on a fresh Odoo 19 database with demo
data, execute these scenarios. Each scenario lists the setup, the
action, and the expected result.

### Scenario 1: Manual button — sales order

**Setup:**
- Create a sales order with at least one line item (don't confirm it yet)

**Action:**
- Open the SO form view
- Click the "Direct Print" button in the form header

**Expected:**
- The Direct Print client action takes over the main content area
- A loading spinner appears ("Preparing print preview…")
- After ~400ms, the browser's native print dialog opens
- The print preview shows the SO report (not the Odoo UI chrome)
- After closing the print dialog (Print or Cancel), the user is
  returned to the SO form view

### Scenario 2: Manual button — customer invoice

**Setup:**
- Create a customer invoice (`account.move`, `move_type=out_invoice`)
- Add at least one invoice line

**Action:**
- Click "Direct Print" on the invoice form

**Expected:**
- Same flow as Scenario 1, but the report is the customer invoice
  report (`account.account_invoices`)

### Scenario 3: Manual button — vendor bill

**Setup:**
- Create a vendor bill (`account.move`, `move_type=in_invoice`)

**Action:**
- Click "Direct Print" on the vendor bill form

**Expected:**
- The print dialog opens with the vendor bill report (the manual
  button works on all move types — the customer-only filter only
  applies to auto-print)

### Scenario 4: Manual button — outgoing delivery

**Setup:**
- Create a delivery order (`stock.picking`, picking type outgoing)
- Mark as available (set quantities done)

**Action:**
- Click "Direct Print" on the picking form

**Expected:**
- Print dialog opens with the delivery slip report

### Scenario 5: Manual button — incoming picking

**Setup:**
- Create a receipt (`stock.picking`, picking type incoming)

**Action:**
- Click "Direct Print" on the picking form

**Expected:**
- Print dialog opens with the receipt report (the manual button
  works on all picking types — the outgoing-only filter only applies
  to auto-print)

### Scenario 6: Manual button — purchase order

**Setup:**
- Create a purchase order with at least one line

**Action:**
- Click "Direct Print" on the PO form

**Expected:**
- Print dialog opens with the PO report

### Scenario 7: Auto-print SO on confirm (toggle on)

**Setup:**
- Go to Settings → Sales → Direct Print
- Toggle "Auto-print Sales Orders" ON
- Save settings
- Create a new SO with one line item

**Action:**
- Click "Confirm" on the SO form

**Expected:**
- The SO state changes to "Sales Order" (standard confirm runs first)
- Immediately after, the Direct Print client action takes over
- The print dialog opens with the SO report
- After closing the print dialog, the user is returned to the
  confirmed SO form view (state="Sales Order")

### Scenario 8: Auto-print SO off (toggle off)

**Setup:**
- Ensure "Auto-print Sales Orders" is OFF in settings
- Create a new SO

**Action:**
- Click "Confirm" on the SO form

**Expected:**
- Standard Odoo confirm flow: SO state changes to "Sales Order"
- No print dialog opens
- The Direct Print button is still available on the confirmed form
  for manual printing

### Scenario 9: Auto-print customer invoice on post

**Setup:**
- Toggle "Auto-print Customer Invoices" ON
- Create a customer invoice (`out_invoice`) with one line

**Action:**
- Click "Post" on the invoice form

**Expected:**
- Standard post flow: invoice state changes to "Posted"
- Print dialog opens with the customer invoice report
- After closing, user is returned to the posted invoice form

### Scenario 10: Vendor bill does NOT auto-print

**Setup:**
- "Auto-print Customer Invoices" is ON
- Create a vendor bill (`in_invoice`)

**Action:**
- Click "Post" on the vendor bill form

**Expected:**
- Standard post flow: vendor bill is posted
- **No print dialog opens** (domain filter excludes `in_invoice`)
- The manual Direct Print button is still available if needed

### Scenario 11: Outgoing delivery auto-prints on validate

**Setup:**
- Toggle "Auto-print Delivery Slips" ON
- Create an outgoing delivery picking with stock moves
- Set quantities done (mark as done)

**Action:**
- Click "Validate" on the picking form

**Expected:**
- Standard validate flow: picking state changes to "Done"
- Print dialog opens with the delivery slip report

### Scenario 12: Incoming picking does NOT auto-print

**Setup:**
- "Auto-print Delivery Slips" is ON
- Create an incoming picking (receipt) with stock moves
- Set quantities done

**Action:**
- Click "Validate" on the picking form

**Expected:**
- Standard validate flow: receipt is validated
- **No print dialog opens** (domain filter excludes non-outgoing)
- Manual Direct Print button still available

### Scenario 13: PO auto-print on approve

**Setup:**
- Toggle "Auto-print Purchase Orders" ON
- Create a purchase order in "To Approve" state (need approval flow)

**Action:**
- Click "Approve" on the PO form

**Expected:**
- Standard approve flow: PO state changes to "Purchase Order"
- Print dialog opens with the PO report

### Scenario 14: Multi-record confirm (no auto-print)

**Setup:**
- "Auto-print Sales Orders" is ON
- Create 3 SOs in list view, select all 3

**Action:**
- Use the action menu → "Confirm" (multi-confirm)

**Expected:**
- All 3 SOs are confirmed (standard multi-confirm flow)
- **No print dialog opens** (multi-record auto-print is skipped by design)
- A notification appears showing the 3 confirmed SOs

### Scenario 15: Permissions — Direct Print User

**Setup:**
- Create a user with only the "Direct Print User" group (implied by
  Sales / See All Leads)
- Log in as this user

**Action:**
- Open a sales order form

**Expected:**
- The Direct Print button is visible in the form header
- Clicking it works (print dialog opens)
- The user cannot access Settings → Direct Print (no Settings manager
  access)

### Scenario 16: Permissions — Sales user without Direct Print User group

**Setup:**
- Create a user with Sales / See All Leads but NOT Direct Print User

**Action:**
- Open a sales order form

**Expected:**
- The Direct Print button is **not visible** in the form header
  (hidden by `groups=` attribute)

### Scenario 17: Uninstall

**Setup:**
- Module installed, with auto-print toggles set

**Action:**
- Uninstall the module via Apps

**Expected:**
- The Direct Print button disappears from all form views
- The Direct Print settings block disappears from Settings → Sales
- The `direct_print_auto.*` system parameters are removed
- No errors during uninstall (no orphan records/tables/columns)
- All four target models (SO, invoice, picking, PO) continue to work
  normally (standard confirm/post/validate/approve behaviour restored)

---

## Edge cases to verify

| # | Edge case | Expected behaviour |
|---|-----------|--------------------|
| E1 | Print a cancelled SO | Manual button works — print dialog opens with the cancelled SO report |
| E2 | Print a draft quotation | Manual button works — print dialog opens with the draft quote report |
| E3 | Browser blocks popups | If the browser blocks the iframe's print dialog, the loading spinner will stay forever. User must allow popups for the Odoo domain. (Consider adding a "Cancel" button after a timeout — future improvement.) |
| E4 | Slow network — report takes 10s to render | Loading spinner stays visible until the iframe loads. Once loaded, the 350ms delay runs and the print dialog opens. |
| E5 | User closes print dialog with Cancel (not Print) | Same as clicking Print — `_dispatchNext()` runs after 400ms, user is returned to the next action. No error. |
| E6 | Report template is missing (e.g. `account.account_invoices` was renamed in a custom module) | The iframe will load a 404 error page. The print dialog will open with the 404 content. User can close it. (Future improvement: detect 404 in the iframe response and show an error.) |
| E7 | User doesn't have read access to the record | `/report/html/<ref>/<id>` returns 403. The iframe will load the 403 error page. Same as E6. |
| E8 | Multiple Direct Print clicks in rapid succession | The `_printed` flag in `onFrameLoad()` prevents double-printing. Subsequent clicks would open new client actions, each with their own `_printed` flag — so each click opens its own print dialog. Acceptable behaviour. |
