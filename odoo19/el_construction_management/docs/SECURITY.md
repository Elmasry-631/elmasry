# Security & Governance

## Principles
- Least privilege.
- Company consistency.
- Controlled workflow transitions.
- Separation of duties for approvals.
- Finalized records are protected from arbitrary edits.

## Manager controls
Manager-only operations include approval governance and selected hardening/repair actions.

## Inventory security
Construction stock operations rely on Odoo Inventory permissions. A user must have the underlying stock permissions required to validate the generated stock document.

## Auditability
Business changes should be made through workflow buttons and controlled revisions rather than direct state edits or manual database changes.
