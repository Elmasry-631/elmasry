# Workflows — `direct_print_auto`

## Workflow 1 — Salesperson confirms an order

**Persona:** Anna, a salesperson at a mid-size retail company.
**Goal:** Confirm a sales order in Odoo and immediately hand a
printed copy to the warehouse team for fulfilment.

### Without Direct Print Auto

1. Anna opens the SO form.
2. Clicks **Confirm**. SO state → "Sales Order".
3. Form reloads in confirmed state.
4. Anna clicks **Print** in the action dropdown.
5. Browser downloads the SO PDF.
6. Anna opens the PDF in the browser's built-in viewer.
7. Anna clicks **Print** in the PDF viewer.
8. Browser print dialog opens.
9. Anna selects the office printer, clicks **Print**.
10. Anna walks to the printer, picks up the SO, hands it to the
    warehouse team.

**Total clicks:** ~5. Time: ~30 seconds per SO.

### With Direct Print Auto (auto-print ON)

1. Anna opens the SO form.
2. Clicks **Confirm**. SO state → "Sales Order".
3. Browser print dialog opens immediately (auto-print).
4. Anna selects the office printer (or it's already the default),
   clicks **Print**.
5. Anna walks to the printer, picks up the SO, hands it to the
    warehouse team.

**Total clicks:** ~2. Time: ~10 seconds per SO.

**Saved per SO:** ~20 seconds, 3 clicks. For a salesperson
confirming 30 SOs/day, that's ~10 minutes/day saved.

---

## Workflow 2 — Warehouse validates a delivery

**Persona:** Bob, a warehouse worker.
**Goal:** Validate an outgoing delivery picking and immediately
print the delivery slip to attach to the shipment.

### With Direct Print Auto (picking toggle ON)

1. Bob opens the delivery picking form.
2. Sets quantities done (or uses the barcode scanner to mark
   picked quantities).
3. Clicks **Validate**. Picking state → "Done".
4. Browser print dialog opens automatically.
5. Bob selects the warehouse label printer (or it's already the
   default), clicks **Print**.
6. Bob picks up the printed delivery slip from the label printer,
   staples it to the shipment, and ships it.

**Key benefit:** Bob never has to leave the picking form — the
print dialog is part of the validate flow. This is critical in a
fast-paced warehouse where workers confirm hundreds of pickings
per shift.

---

## Workflow 3 — Accounting posts a batch of customer invoices

**Persona:** Carla, an accountant.
**Goal:** Post the day's customer invoices and email/print each
one for the customer.

### With Direct Print Auto (invoice toggle ON, but for batch work)

**Important:** Direct Print Auto intentionally skips multi-record
operations. If Carla multi-selects 20 invoices and clicks **Post**,
the standard batch-post flow runs (all 20 invoices are posted) and
**no print dialog opens** — because opening 20 print dialogs in a
row would be unusable.

For batch workflows, Carla has two options:

#### Option A — Use the manual button per invoice

1. Carla opens invoice #1.
2. Clicks **Post**. Invoice state → "Posted". (No auto-print since
   multi-select? No — single record, but Carla would need to enable
   the invoice toggle to get auto-print.)
3. If invoice auto-print toggle is ON: print dialog opens
   automatically. Carla prints, closes, opens invoice #2.
4. Repeat for each invoice.

#### Option B — Use the standard batch flow + manual print

1. Carla multi-selects 20 invoices in list view.
2. Clicks **Post** in the action menu. All 20 invoices are posted.
3. Carla multi-selects the 20 posted invoices again.
4. Uses **Print → Invoices** in the action menu to generate a
   single PDF containing all 20 invoices.
5. Prints the combined PDF from the browser's PDF viewer.

**Recommendation:** For batch invoice posting, keep the auto-print
toggle OFF and use Option B. For single-invoice posting (the common
case for most accountants), turn the toggle ON and use Option A.

---

## Workflow 4 — Purchase manager approves a PO

**Persona:** David, a purchase manager.
**Goal:** Approve a purchase order and immediately print a copy
for the vendor file.

### With Direct Print Auto (PO toggle ON)

1. David opens the PO form (in "To Approve" state).
2. Clicks **Approve**. PO state → "Purchase Order".
3. Browser print dialog opens automatically.
4. David clicks **Print** to print a hard copy for the vendor file.

**Key benefit:** No need to remember to print after approving —
the system reminds you by opening the print dialog automatically.

---

## Workflow 5 — Reprinting a lost delivery slip

**Persona:** Bob (same as Workflow 2).
**Goal:** Re-print a delivery slip that was lost after the original
print.

### With Direct Print Auto (manual button — no auto-print)

1. Bob opens the done picking form (state = "Done").
2. The **Direct Print** button is still visible in the header
   (it's always visible per STEP 0).
3. Bob clicks **Direct Print**.
4. Browser print dialog opens with the delivery slip report.
5. Bob prints the replacement copy.

**Key benefit:** Even though the picking is already done (so
`button_validate` won't be called again), the manual button
provides on-demand printing for any state.

---

## Workflow 6 — Printing a draft quotation for a customer meeting

**Persona:** Anna (same as Workflow 1).
**Goal:** Print a draft quotation (not yet confirmed) to take to
an in-person customer meeting.

### With Direct Print Auto (manual button)

1. Anna opens the draft quotation.
2. Clicks **Direct Print** in the header.
3. Browser print dialog opens with the draft quotation report.
4. Anna prints it and takes it to the meeting.

**Key benefit:** Even though the quotation is in draft state (so
`action_confirm` hasn't run), the manual button provides on-demand
printing. No need to navigate to the Print dropdown menu.

---

## Workflow 7 — Auditor prints a cancelled invoice

**Persona:** Erin, an external auditor.
**Goal:** Print a copy of a cancelled invoice for the audit trail.

### With Direct Print Auto (manual button)

1. Erin (with Direct Print User group) opens the cancelled invoice.
2. Clicks **Direct Print** in the header.
3. Browser print dialog opens with the cancelled invoice report
   (which shows the cancelled state and any cancellation reasons).
4. Erin prints it for the audit file.

**Key benefit:** The manual button works in any state, including
cancelled. This is important for auditors who need to print
historical records.
