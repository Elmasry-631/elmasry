# -*- coding: utf-8 -*-
{
    'name': 'Disallow Negative Stock (Elmasry)',
    'version': '20.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Prevent Negative Stock in POS & Inventory',
    'description': """
This module prevents negative stock levels in both Point of Sale and Inventory operations,
with advanced support for kit products and configurable exceptions.

Features:
✅ Prevents negative stock in POS and Inventory operations.
✅ Supports kit products with phantom BoMs.
✅ Configurable exceptions for specific products or categories.
✅ Real-time stock validation during transactions.
✅ User-friendly error messages and alerts.
    """,
    'author': 'Elmasry',
    'website': 'https://elmasry.com',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'point_of_sale',
    ],
    'data': [
        'views/product_template_views.xml',
        'data/ir_config_parameter.xml',
    ],
    'demo': [],
    'auto_install': False,
    'installable': True,
    'application': False,
}