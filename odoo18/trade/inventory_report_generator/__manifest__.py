{
    'name': 'Inventory All In One Report Generator',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': "Dynamic Inventory Report Generator for Odoo 17",
    'description': "Streamline your inventory reporting with ease. Generate "
                   "dynamic reports, gain insights, and make informed "
                   "decisions.",
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/inventory_report_views.xml',
        'report/inventory_pdf_report_templates.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'inventory_report_generator/static/src/js/inventory_report.js',
            'inventory_report_generator/static/src/css/inventory_report.css',
            'inventory_report_generator/static/src/xml/inventory_report_templates.xml',
        ]
    },
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
