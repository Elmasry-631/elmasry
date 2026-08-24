{
    'name': 'Prevent Negative Stock',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Security',
    'summary': 'Prevent negative stock — block stock moves AND sales orders when stock is insufficient',
    'description': """
Prevent Negative Stock
======================

Prevents negative stock quantities by rejecting any stock move or sales order
that would result in a negative quantity for a product in a given location.

Features:
- Rejects ALL stock moves that would cause negative stock (delivery, internal, MRP)
- Blocks sales order confirmation when products have insufficient stock
- NO exceptions — even managers cannot bypass
- Creates an alert log entry for every rejected attempt
- Sends email notification to warehouse manager on rejection

Author: Ibrahim Elmasry
License: LGPL-3
    """,
    'author': 'Ibrahim Elmasry',
    'website': 'https://github.com/Elmasry-631',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'stock',
        'mail',
        'sale_management',
        'nmo_sale_order_approval_workflow',
        'nmo_stock_user_restriction',
    ],
    'data': [
        'security/el_prevent_negative_stock_groups.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/sequence.xml',
        'views/el_stock_alert_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    '_constitution_version': '1.1.0',
}
