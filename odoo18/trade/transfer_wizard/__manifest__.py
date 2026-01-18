# -*- coding: utf-8 -*-
{
    'name': "trade_paints_wizard",

    'summary': """
        Transfer Wizard""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    'category': 'Uncategorized',
    'version': '1.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management', 'stock', 'purchase',],

    # always loaded
    'data': [
        'wizard/transfer_wizard.xml',
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
}