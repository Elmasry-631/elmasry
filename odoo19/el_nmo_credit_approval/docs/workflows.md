# Workflows Documentation

## Credit Approval Workflow

### Step 1: Salesperson Creates/Confirms Sale Order

The workflow is triggered when a salesperson clicks the "Confirm" button on a sale order. The system evaluates three conditions in sequence:

1. **Payment Type Check**: Is the customer's `payment_type` equal to 'credit'? If no → confirm normally.
2. **Credit Policy Check**: Does the customer's classification have `credit_policy` equal to 'block'? If no (or no classification) → either warn (if 'warning' policy) or confirm normally.
3. **Credit Limit Check**: Is `partner.credit + order.amount_total > partner.effective_credit_limit`? If no → confirm normally.

If all three conditions are true, the order is credit-blocked.

### Step 2: Approval Request Creation

When the block is detected, the system automatically:
1. Checks if there's already a pending approval request for this SO (prevents duplicates)
2. If an existing request exists → raises UserError telling the salesperson to wait
3. If no existing request → calls `CreditApprovalRequest._create_from_sale_order(order)`
4. The factory method captures a snapshot of all credit values (limit, used, exceeded)
5. Discovers the supervisor via sales team → user parent → current user
6. Creates the request record and immediately submits it

### Step 3: Supervisor Notification

On submission, the system:
1. Sends an HTML email to the supervisor via `mail.template` with a credit details table
2. Posts a message on the approval request's chatter
3. Posts a message on the sale order's chatter linking to the approval request
4. The supervisor sees the request in the "To Approve" filter (default search filter)

### Step 4: Supervisor Reviews

The supervisor opens the request and sees:
- Full credit details (limit, used, order amount, exceeded by)
- A link to the original sale order
- The customer's name and the salesperson who created the request
- Two action buttons: Approve (green) and Reject (red)

### Step 5a: Approval Path

When the supervisor clicks "Approve":
1. Request state changes to 'approved'
2. `approval_date` is set to current datetime
3. A message is posted on the approval request chatter
4. Sale order's `credit_approval_state` is set to 'approved'
5. A message is posted on the sale order chatter with approval details
6. The sale order's `action_confirm()` is called with `credit_approval_bypass=True` context
7. The bypass context causes the credit check to be skipped, and `super().action_confirm()` runs
8. The sale order transitions to 'sales_order' or 'sale' state normally

### Step 5b: Rejection Path

When the supervisor clicks "Reject":
1. System validates that `rejection_reason_id` is set (raises `ValidationError` if not)
2. Request state changes to 'rejected'
3. `approval_date` is set to current datetime
4. The rejection reason name and optional notes are recorded
5. Messages are posted on both the approval request and sale order chatters
6. Sale order's `credit_approval_state` is set to 'rejected'
7. The sale order stays in 'draft' state — the salesperson cannot confirm it

### Step 6: Resubmission (Optional)

After rejection, the salesperson can:
1. Review the rejection reason on the SO or approval request
2. Optionally adjust the order (reduce quantity, change payment terms, etc.)
3. Click "Resubmit" on the approval request
4. The request resets to 'draft' state, rejection data is cleared
5. The salesperson clicks "Submit" to send it back to the supervisor
6. A new notification is sent

### Step 7: Cancellation

Either the salesperson or supervisor can cancel a request that is in 'draft' or 'submitted' state:
1. Request state changes to 'cancelled'
2. Sale order's `credit_approval_state` resets to 'none'
3. The `credit_approval_id` is cleared
4. A message is posted on the request chatter

## Notification Flow Diagram

```
[Salesperson confirms SO]
        |
        v
[Credit check: exceeded + block]
        |
        v
[Create Approval Request]
        |
        v
[Email to Supervisor] + [Chatter on SO] + [Chatter on Request]
        |
        v
[Supervisor opens Request]
        |
   +----+----+
   |         |
[Approve] [Reject]
   |         |
   v         v
[SO Confirmed] [SO Stays Draft]
[Email/Chatter] [Reason recorded]
                [Email/Chatter]