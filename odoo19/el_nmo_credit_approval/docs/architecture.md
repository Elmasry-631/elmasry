# Architecture Documentation

## Module Overview

`el_nmo_credit_approval` is an Odoo 19 module that transforms the hard credit limit block (implemented in `el_nmo_classification`) into a flexible approval workflow. It follows the Odoo extension pattern by inheriting existing models and overriding key methods.

## Dependency Chain

```
base → mail → sale → el_nmo_classification → el_nmo_credit_approval
```

The module depends on `el_nmo_classification` because it needs access to:
- `partner.payment_type` (cash/credit)
- `partner.credit_policy` (block/warning)
- `partner.effective_credit_limit` (the computed credit limit)
- `partner.credit` (the outstanding balance from Odoo's base accounting)
- `partner.classification_id` (the customer classification reference)

## Design Patterns

### Override Pattern (sale.order.action_confirm)

The most critical architectural decision is how the module intercepts the credit block. The `el_nmo_classification` module's `sale.order.action_confirm()` raises a `UserError` when credit is exceeded with block policy. This module overrides `action_confirm()` with the same logic but replaces the `UserError` with an approval request creation.

To handle the post-approval confirmation (where the SO should no longer be blocked), the module uses a context key: `credit_approval_bypass=True`. When the supervisor approves, the module calls `sale_order.with_context(credit_approval_bypass=True).action_confirm()`, which skips the credit check and delegates to `super().action_confirm()`.

### Factory Method Pattern (_create_from_sale_order)

The `CreditApprovalRequest._create_from_sale_order()` class method encapsulates the entire creation logic: computing credit snapshots, discovering the supervisor, creating the record, and submitting it. This keeps the `action_confirm()` override clean and focused on the decision logic.

### Supervisor Discovery Strategy

The `_get_supervisor()` method implements a fallback chain:
1. **Sales Team Leader**: Searches `crm.team.member` for the salesperson's team, then checks if the team has a `user_id` (team leader).
2. **User Parent**: Falls back to `salesperson.parent_id` (the Odoo "Manager" field on the user form).
3. **Current User**: If no supervisor is found, the current user is used as a last resort to avoid empty required fields.

### Notification System

The module uses Odoo's `mail.template` for supervisor notifications. The template sends a formatted HTML email with a table showing all credit details. If the template is not found (e.g., deleted by a user), the system falls back to posting a chatter message and sending a partner notification.

## Data Flow

```
1. User clicks "Confirm" on SO
2. action_confirm() checks credit conditions
3. If blocked → _create_from_sale_order(so) called
4. Factory creates credit.approval.request record
5. Factory calls action_submit()
6. action_submit() writes state='submitted'
7. action_submit() sends email to supervisor via mail.template
8. action_submit() posts message on SO chatter
9. Supervisor opens the request (filtered by "To Approve")
10. Supervisor clicks Approve OR selects rejection_reason_id and clicks Reject
11a. Approve → state='approved', SO.confirmed via bypass context
11b. Reject → state='rejected', rejection_reason_id recorded, SO stays draft
```

## State Machine Design

The `credit.approval.request` model uses a Selection field for state management rather than Odoo's `mail.thread` state tracking. This is intentional because the state transitions are guarded by business logic in Python methods (`action_approve`, `action_reject`, etc.), not by XML buttons alone. Each method validates the current state before transitioning, preventing invalid state changes even if the UI is bypassed via RPC.