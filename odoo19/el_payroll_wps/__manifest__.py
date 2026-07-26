{
    'name': 'Payroll WPS Export',
    'version': '19.0.1.0.0',
    'category': 'Human Resources/Payroll',
    'summary': "Adds an 'Others' field to payslips and a WPS CSV export action",
    'description': """
Payroll WPS Export
===================
- Adds an "Others" field on the payslip (Allowances - Deductions, auto-computed,
  manually editable, informational only — does not affect Net Salary).
- Adds a "WPS Export" wizard/action that generates a CSV file for all payslips
  in a chosen month, with the columns required for WPS bank submission:
  Bank, Account, Salary (Net), Notice (Month), Name, ID Number, Address,
  Wage, House, Others, Discount (Deductions).
- Odoo 19 compatible: uses primary_bank_account_id, private_state_id,
  validated/paid states, HOUALLOW housing rule code.
""",
    'author': 'Ibrahim Elmasry',
    'license': 'LGPL-3',
    'depends': ['base', 'hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wps_export_wizard_views.xml',
        'views/hr_payslip_views.xml',
    ],
    'tests': ['tests/test_wps_export.py'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
}
