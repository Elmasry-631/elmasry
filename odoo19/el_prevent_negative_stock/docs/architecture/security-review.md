# Security Review — el_prevent_negative_stock

## User Groups
| Group | Stakeholder | Permissions |
|-------|-------------|-------------|
| group_alert_user | Warehouse User | Read alerts |
| group_alert_manager | Warehouse Manager | Read/Create/Write/Delete alerts |

## Access Rights
| Model | User | Manager | System |
|-------|------|---------|--------|
| el.stock.alert | R | RWCD | RWCD |

## Record Rules
None needed — the alert model is read-only for users (create="false" in form).

## Key Security Notes
- The _action_done override runs for ALL users including admin
- NO group-based bypass — this is a hard business rule
- Even users with stock.group_stock_manager cannot override
- Alert records are created programmatically (not by user)
- Only managers can delete alert records (for cleanup)

## Field-Level Security
No restricted fields — all fields are readonly in views.
