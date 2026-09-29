# Security Inventory - el_commission_type

## Access Rights

### Access Right: sales_commission_type.user
- Model: sales.commission_type
- Permissions: read, write, create, unlink
- Groups: 
  - el_commission_type.group_commission_user
  - el_commission_type.group_commission_manager

## Record Rules

### Rule: commission_type_company_rule
- Model: sales.commission_type
- Domain: ['|', ('company_id', '=', False), ('company_id', 'in', user.company_ids.id)]
- Groups: All users

## Security Groups

### Group: Commission Type User
- Name: Commission Type User
- Category: Commissions
- Implied: base.group_user
- Users: Sales team members

### Group: Commission Type Manager
- Name: Commission Type Manager  
- Category: Commissions
- Implied: el_commission_type.group_commission_user
- Users: Managers