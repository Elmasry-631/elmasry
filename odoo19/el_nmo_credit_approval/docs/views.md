# Views Documentation

## credit.rejection.reason Views

### List View (`view_credit_rejection_reason_list`)
- Displays: sequence (drag handle), name, description (optional), company (multi-company only), active (boolean toggle)
- Decoration: `decoration-danger="not active"` — inactive reasons appear with a red stripe
- The boolean toggle widget allows managers to quickly activate/deactivate reasons without opening the form

### Form View (`view_credit_rejection_reason_form`)
- Clean form with a title field, sequence number, company selector, and active toggle
- Description field in a separate group for better visual hierarchy
- Uses `<sheet>` and `<group>` layout per Odoo UI design patterns

### Search View (`view_credit_rejection_reason_search`)
- Search by name field
- Filters: Active, Inactive

## credit.approval.request Views

### List View (`view_credit_approval_request_list`)
- Color-coded rows based on state: success for approved, danger for rejected, warning for submitted, muted for cancelled
- Fields: name, sale order, customer, requested by, supervisor, credit details (optional), rejection reason (optional), state badge
- The `exceeded_by` field uses `decoration-danger` to highlight the overage amount in red
- State field uses the `badge` widget with matching decorations for quick visual scanning

### Form View (`view_credit_approval_request_form`)
- **Header**: Status bar with context-sensitive buttons (Submit, Approve, Reject, Resubmit, Cancel). The Approve/Reject buttons are only visible to supervisors via `groups=` attribute.
- **Request Info group**: Sale order link, customer, requested by, supervisor, company
- **Credit Details group**: Credit limit, credit used, order amount, exceeded by (red decoration)
- **Rejection Details group**: Only visible when state is submitted or rejected. Contains the `rejection_reason_id` Many2one dropdown and optional `rejection_notes` text field. The rejection reason is `required` when state is submitted.
- **Approval Date**: Shown only for approved or rejected requests
- **Chatter**: Full mail.thread chatter at the bottom for audit trail

### Search View (`view_credit_approval_request_search`)
- Search by: name, sale order, customer, requested by, supervisor
- Filters: Draft, Submitted, Approved, Rejected, My Requests (requested_by = uid), To Approve (supervisor_id = uid AND state = submitted)
- Default context: `search_default_filter_to_approve=1` — supervisors see pending requests first
- Group by: Status, Supervisor, Customer

## sale.order View Extensions

### Form View Extension (`view_sale_order_form_credit_approval`)
Three alert banners are injected before the button box area:

1. **Yellow warning** (`alert-warning`): Shown when `is_credit_blocked=True` and not approved. Displays "Credit Limit Exceeded — Approval Pending" with a link to the approval request.

2. **Green success** (`alert-success`): Shown when `credit_approval_state='approved'`. Confirms the order has been approved for exceeding the credit limit, with a link to view the approval.

3. **Red danger** (`alert-danger`): Shown when `credit_approval_state='rejected'`. Informs the salesperson the order was rejected, with a link to view the request.

Additionally, a `credit_approval_state` badge widget is inserted before the `state` field in the header, providing at-a-glance status visibility without scrolling.

### List View Extension (`view_sale_order_list_credit_approval`)
- Adds `credit_approval_state` as a color-coded badge after the `state` column (optional, shown by default)
- Uses decoration-info for pending, decoration-success for approved, decoration-danger for rejected

### Search View Extension (`view_sale_order_search_credit_approval`)
- Three new filters: Credit Pending, Credit Approved, Credit Rejected
- Placed after the "My Orders" filter for easy access

## Menu Structure

```
Sales > Configuration > Credit Approval
    ├── Approval Requests     (all users in credit groups)
    └── Rejection Reasons     (managers only)
```