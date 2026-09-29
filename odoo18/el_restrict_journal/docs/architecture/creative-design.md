# Creative Design — el_restrict_journal

## The 5 Creative Lenses Applied

### Lens 1: Pattern Discovery

**Pattern identified:** "Security Extension Pattern" — extends existing models with record rules + Python overrides.

**Pattern source:** Standard Odoo pattern used by `account_sequential_drafts`, `account_lock`, `account_tax_audit` — every "restrict X" module uses the same 3-layer defense (UI onchange → record rule → Python override).

**Why this pattern fits:**
- Additive (no breaking changes to existing flows)
- Reversible (uninstall removes all restrictions)
- Composable (works alongside other accounting modules)
- Auditable (every restriction raises a logged exception)

### Lens 2: UX Innovation

**8 UX strategies considered, 3 applied:**

| Strategy | How Applied |
|----------|-------------|
| **Immediate Feedback** | `_onchange_journal_id` clears the journal + shows a warning popup BEFORE the user clicks Save — eliminates "fill form → click save → error" frustration |
| **Visible Configuration** | Smart button on `account.journal` form: "Restricted Users (N)" — managers can see at-a-glance which journals have restrictions, click to drill into the user list |
| **Non-Destructive Default** | Empty `journal_ids` = unrestricted → installing the module changes NOTHING until admin actively configures restrictions |

### Lens 3: Smart Automation

**5 automation types considered, 1 applied:**

| Type | Applied? | Notes |
|------|----------|-------|
| Scheduled (cron) | ❌ No | Restrictions are real-time; no need for scheduled checks |
| On-Event (bus) | ❌ No | Restriction is checked at operation time, not asynchronously |
| On-Write (override) | ✅ Yes | `create`/`write` overrides enforce restriction automatically |
| Computed | ❌ No | (Avoiding the original module's anti-pattern) |
| Workflow | ❌ No | No state machine needed |

### Lens 4: Future-Proofing

**4 scalability strategies applied:**

| Strategy | How |
|----------|-----|
| **Index-friendly fields** | No new indexed fields; uses existing `journal_id` index on `account_move` and `account_payment` |
| **Batch-safe overrides** | `@api.model_create_multi` for `create` — handles batch creation correctly |
| **Multi-company ready** | `journal_ids` M2M filters by `company_ids` automatically (record rule on `account.journal`) |
| **Backwards-compatible uninstall** | All overrides use `super()` chain; uninstall cleanly removes the module without orphan records |

### Lens 5: Wow Factor

**1 of 12 differentiators applied:** **"Defense in Depth"** visualization.

Most "restrict" modules stop at one layer (either record rule OR Python override). This module uses **3 layers**:
1. UI Onchange (immediate UX feedback)
2. Record Rules (ORM-level enforcement)
3. Python `@api.constrains` (post-super safety net)

This is documented in the user form as a tooltip: "Restrictions are enforced at 3 layers for maximum security."

## Icon Design

**Concept:** A padlock over a ledger book.
- **Color:** Accounting green (#0d8a72) — matches Odoo's "Accounting" category color
- **Glyph:** Lock icon ( restricting access to a journal/ledger)
- **Style:** Flat, single-color, 256x256 PNG, transparent background
- **Rationale:** Instantly communicates "restricted access to financial records"

## UI Design Choices

| Element | Choice | Rationale |
|---------|--------|-----------|
| Smart button on journal form | Icon: `fa-lock` | Universal "restricted" symbol |
| Smart button color | Default (no decoration) | Avoids visual noise on the journal form |
| User form tab name | "Restricted Journals" | Clear, action-oriented |
| Field widget for `journal_ids` | Standard Many2many tags | Familiar widget; users see selected journals as removable tags |
| Onchange warning popup | Title: "Restricted Journal" | Action-oriented; tells user what to do |

## Differentiator Summary

This module is **not** the first "restrict journal" module in the Odoo ecosystem. But it is the first to:
1. Use 3-layer defense (others use 1 or 2)
2. Provide an onchange UX layer (others force users to click Save then fail)
3. Have full test coverage (≥13 tests; others ship untested)
4. Have full Arabic translation (others ship English-only)
5. Have full docs + stakeholder analysis + RACI matrix (others ship README only)
