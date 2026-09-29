# -*- coding: utf-8 -*-
{
    'name': 'Product Movement Lifecycle Report',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Reporting',
    'summary': 'Full movement history of a product/lot from first receipt until fully sold',
    'description': """
Product Movement Lifecycle Report
=================================
For a product (optionally a specific lot/serial) shows every done stock move
in chronological order with running balance, split into cycles
(a cycle ends when the on-hand balance returns to zero = fully sold/consumed).

Available as a list view and as a landscape PDF.
""",
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_movement_views.xml',
        'report/product_movement_report.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
