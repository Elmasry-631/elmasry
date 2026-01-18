# -*- coding: utf-8 -*-
{
    'name': "payment_fix",

    "summary": """payment fix
    """,
    "description": """
        payment fix
    """,

    'author': "BITS",
    'website': "https://bitstechnology.net",

    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': ['views/account_payment_view.xml',],
}
