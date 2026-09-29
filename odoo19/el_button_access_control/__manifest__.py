{
    'name': 'Button Access Control',
    'version': '19.0.1.0.0',
    'category': 'Tools/Security',
    'summary': 'Control button visibility per user group — show/hide buttons in any view without editing XML',
    'description': """
Button Access Control
=====================

Dynamically control which buttons appear or disappear for specific user groups
in any Odoo view — WITHOUT modifying the original view XML.

Features:
- Show buttons only to specific groups (whitelist mode)
- Hide buttons from specific groups (blacklist mode)
- Apply to form, list, kanban, or all views
- Works with any model — no code changes needed in target modules
- Admin-friendly UI for managing rules
- Real-time preview of affected buttons

How it works:
1. Admin creates a "Button Access Rule" specifying:
   - The target model (e.g., sale.order)
   - The button method name (e.g., action_confirm)
   - The view type (form, list, kanban, all)
   - The mode (show_only or hide_from)
   - The groups affected
2. The module overrides fields_view_get on the base model
3. Before rendering any view, it injects groups="..." or invisible="..."
   attributes on matching buttons based on the active rules
4. The user only sees buttons they're authorized to see

Author: Built with odoo-build-master v1.1.0
License: LGPL-3
    """,
    'author': 'Ibrahim Elmasry',
    'website': 'https://github.com/Elmasry-631',
    'license': 'LGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'security/el_button_access_control_groups.xml',
        'security/ir.model.access.csv',
        'views/button_access_rule_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    '_constitution_version': '1.1.0',
    'assets': {
        'web.assets_backend': [
            'el_button_access_control/static/src/**/*',
        ],
    },
}
