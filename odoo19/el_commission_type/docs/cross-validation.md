# Cross-Validation - el_commission_type

## Status: PASSED

### Model Fields vs View Fields
- [x] name - Present in model and views
- [x] team_member_type - Present in model and views
- [x] commission_percentage - Present in model and views
- [x] company_id - Present in model and views

### Manifest data[] vs Disk Files
- [x] security/security.xml - Exists
- [x] security/ir.model.access.csv - Exists
- [x] views/commission_type_views.xml - Exists
- [x] views/menu.xml - Exists

### __init__.py Chain
- [x] __init__.py imports models
- [x] models/__init__.py imports commission_type

### Odoo 19 Compatibility
- [x] Using <list> instead of <tree>
- [x] Using <chatter/> instead of oe_chatter div
- [x] Using @api.constrains instead of _sql_constraints