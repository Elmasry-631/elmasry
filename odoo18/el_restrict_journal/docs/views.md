# Views — el_restrict_journal

## 1. res.users form (inherit)

Inherits `base.view_users_form`, adds a new "Restricted Journals" page to the notebook.

```xml
<xpath expr="//notebook" position="inside">
    <page string="Restricted Journals" name="restricted_journals"
          groups="el_restrict_journal.group_restrict_journal_manager">
        <group>
            <field name="journal_ids" widget="many2many_tags"
                   options="{'no_create': True, 'no_create_edit': True}"/>
        </group>
    </page>
</xpath>
```

## 2. account.move form (inherit)

Inherits `account.view_move_form`, ensures the journal_id field has `no_create` option (so users cannot create new journals from the move form).

## View Architecture

```mermaid
graph TD
    A[base.view_users_form] --> B[view_users_form_restrict_journal]
    C[account.view_move_form] --> D[view_account_move_form_restrict_journal]
```

## UX Flow

```mermaid
flowchart LR
    A[Manager opens user form] --> B[Clicks Restricted Journals tab]
    B --> C[Selects journals via tag widget]
    C --> D[Saves]
    D --> E[Restriction active]
```
