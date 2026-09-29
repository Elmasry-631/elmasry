# Requirements Specification - el_commission_type

## 1. Functional Requirements

### FR-001: Commission Type Model
The system shall provide a model to manage sales commission types.

### FR-002: Team Member Type Selection
The system shall provide a selection field with the following options:
- General Manager
- Team Manager
- Team Leader
- Salesperson

### FR-003: Commission Percentage
The system shall store commission percentage as float value (0-100%).

### FR-004: Auto-generated Name
The system shall automatically generate the name field from:
- team_member_type value
- commission_percentage value
- Format: "{Type} {Percentage}%"
Example: "General Manager 0%"

### FR-005: Read-only Name
The name field SHALL be read-only and computed (not user-editable).

### FR-006: Percentage Widget
The commission_percentage field SHALL use the percentage widget.

## 2. Technical Requirements

### TR-001: Odoo 19 Compatibility
Module MUST be compatible with Odoo 19.

### TR-002: Module Structure
Standard Odoo module structure with proper __init__.py chain.

### TR-003: Views
- Form View with readonly name field
- Tree View for list display
- Search View for filtering

### TR-004: Security
- Proper access rights (create, read, write, delete)
- Record rules for company filtering

## 3. Menu Structure

### M-001: Main Menu
- Name: Commissions
- Position: Standalone top-level menu

### M-002: Submenu  
- Name: Commission Types
- Action: Open sales.commission.type tree/form