# Security Design — ie_stock_movement_report

## 1. User Groups (mapped from stakeholder analysis)

| Group                                | Stakeholders                  | Implies                |
|--------------------------------------|-------------------------------|------------------------|
| group_stock_movement_report_user     | Inventory Controller, End Users | stock.group_stock_user |
| group_stock_movement_report_manager  | Inventory Manager              | group_stock_movement_report_user |

## 2. Access Rights (ir.model.access.csv)

| Model                              | User Group  | R | W | C | D |
|------------------------------------|-------------|---|---|---|---|
| stock.movement.report.wizard       | User        | 1 | 1 | 1 | 0 |
| stock.movement.report.wizard       | Manager     | 1 | 1 | 1 | 1 |

**Notes:**
- Abstract models (`stock.movement.report`, `stock.movement.report.handler`) need NO ACL
  (they have no DB table)
- User can create wizards (run report) but cannot delete (auto-cleaned by Odoo cron)
- Manager can delete (cleanup of stuck wizards)

## 3. Record Rules

**Not applicable** — this module has no persisted business records with
multi-company or personal-record isolation needs. The wizard is transient
and visible only to its creator during the session.

## 4. Field-Level Security

**Not applicable** — all wizard fields are non-sensitive (dates, filter refs).
No salary, no personal data, no internal notes.

## 5. Workflow Security

**Not applicable** — wizard has no state machine, no approval flow, no
buttons restricted by group. The "Print PDF" button is visible to any
user in the User or Manager group (both inherit stock.group_stock_user).

## Security Checklist

- [x] Every persisted model has at least one access rule (wizard only)
- [x] No model is world-readable (no `base.group_user` for wizard)
- [x] Delete (unlink) is restricted — only manager
- [x] Transient model has full access for relevant groups
- [x] Multi-company rule not needed (no company_id field on wizard)
- [x] Personal-record rule not needed (wizard is session-scoped)
- [x] No sensitive fields to restrict
- [x] No workflow state transitions to gate

## Odoo 19 Compliance

- [x] Uses `ir.module.privilege` (not `ir.module.category`) per LAW 11/14
- [x] No `category_id` on `res.groups` (E-VER-020 — removed in Odoo 18+)
- [x] `implied_ids` uses standard `(4, ref(...))` syntax
