{
    'name': 'Vehicle Installment Management',
    'version': '19.0.2.0.0',
    'category': 'Fleet',
    'summary': 'Manage vehicle installments with automatic calculation',
    'description': """
Vehicle Installment Management
================================
This module allows you to manage vehicle installments with:
* Link to fleet vehicles
* Rate percentage calculation
* Automatic installment calculation with fractional handling
* Monthly payment tracking
* Approval workflow
    """,
    'author': 'Abdullah Al-Habbal',
    'website': '',
    'depends': ['base', 'mail', 'fleet', 'hr', 'hr_payroll'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/vehicle_installment_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
