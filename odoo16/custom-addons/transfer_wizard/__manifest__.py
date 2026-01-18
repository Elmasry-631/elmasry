# -*- coding: utf-8 -*-
{
    'name': "trade_paints_wizard",

    'summary': """
        Transfer Wizard""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Bilal S",
    'website': "bitstechnologies.net",
    'category': 'Uncategorized',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management', 'stock', 'purchase',],

    # always loaded
    'data': [
        'wizard/transfer_wizard.xml',
    ],
    # only loaded in demonstration mode
}