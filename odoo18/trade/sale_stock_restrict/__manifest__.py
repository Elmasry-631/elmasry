{
    'name': 'Sale Stock Restrict',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Module helps to restrict out of stock products',
    'description': """This module helps manage out-of-stock products based on 
    on-hand or forecast quantity.""",
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    'depends': ['base', 'sale_management', 'stock', 'account'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/sale_order.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
