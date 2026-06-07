# -*- coding: utf-8 -*-
{
    'name': 'Invoice Tracking',
    'version': "19.0.1.0.0",
    'summary': 'Brief description of the module',
    'description': '''
        Detailed description of the module
    ''',
    'category': 'accounting',
    'author': 'Ibrahim Elmasry',
    'website': 'https://www.woledge.com',
    'depends': ['base', 'mail', 'account', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'data/invoice_tracking_sequence.xml',

        'views/well_view.xml',
        'views/invoice_tracking_views.xml',
        'views/purchase_order_views.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'views/check_tracking_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu_item.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
