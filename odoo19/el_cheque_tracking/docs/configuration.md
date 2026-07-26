# Configuration Guide — el_cheque_tracking

## Prerequisites

1. Odoo 19 installed and running.
2. A chart of accounts configured (the `account` module's demo data works
   for testing; for production, install your country's localization).
3. At least one bank journal configured (Settings → Accounting → Journals).
4. The `el_cheque_tracking` module installed.

## Step 1: Configure company cheque accounts

1. Go to **Settings → Accounting → EL Cheque Tracking**.
2. Under **Cheque Accounts**, set:
   - **Cheques Received Account** — a current-asset account (e.g. 101100)
   - **Cheques Under Collection Account** — a current-asset account (e.g. 101200)
   - **Cheques Issued Account** — a current-liability account (e.g. 201100)
   - **Cheque Penalty Income Account** — an income account (e.g. 401100)
   - **Cheque Bank Charges Account** — an expense account (e.g. 501100)
3. Click **Save**.

## Step 2: Configure lifecycle rules

Under **Cheque Lifecycle Rules**, set:
- **Stale Cheque Months** — e.g. 6 (a received cheque is stale after 6 months)
- **PDC Reminder Days** — e.g. 7 (remind 7 days before a PDC matures)
- **Max Re-deposit Attempts** — e.g. 2 (max re-deposits for a returned cheque)
- **High-value Approval Threshold** — e.g. 50000.0 (issued cheques above this
  amount schedule an approval activity)

Click **Save**.

## Step 3: Verify security groups

1. Go to **Settings → Users → Groups**.
2. Search for "Cheque".
3. Verify the three groups exist:
   - **Cheque User** — create and track cheques
   - **Cheque Manager** — approve, re-deposit, void
   - **Cheque Administrator** — full access
4. Assign users to the appropriate groups.

## Step 4: Verify return reasons

1. Go to **Cheque Tracking → Configuration → Return Reasons**.
2. Verify the 4 default reasons exist: NSF, Stale, Damaged, Other.
3. Add custom reasons as needed (set a default penalty if applicable).

## Step 5: Verify cron jobs

1. Go to **Settings → Technical → Automation → Scheduled Actions**.
2. Search for "Cheque".
3. Verify the two cron jobs:
   - **Cheque: PDC Maturity Reminder** — daily
   - **Cheque: Stale Cheque Detection** — daily
4. Click **Run Manually** to test, or wait for the next scheduled run.

## Step 6: Verify multi-company (if applicable)

1. Go to **Settings → Users → Companies**.
2. For each company, repeat Step 1 (each company has its own cheque accounts).
3. Verify users with multi-company access can see cheques across companies;
   users without multi-company access see only their own company's cheques.
