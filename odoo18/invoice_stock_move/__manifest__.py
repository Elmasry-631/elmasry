{
    'name': "Stock Picking From Invoice",
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': """Stock Picking From Customer/Supplier Invoice""",
    'description': """This Module Enables To Create Stocks Picking From 
     Customer/Supplier Invoice""",
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    'depends': ['account', 'stock', 'payment'],
    'data': ['views/account_move_views.xml'],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
