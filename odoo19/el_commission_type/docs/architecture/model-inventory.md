# Model Inventory - el_commission_type

## Models

### sales.commission.type
- **Type:** Main Model
- **Table:** sales_commission_type
- **Inherits:** mail.thread, mail.activity.mixin (for chatter)

#### Fields Inventory
| Field | Type | Attributes | Description |
|-------|------|------------|-------------|
| name | Char | compute, store, readonly | Auto-generated commission name |
| team_member_type | Selection | required | Team member role type |
| commission_percentage | Float | required | Commission percentage |
| company_id | Many2one(res.company) | required | Company relation |

#### Methods
| Method | Type | Description |
|--------|------|-------------|
| _compute_name | @api.depends | Compute name from type + percentage |

#### Constraints
| Constraint | Type | Description |
|------------|------|-------------|
| name_unique | SQL | Unique name per company |