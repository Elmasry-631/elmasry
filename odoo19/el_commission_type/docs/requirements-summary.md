# Requirements Summary - el_commission_type

## Module Overview
- **Module Name:** el_commission_type
- **Odoo Version:** 19
- **Purpose:** Sales Commission Types Management

## Business Requirement
Manage sales commission types by team member role with automatic name generation.

## Models

### 1. sales.commission.type
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | Char (Computed) | Yes | Auto-generated: "{Team Member Type} {Percentage}%" |
| team_member_type | Selection | Yes | Role type (General Manager, Team Manager, Team Leader, Salesperson) |
| commission_percentage | Float | Yes | Commission percentage (0-100%) with percentage widget |
| company_id | Many2one | Yes | Company (res.company) |

## Views Required
1. **Form View** - Single record editing with readonly computed name
2. **Tree/List View** - List view for browsing records
3. **Search View** - Search and filter capabilities

## Menu Structure
- Main Menu: Commissions (standalone top-level menu)
- Submenu: Commission Types

## Key Features
- Name is computed from team_member_type + commission_percentage
- Name field is READONLY (user cannot edit)
- Percentage widget on commission_percentage field
- Multi-company support
- Chatter integration (mail.thread)

## Security
- Standard CRUD access controls
- Company-based record filtering