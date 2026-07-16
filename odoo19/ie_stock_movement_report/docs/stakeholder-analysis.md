# Stakeholder Analysis — ie_stock_movement_report

## Module Purpose

A PDF report of inventory movements per product with opening/closing balance
and running value. Designed for inventory controllers, warehouse managers,
and accountants.

## Stakeholder Matrix

| # | Name/Title                    | Role          | Influence | Impact | Attitude   | Engagement                  |
|---|-------------------------------|---------------|-----------|--------|------------|-----------------------------|
| 1 | Inventory Manager (Sponsor)   | Sponsor       | High      | High   | Supportive | Demo at end, sign-off       |
| 2 | Warehouse Supervisor          | Champion      | High      | High   | Supportive | Co-design filters, UAT      |
| 3 | Inventory Controller (Key User) | Key User    | Medium    | High   | Neutral    | Training + daily-use feedback |
| 4 | Accountant                    | Key User      | Medium    | Medium | Supportive | Verify valuation figures    |
| 5 | End Users (5-10 controllers)  | End User      | Low       | High   | Unknown    | Training + announce         |
| 6 | IT Admin / Odoo Functional    | IT Admin      | Medium    | Low    | Supportive | Receive technical docs      |
| 7 | Auditor (External)            | External      | Low       | Medium | Neutral    | Read-only access to report  |

## Key Concerns to Address

- **Inventory Manager:** Performance with thousands of movements — must not
  time out the web client.
- **Warehouse Supervisor:** Scope filtering (warehouse/location) must be
  intuitive; results must match physical counts.
- **Inventory Controller:** Layout must be printable A4 Landscape; numbers
  must align for manual reconciliation.
- **Accountant:** Unit cost must come from `standard_price` (not FIFO/LIFO
  which is Enterprise); valuation must be reproducible.
- **Auditor:** Opening balance must be traceable to specific move lines.

## User Roles → Security Groups Mapping

| Stakeholder                  | Security Group                          | Permissions       |
|------------------------------|-----------------------------------------|-------------------|
| Inventory Controller / End User | group_stock_movement_report_user     | run report (read) |
| Inventory Manager            | group_stock_movement_report_manager    | run + manage      |

## Influence vs Impact Matrix

```
              HIGH IMPACT
                  |
    Manage        |    Engage Closely
    Closely       |    (Manager, Supervisor, Controller)
    (IT Admin)    |
LOW  ─────────────+──────────── HIGH
INFLUENCE         |
                  |
    Keep          |    Monitor
    Informed      |    (End Users, Accountant, Auditor)
    (Auditor)     |
                  |
              LOW IMPACT
```
