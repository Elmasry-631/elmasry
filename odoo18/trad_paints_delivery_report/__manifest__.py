# -*- coding: utf-8 -*-
{
    'name': "trad_paints_delivery_report",

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
    'category': 'stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_location_view.xml',
        'reports/templates/report.xml',
        'reports/templates/stock_picking_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}