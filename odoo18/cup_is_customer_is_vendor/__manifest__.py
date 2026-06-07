# -*- coding: utf-8 -*-
{
    'name': "Is a Customer and Is a Vendor",

    'summary': """
        Add Field Is a Customer And Is a Vendor""",

    'description': """
        *   Add Field Is a Customer And Is a Vendor checkbox Into The Partner Form For Identification.\n
        *   Easy To Use.\n
        *   User Can Manually Set / Unset Customer and Vendor Checkbox.\n
        *   Add Customer Filter In Sale Order.\n
        *   Add Vendor Filter In Purchase Order.
    """,

    'license': "LGPL-3",
    'images': ['static/description/cupdev2.png'],
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','account','sale_management','purchase'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}