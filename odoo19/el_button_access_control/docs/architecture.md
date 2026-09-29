# Architecture — el_button_access_control

## Overview

The module uses a **hook pattern**: by inheriting `base` (the abstract model
ALL Odoo models extend), we insert our logic into every `fields_view_get`
call system-wide. This allows us to modify view archs before they reach
the browser, without modifying any target module's XML.

## Core Components

### 1. `el.button.access.rule` (Rule Model)

Stores the admin-defined rules. Each rule specifies:
- **Target**: model + view type
- **Button**: method name to match
- **Mode**: whitelist (show_only) or blacklist (hide_from)
- **Groups**: which res.groups are involved

### 2. `base` extension (fields_view_get override)

The `_el_apply_button_access_rules` method:
1. Checks if rules exist for the current model/view
2. Parses the view arch as XML (lxml)
3. XPath-finds `<button>` elements matching the rule's `button_name`
4. Injects `groups=` (whitelist) or `invisible=` (blacklist) attributes
5. Serializes the modified arch back to string

### 3. Cache Invalidation

On rule CRUD (create/write/unlink), we call `self.env.registry.clear_cache()`
to ensure the modified views are re-rendered on next access.

## Data Flow

```
User requests view
    ↓
Odoo calls fields_view_get()
    ↓
super().fields_view_get() returns original arch
    ↓
_el_apply_button_access_rules():
    → Search active rules for this model/view
    → Parse arch as XML
    → For each rule: XPath //button[@name='xxx']
    → Inject groups= or invisible= attribute
    → Return modified arch
    ↓
Odoo renders modified arch to browser
    ↓
User sees only buttons they're authorized to see
```

## Design Decisions

### Why inherit `base` instead of specific models?
Inheriting `base` means our override runs for EVERY model — no need to know
in advance which models the admin will target. The performance impact is
minimal because we check for active rules before doing any XML parsing.

### Why `groups=` for whitelist but `invisible=` for blacklist?
- `groups="g1,g2"` is Odoo's native attribute — it tells the framework to
  hide the element for users not in those groups. This is the cleanest
  approach for whitelisting.
- There's no native `hide_from_groups=` attribute. For blacklisting, we
  use `invisible="user.has_group('g1') or user.has_group('g2')"` which
  Odoo evaluates per-user at render time.

### Why not use `ir.ui.view` inheritance?
View inheritance requires writing XML patches for each target view. Our
approach is dynamic — the admin can target ANY button in ANY model without
writing a single line of XML.
