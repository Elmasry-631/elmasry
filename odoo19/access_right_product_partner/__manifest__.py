# -*- coding: utf-8 -*-
{
    'name': "access_right_product_partner",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','account','sale','stock','purchase'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'security/group_user.xml',
        'views/product_remove.xml',
        'views/partner_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}