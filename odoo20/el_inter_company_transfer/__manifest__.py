# -*- coding: utf-8 -*-
{
    'name': 'Inter Company Internal Transfer',
    'version': '20.0.1.0.1',
    'author': 'Ibrahim Elmasry',
    'summary': 'Request stock transfers between warehouses of different companies',
    'description': """
Inter Company Internal Transfer
================================

Allows users to request stock transfers between warehouses of different companies.

Features
--------
* Create transfer requests from a warehouse in one company to a warehouse in another company
* Multi-company support with proper access control
* Request workflow: Draft -> Confirmed -> Done
* Automatic stock move creation upon confirmation by authorized user
* Email notifications for request updates
* Full chatter and activity tracking
* Dashboard for managing transfer requests

Workflow
--------
1. User in Company A creates a request for products from Company B's warehouse
2. Request is in 'Draft' state
3. User with access to Company B's warehouse confirms the request
4. Stock moves are automatically created in Company B for the requested quantities
5. Request moves to 'Done' state

Security
--------
* Users can only create requests for their own company's warehouses as source
* Users can only confirm requests for companies they have access to
* Multi-company access is enforced through ir.access domains (Odoo 20 unified access model)

Author
------
Ibrahim Elmasry
    """,
    'depends': [
        'base',
        'stock',
        'mail',
        'portal',
    ],
    'data': [
        'security/ir.access.csv',
        'data/ir_sequence_data.xml',
        'views/transfer_request_views.xml',
        'views/transfer_request_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'category': 'Inventory/Warehouse Management',
}