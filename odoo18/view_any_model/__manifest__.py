{
    'name': 'View Records Of Any Model',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'View records of selected model',
    'description': 'This module helps to display and interact with records '
                   'from a specific model in Odoo, either in a List View or a Form View.',
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    'depends': ['base'],
    'data': [
        'security/view_any_model_groups.xml',
        'security/ir.model.access.csv',
        'wizard/view_any_model_views.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
