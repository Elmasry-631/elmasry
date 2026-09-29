{
    "name": "Restrict Journal for Users (Whitelist)",
    "version": "18.0.2.0.0",
    "category": "Accounting/Management",
    "summary": "Per-user journal whitelist — only allowed journals are visible",
    "description": """
Restrict Journal for Users (Whitelist Mode)
============================================

Adds an "Allowed Journals" field on res.users. Admins select which
account.journal records each user is ALLOWED to use; the user will
then ONLY see and use those journals. All other journals are
COMPLETELY HIDDEN (not just read-only — invisible in lists,
dropdowns, and search).

Whitelist semantics:
  * Empty list = unrestricted user (default Odoo behavior — sees all journals).
  * Non-empty list = user can ONLY see/use the journals in this list.

Defense-in-depth: 3 layers (UI onchange + record rules + Python overrides).
Auto group membership: when admin sets allowed list, user is auto-added
to the restriction group; when cleared, user is auto-removed.
""",
    "author": "Ibrahim Elmasry",
    "maintainer": "Ibrahim Elmasry",
    "website": "https://github.com/ُElmasry-631",
    "license": "LGPL-3",
    "depends": [
        "base",
        "account",
    ],
    "data": [
        "security/account_restrict_journal_groups.xml",
        "security/ir.model.access.csv",
        "security/account_restrict_journal_rules.xml",
        "views/res_users_views.xml",
        "views/account_move_views.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "auto_install": False,
    "application": False,
}
