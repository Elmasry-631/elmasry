{
    'name': 'Customer Credit Limit with Due Amount Warning',
    'version': '18.0.1.0.0',
    'summary': 'An advanced way to handle customer credit limit through warning and blocking stage.',
    'description': """This module helps you to handle customer credit limit in an efficient way.
                You can set a warning stage and blocking stage to a particular customer.
                This module also shows the due amount of a customer while creating an order.""",
    'category': 'Sales',
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    'depends': ['base', 'sale_management'],
    'data': [
        'views/credit_limit_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
    'price': 20,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,
}
