# El-Nmo Credit Limit Approval Workflow

> Odoo 19 module that replaces hard credit limit blocks with an approval workflow, allowing supervisors to authorize sale orders that exceed customer credit limits.

## Overview

When a salesperson tries to confirm a sale order for a credit customer whose credit policy is "Block Sale" and whose credit limit has been exceeded, instead of raising a hard error (as the base `el_nmo_classification` module does), this module automatically creates an **approval request** and routes it to the sales supervisor. The supervisor can then **approve** (which confirms the sale order) or **reject** (selecting a predefined reason from the `credit.rejection.reason` model).

## Dependencies

- `el_nmo_classification` (Customer Classification with credit limits and policies)
- `sale` (Sale Orders)
- `mail` (Chatter and notifications)

## How It Works

### Flow Diagram

```
Salesperson clicks "Confirm" on Sale Order
    |
    v
Is customer payment_type = credit?
    |-- No  --> Confirm normally
    |
    Yes
    |
    v
Is credit_policy = "block"?
    |-- No (warning) --> Post warning, confirm normally
    |
    Yes
    |
    v
Is credit limit exceeded? (outstanding + order > limit)
    |-- No  --> Confirm normally
    |
    Yes
    |
    v
Create Credit Approval Request --> Notify Supervisor
    |
    v
Supervisor Reviews
    |
    +---> Approve  --> SO confirms automatically
    |
    +---> Reject (must select reason) --> SO stays blocked
              |
              v
         Salesperson can Resubmit (after fixing)
```

### Credit Check Logic

The check evaluates three conditions, all of which must be true for a block:
1. `partner.payment_type == 'credit'`
2. `partner.credit_policy == 'block'`
3. `partner.credit + order.amount_total > partner.effective_credit_limit`

### Supervisor Discovery

The module looks for the supervisor in this order:
1. Sales team leader (`crm.team.user_id`) of the salesperson's team
2. User's parent (`user.parent_id`)
3. Falls back to the current user

## Models

### credit.approval.request

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | Auto-generated reference (CR/00001) |
| `sale_order_id` | Many2one | Related sale order |
| `partner_id` | Many2one | Customer |
| `requested_by` | Many2one | Salesperson who created the request |
| `supervisor_id` | Many2one | Supervisor to approve/reject |
| `state` | Selection | draft / submitted / approved / rejected / cancelled |
| `credit_limit` | Float | Snapshot of customer credit limit |
| `credit_used` | Float | Snapshot of outstanding balance |
| `order_amount` | Monetary | Sale order total |
| `exceeded_by` | Float | How much the limit was exceeded |
| `rejection_reason_id` | Many2one | Predefined rejection reason |
| `rejection_notes` | Text | Optional additional notes |

### credit.rejection.reason

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char (translatable) | Reason text displayed in selection |
| `description` | Text | Detailed explanation |
| `sequence` | Integer | Sort order |
| `active` | Boolean | Can be disabled without deleting |
| `company_id` | Many2one | Company scoping |

### sale.order (extended)

| Field | Type | Description |
|-------|------|-------------|
| `credit_approval_id` | Many2one | Linked approval request |
| `credit_approval_state` | Selection | none / pending / approved / rejected |
| `is_credit_blocked` | Boolean (computed) | Whether the order is currently credit-blocked |

## Default Rejection Reasons

The module ships with 8 predefined reasons:
1. Insufficient Payment History
2. Overdue Payments
3. Credit Limit Exceeded
4. High Risk Customer
5. Classification Pending Downgrade
6. Management Decision
7. Incomplete Documents
8. Other

Managers can add, edit, or deactivate reasons from Settings > Credit Approval > Rejection Reasons.

## Security Groups

| Group | Can Do |
|-------|--------|
| Credit Approval - Salesperson | Create requests, view all |
| Credit Approval - Supervisor | Approve/reject requests |
| Credit Approval - Manager | Full access + manage rejection reasons |

## Installation

1. Install `el_nmo_classification` first
2. Copy this module to your Odoo addons directory
3. Update apps list and install "El-Nmo - Credit Limit Approval Workflow"

## Configuration

1. Go to Sales > Configuration > Credit Approval > Rejection Reasons
2. Review and customize the predefined rejection reasons
3. Assign users to the appropriate security groups
4. Ensure sales team leaders are configured (used for supervisor lookup)

## Testing

```bash
# Run the module tests
odoo --test-enable --test-tags=/el_nmo_credit_approval \
    -i el_nmo_credit_approval --stop-after-init -d test_db
```

## Author

**Ibrahim Elmasry** - Senior Odoo Developer + DevOps + Implementation Consultant