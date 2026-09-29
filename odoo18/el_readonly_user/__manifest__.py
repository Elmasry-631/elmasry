# -*- coding: utf-8 -*-
{
    'name': 'EL Readonly User Access',
    'version': '18.0.1.2.0',
    'category': 'Extra Tools',
    'summary': 'Grant controlled read-only access to users',
    'description': """
EL Readonly User Access provides controlled read-only access for selected Odoo users.

Readonly users can access permitted business data without create, write, or delete
operations. Configuration and Settings menus are hidden for this group, while inventory and stock movements remain readable.
    """,
    'author': 'Ibrahim Elmasry',
    'company': 'Ibrahim Elmasry',
    'maintainer': 'Ibrahim Elmasry',
    'website': False,
    'depends': ['base', 'web'],
    'data': [
        'security/el_readonly_user_groups.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'el_readonly_user/static/src/js/readonly_user.js',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'post_update_hook': 'post_update_hook',
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
