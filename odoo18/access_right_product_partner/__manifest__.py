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
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','product','account','sale','stock','purchase'],
    'data': [
        #'security/ir.model.access.csv',
        'security/group_user.xml',
        'views/product_remove.xml',
        'views/partner_views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}