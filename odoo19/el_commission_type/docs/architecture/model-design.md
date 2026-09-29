# Model Design - el_commission_type

## sales.commission.type

### ER Diagram


### Field Details

#### name
- **Type:** Char
- **Compute:** _compute_name()
- **Store:** True
- **Readonly:** True
- **Formula:** f"{team_member_type_display} {int(commission_percentage)}%"

#### team_member_type  
- **Type:** Selection
- **Options:**
  - general_manager: General Manager
  - team_manager: Team Manager
  - team_leader: Team Leader
  - salesperson: Salesperson
- **Default:** general_manager
- **Required:** True

#### commission_percentage
- **Type:** Float
- **Default:** 0.0
- **Required:** True
- **Widget:** percentage

#### company_id
- **Type:** Many2one(res.company)
- **Default:** lambda self: self.env.company
- **Required:** True