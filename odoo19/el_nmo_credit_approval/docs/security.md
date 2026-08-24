# Security Documentation

## Security Groups

The module defines three hierarchical security groups under the "Sales" category:

### 1. Credit Approval — Salesperson (`group_credit_approval_salesperson`)
- **Implies:** `sales_team.group_sale_salesman` (base salesperson group)
- **Purpose:** Salespeople who create approval requests when their orders are blocked
- **Access:**
  - `credit.approval.request`: Read, Create (no write, no unlink)
  - `credit.rejection.reason`: Read only

### 2. Credit Approval — Supervisor (`group_credit_approval_supervisor`)
- **Implies:** `group_credit_approval_salesperson` (inherits salesperson access)
- **Purpose:** Team leaders who review and approve/reject credit requests
- **Access:**
  - `credit.approval.request`: Read, Write (can approve/reject, cannot create or delete)
  - `credit.rejection.reason`: Read only (can see reasons, cannot manage them)

### 3. Credit Approval — Manager (`group_credit_approval_manager`)
- **Implies:** `sales_team.group_sale_manager` (base sales manager group)
- **Purpose:** Full administrative access including managing rejection reasons
- **Access:**
  - `credit.approval.request`: Full CRUD (read, write, create, unlink)
  - `credit.rejection.reason`: Full CRUD (can add, edit, deactivate, and delete reasons)

## Access Rights Matrix

| Model | Salesperson | Supervisor | Manager |
|-------|:-----------:|:----------:|:-------:|
| `credit.approval.request` | R, C | R, W | R, W, C, U |
| `credit.rejection.reason` | R | R | R, W, C, U |

R = Read, W = Write, C = Create, U = Unlink

## Design Decisions

**Why can salespersons create but not write?** The approval request is created automatically by the system when a sale order is blocked. The salesperson should be able to view their requests and see the status, but should not be able to manually change the state or modify credit details after submission.

**Why can supervisors write but not create?** Supervisors should only approve or reject existing requests. They should not be able to create fake approval requests. The write permission allows them to set the `rejection_reason_id` and trigger the state change via the button methods.

**Why are rejection reasons manager-only for management?** The set of rejection reasons is a configuration that should be controlled centrally. Allowing supervisors or salespersons to add reasons would lead to inconsistency and potential misuse (e.g., creating vague reasons to avoid accountability).

## Record Rules

No explicit record rules are defined in this version. Access is controlled purely through group-based read/write permissions. The module relies on the Odoo default behavior where users can see records they have access to based on their group membership. If multi-company isolation is needed in the future, a record rule on `company_id` should be added.

## Menu Visibility

The "Rejection Reasons" menu item is only visible to users in the `group_credit_approval_manager` group, preventing non-managers from accessing the configuration. The "Approval Requests" menu is visible to all users in any of the three groups.