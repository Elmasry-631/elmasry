# -*- coding: utf-8 -*-
{
    'name': 'Ie Restrict Qty',
    'version': '1.0',
    'summary': 'Brief description of the module',
    'description': '''
        Detailed description of the module
    ''',
    'category': 'Uncategorized',
    'author': 'Ibrahim Elmasry',

    'website': 'https://www.woledge.com',
    'depends': ['base', 'mail','stock','sale_management'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/ie_restrict_qty_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}