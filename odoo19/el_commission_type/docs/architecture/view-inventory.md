# View Inventory - el_commission_type

## Views

### 1. Form View: view_commission_type_form
- **Model:** sales.commission.type
- **Layout:**
  - Group with readonly name field (top)
  - Two-column group:
    - Left: team_member_type, commission_percentage (with widget)
    - Right: company_id
  - Chatter at bottom

### 2. Tree View: view_commission_type_tree  
- **Model:** sales.commission.type
- **Columns:** name, team_member_type, commission_percentage, company_id

### 3. Search View: view_commission_type_search
- **Model:** sales.commission.type
- **Fields:** name, team_member_type
- **Filters:** My Company