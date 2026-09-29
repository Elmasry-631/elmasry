{
    'name': 'Sale Order Confirmation User',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Track which user actually confirmed each sales order',
    'description': """
Sale Order Confirmation User
=============================
Adds a "Confirmed By" field on the Sales Order (sale.order) that stores the
actual user who performed the confirmation action (as opposed to the
Salesperson, the record creator, or the last writer).

Adds a "Confirmed By" filter and Group By in the Sales Orders / Quotations
search view.
""",
    'author': 'Ibrahim Elmasry',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
