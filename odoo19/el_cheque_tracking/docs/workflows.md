# Workflows — el_cheque_tracking

## Workflow 1: Receive a cheque from a customer

1. Customer hands you a cheque for an invoice.
2. Go to **Cheque Tracking → Received → Received Cheques → New**.
3. Fill in:
   - Cheque Type: Received
   - Cheque Number: (from the physical cheque)
   - Cheque Date: (date written on the cheque)
   - Due Date: (post-dated? set the future date)
   - Amount: (cheque amount)
   - Partner: (the customer)
   - Bank: (the bank on the cheque)
   - Deposit / Drawee Bank Journal: (your bank account for deposit)
4. (Optional) Link invoices via the "Invoices / Bills" tab.
5. Save.
6. Click **Receive** → state moves to **Holding** + a receipt entry is posted.
7. (If post-dated) Wait until the due date.

## Workflow 2: Deposit cheques in batch

1. Go to **Cheque Tracking → Received → Received Cheques**.
2. Select multiple cheques in **Holding** state (use the list view checkboxes).
3. From the action menu, choose **Batch Deposit**.
4. In the wizard, select the bank journal + deposit date.
5. Click **Create Deposit** → a `cheque.deposit` is created + confirmed.
6. Each cheque moves to **Deposited** state + a deposit entry is posted.
7. Print the deposit slip from the deposit form (Print Deposit Slip button).

## Workflow 3: Clear a deposited cheque

1. Bank confirms the cheque has cleared.
2. Go to **Cheque Tracking → Received → Received Cheques**.
3. Open the deposited cheque.
4. Click **Clear** → state moves to **Cleared** + a clearance entry is posted.

## Workflow 4: Return a bounced cheque

1. Bank notifies you that a deposited cheque bounced (NSF).
2. Open the deposited cheque.
3. Click **Return** → the return wizard opens.
4. Select the return reason (e.g. NSF).
5. (Optional) Enter bank charges + penalty amount.
6. Click **Submit Return** → state moves to **Returned** + a reversal entry
   is posted + optional charges/penalty entries.
7. A follow-up activity is scheduled on the cheque.
8. (Optional) Re-deposit the cheque via Workflow 2 (max-attempt validated).

## Workflow 5: Issue a cheque to a vendor

1. You need to pay a vendor by cheque.
2. Go to **Cheque Tracking → Issued → Issued Cheques → New**.
3. Fill in:
   - Cheque Type: Issued
   - Cheque Number: (from your chequebook)
   - Cheque Date, Due Date, Amount, Partner (vendor), Bank, Deposit Journal.
4. Save.
5. Click **Approve** → state moves to **Approved** + an issue entry is posted
   (Dr Payable / Cr Cheques Issued).
6. (If high-value) An approval activity is scheduled.

## Workflow 6: Hand over + cash an issued cheque

1. Physically hand the cheque to the vendor.
2. Open the approved issued cheque.
3. Click **Hand Over** → state moves to **Handed Over** (no entry, just
   records `handover_date` + `handover_recipient`).
4. Vendor cashes the cheque at their bank.
5. Your bank confirms the cheque was cashed.
6. Open the handed-over cheque.
7. Click **Cash** → state moves to **Cashed** + a cashing entry is posted
   (Dr Cheques Issued / Cr Bank).

## Workflow 7: Void an issued cheque

1. An issued cheque was written but never cashed (or was lost).
2. Open the issued cheque (must be in draft, approved, or handed_over state).
3. Click **Void** → state moves to **Void** + any posted entries are reversed.
