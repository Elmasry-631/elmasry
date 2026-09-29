# -*- coding: utf-8 -*-
{
    'name': "Loans Management",

    'summary': "Manages employees' loans",

    'description': """Manages employees' loans""",

    'author': "Abdullah Al-Habbal",
    'website': "",
    'category': 'Hidden',
    'version': '19.0.2.0.0',
    'depends': ['base', 'hr_payroll'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/loan_views.xml',
        'views/hr_payslip_views.xml',
        'report/hr_payslip_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'Other proprietary',
}

