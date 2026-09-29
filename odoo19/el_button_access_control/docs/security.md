# Security — el_button_access_control

## Security Groups

| Group | Description | Permissions |
|-------|-------------|-------------|
| `group_button_access_user` | Button Access: User | Read rules (view-only) |
| `group_button_access_manager` | Button Access: Manager | Full CRUD on rules |

The Manager group is assigned to `admin` by default.

## Access Rights (ir.model.access.csv)

| Model | User Group | Read | Write | Create | Delete |
|-------|-----------|------|-------|--------|--------|
| el.button.access.rule | User | ✓ | ✗ | ✗ | ✗ |
| el.button.access.rule | Manager | ✓ | ✓ | ✓ | ✓ |

## Record Rules

No record rules are needed — the ACL is sufficient. All rules are visible
to all users in the User/Manager groups regardless of company.

## Field-Level Security

No fields are restricted — all fields are visible to users who can access
the rule model.

## Notes

- The `fields_view_get` override runs for ALL users, but it only READS rules.
  It doesn't require any special permissions.
- The cache clearing on rule CRUD requires the user to be in the Manager group
  (enforced by ACL, not by code).
