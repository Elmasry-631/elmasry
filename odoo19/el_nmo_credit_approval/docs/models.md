# Models Documentation

## credit.approval.request

This is the core model that manages the approval workflow for credit-limit-exceeded sale orders. It inherits `mail.thread` and `mail.activity.mixin` for full chatter and activity support.

### State Machine

The model follows a strict state machine with five possible states:

| State | Description | Allowed Transitions |
|-------|-------------|-------------------|
| `draft` | Initial state, request being prepared | submitted, cancelled |
| `submitted` | Sent to supervisor for review | approved, rejected, cancelled |
| `approved` | Supervisor approved, SO confirmed | — |
| `rejected` | Supervisor rejected with reason | draft (resubmit) |
| `cancelled` | Request cancelled by user | — |

### Key Fields

**Identification:** `name` (auto-generated sequence CR/00001), `display_name` (computed from name + SO name).

**Relations:** `sale_order_id` (cascade delete), `partner_id` (customer snapshot), `requested_by` (salesperson), `supervisor_id` (approver), `rejection_reason_id` (Many2one to predefined reasons).

**Credit Snapshot:** `credit_limit`, `credit_used`, `order_amount`, `exceeded_by`, `currency_id` — all captured at request creation time for audit purposes. These are readonly to preserve the exact values that triggered the approval.

**Rejection:** `rejection_reason_id` is a Many2one to `credit.rejection.reason` (required before rejecting). `rejection_notes` provides optional free-text context. `approval_date` records when the decision was made.

### Key Methods

- `action_submit()`: Transitions draft to submitted, sends email/notification to supervisor, logs on both the request and the sale order chatter.
- `action_approve()`: Transitions submitted to approved, sets credit_approval_state on SO, then calls `action_confirm()` on the SO with a `credit_approval_bypass` context key to skip the credit check.
- `action_reject()`: Requires `rejection_reason_id` to be set (raises ValidationError otherwise). Transitions to rejected, logs the reason.
- `action_cancel()`: Cancels draft or submitted requests, clears the SO approval state.
- `action_resubmit()`: Resets a rejected request back to draft, clears rejection data.
- `_create_from_sale_order(sale_order)`: Factory class method that creates and submits a request. Computes the credit snapshot and discovers the supervisor.
- `_get_supervisor(salesperson)`: Looks up the sales team leader first, then falls back to the user's parent.

## credit.rejection.reason

A simple configuration model storing predefined rejection reasons that supervisors select from when rejecting credit approval requests.

### Fields

- `name` (Char, required, translatable): The reason text displayed in the dropdown.
- `description` (Text): Detailed explanation of when to use this reason.
- `sequence` (Integer): Sort order for the selection list.
- `active` (Boolean): Soft-delete — inactive reasons are hidden from selection.
- `company_id` (Many2one, required): Each reason is company-scoped. A unique constraint ensures no duplicate names per company.

The model ships with 8 default reasons (in `data/default_rejection_reasons.xml` with `noupdate="1"`): Insufficient Payment History, Overdue Payments, Credit Limit Exceeded, High Risk Customer, Classification Pending Downgrade, Management Decision, Incomplete Documents, and Other.

## sale.order (Extended)

The module extends `sale.order` with three fields to track the approval workflow:

- `credit_approval_id` (Many2one): Links to the active approval request. Cleared when the request is cancelled.
- `credit_approval_state` (Selection): Tracks the workflow status — none, pending, approved, or rejected. Displayed as a color-coded badge on the SO form.
- `is_credit_blocked` (Boolean, computed, stored): True when the SO is in draft state, the customer is credit with block policy, and the projected total exceeds the credit limit (and not yet approved). Used to control the visibility of alert banners.

### action_confirm Override

The `action_confirm()` method is overridden to intercept credit blocks. Instead of raising a UserError (as the parent `el_nmo_classification` module does), it creates a Credit Approval Request. The override checks for `credit_approval_bypass` in the context to avoid infinite loops after approval. For "warning" policy customers, it posts a chatter message but allows confirmation to proceed.