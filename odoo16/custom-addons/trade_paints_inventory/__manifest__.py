# -*- coding: utf-8 -*-
{
    'name': "Trade Paint Inventory",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "BITS Technology",
    'website': "bitstechnology.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management', 'stock', 'purchase',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/trade_paints_groups.xml',
        'views/inventory.xml',
        'views/partner.xml',
        'views/product.xml',
        'views/res_users_view.xml',
        'report/report_deliveryslip.xml',
        'report/report_all_delivery.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}