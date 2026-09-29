# Changelog

## 19.0.1.24.0

- Hardened workflow record creation against injected final states.
- Removed Workflow Mixin from Odoo model extension classes to avoid registry `__bases__` layout conflicts.
- Added complete BOQ workflow actions and immutable finalized BOQ/line behavior.
- Fixed Variation Order approval/rejection ordering and protected the approval ledger.
- Added multi-company record rules for approval/revision records.
- Added revision-line create guards and finalized snapshot protection.
- Serialized project/sub-project closeout checks.
- Linked material issues to stock pickings/scraps and tightened MREQ quantity/UoM controls.
- Prevented Progress Billing completion with cancelled invoices.
- Blocked Work Order completion when Quality Check is in recheck.
- Hardened Quality Check evidence and check-point immutability after results.
- Expanded dashboard status coverage and bounded filter loading.
- Removed generated Python bytecode from the distribution package.

## 19.0.1.23.0 — Architectural Refactor

- Split the former `construction_controls.py` God File into domain-specific control modules.
- Hardened project stock-location identity: mismatched existing locations now fail instead of silently creating replacements.
- Batched cost snapshot idempotency checks to reduce repeated database queries.
- Added revision-number row locking for BOQ/Budget revisions.
- Restricted Approval Matrix configuration to the approval workflow actually wired to the approval ledger (Variation Order) instead of advertising unsupported models.
- Kept runtime certification explicitly pending until an Odoo 19 staging install/upgrade and UAT run.

# Changelog

## Historical release 19.0.1.21.0
- Fixed Progress Billing invoice count compute reference causing RPC/Owl errors during form onchange.
- Consolidated user-facing navigation into a shallow business-oriented menu hierarchy.
- Replaced the long report menu tree with a single Report Center entry point.
- Reorganized Configuration, Project Controls, Quality, Procurement, Planning, and Commercial navigation.
- Added upgrade-safe deactivation records for legacy navigation entries.
- Added semantic form section organization and a dedicated lightweight form UX asset.
- Reorganized module documentation into `docs/` and added a complete User Guide, Administration Guide, Workflows, Inventory, Reporting, Architecture, and Security documentation.
