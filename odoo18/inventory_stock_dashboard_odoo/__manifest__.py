{
    'name': 'Inventory Dashboard Odoo 18',
    'version': '18.0.1.0.0',
    'category': 'Warehouse',
    'summary': 'Detailed dashboard view for Inventory module.',
    'description': """This module presents a detailed dashboard view for the
    Inventory module, delivering a compr    ehensive and concise overview that
    serves as a valuable tool for both inventory users and administrators.""",
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    'depends': ['stock', 'base'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/dashboard_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&amp;display=swap',
            'inventory_stock_dashboard_odoo/static/src/css/dashboard.css',
            'inventory_stock_dashboard_odoo/static/src/js/dashboard.js',
            'inventory_stock_dashboard_odoo/static/src/xml/inventory_dashboard_template.xml',
            'https://cdn.jsdelivr.net/npm/chart.js',
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,  
    'application': False,
}
