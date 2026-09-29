# -*- coding: utf-8 -*-
{
    'name': 'Inter Company Transfer',
    'version': '19.0.1.0.0',
    'category': 'Warehouse / Inventory',
    'summary': 'Automate inter-company stock, sale, purchase, and accounting documents',
    'description': """
Inter Company Transfer
======================
Automates stock and accounting inter-company transactions between companies in
one Odoo database. It creates and links sale orders, purchase orders, pickings,
customer invoices, vendor bills, and return transactions according to configured
company-pair rules.
    """,
    'author': 'Ibrahim Elmasry',
    'website': 'https://www.odoo.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'stock',
        'sale_management',
        'sale_stock',
        'purchase',
        'purchase_stock',
        'account',
    ],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'data/inter_company_sequence.xml',
        'views/inter_company_config_views.xml',
        'views/stock_inter_company_transfer_views.xml',
        'views/return_inter_company_transfer_views.xml',
        'views/res_company_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
        'views/inter_company_menus.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
