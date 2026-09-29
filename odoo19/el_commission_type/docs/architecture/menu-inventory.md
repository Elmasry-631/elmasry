# Menu Inventory - el_commission_type

## Menu Structure

### Top-Level Menu
- **ID:** menu_commissions_root
- **Name:** Commissions
- **Sequence:** 100
- **Parent:** None (standalone)
- **Action:** None (container only)

### Submenu: Commission Types
- **ID:** menu_commission_type
- **Name:** Commission Types
- **Parent:** menu_commissions_root
- **Sequence:** 10
- **Action:** action_commission_type

## Actions

### Action: action_commission_type
- **ID:** action_commission_type
- **Name:** Commission Types
- **Res Model:** sales.commission.type
- **View Mode:** list,form
- **Help Text:** Create your first commission type!