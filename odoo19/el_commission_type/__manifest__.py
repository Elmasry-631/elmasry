{
    'name': 'Commission Types',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Manage sales commission types by team member role',
    'description': '''
        Commission Types Management
        ==========================
        
        This module provides a comprehensive system for managing 
        sales commission types based on team member roles.
        
        Features:
        ---------
        - Auto-generated commission names (e.g., "General Manager 0%")
        - Team Member Type selection (General Manager, Team Manager, Team Leader, Salesperson)
        - Commission percentage with visual widget
        - Multi-company support
        - Chatter integration for notes and activities
        - Standalone Commissions menu
    ''',
    'author': 'Ibrahim Elmasry',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/commission_type_views.xml',
        'views/sales_commission_views.xml',
        'views/res_partner_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    '_constitution_waivers': [
        {'law': 4, 'reason': 'Quick prototype - will add proper icon later'},
    ],
}