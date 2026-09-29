# -*- coding: utf-8 -*-
{
    'name': "Deduction",

    'summary': "Manages employees' deductions",

    'description': """Manages employees' deductions""",

    'author': "Abdullah Al-Habbal",
    'website': "",
    'category': 'Hidden',
    'version': '19.0.2.0.0',
    'depends': ['base', 'hr_payroll', 'hr_work_entry_enterprise'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/deduction_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'Other proprietary',
}

