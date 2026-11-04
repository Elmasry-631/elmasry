# Stakeholder Analysis — el_prevent_negative_stock

## Stakeholder Matrix

| # | Name/Title | Role | Influence | Impact | Attitude | Engagement |
|---|-----------|------|-----------|--------|----------|------------|
| 1 | Warehouse Manager | Champion | High | High | Supportive | Weekly demo |
| 2 | Warehouse User | Key User | Medium | High | Neutral | Training + feedback |
| 3 | IT Admin | IT Admin | Medium | Medium | Supportive | Technical docs |
| 4 | End Users (5) | End User | Low | High | Unknown | Training + announce |

## Key Concerns to Address
- Warehouse users need clear error messages when stock is insufficient
- Manager needs visibility into rejected attempts (via alerts log)
- All users need to understand that NO exceptions are allowed

## User Roles → Security Groups Mapping
| Stakeholder | Security Group | Permissions |
|-------------|---------------|-------------|
| Warehouse User | stock.group_stock_user | Read alerts |
| Warehouse Manager | stock.group_stock_manager | Read all alerts + config |
