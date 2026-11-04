{
    'name': 'Payroll WPS Export',
    'version': '19.0.1.2.0',
    'category': 'Human Resources/Payroll',
    'summary': "Adds an 'Others' field to payslips and the bank salary file export (WPS)",
    'description': """
Payroll WPS Export
===================
- Adds an "Others" field on the payslip (Allowances - Deductions, auto-computed,
  manually editable, informational only — does not affect Net Salary).
- Adds a "WPS Export" wizard that generates the bank salary Excel file (same
  layout as the bank template "ملف رواتب البنك"): البنك, رقم الحساب, إجمالي الراتب
  (=H+I+J-K), ملاحظات (month), اسم الموظف, رقم الهوية أو الإقامة, عنوان الموظف,
  الراتب الأساسي, بدل سكن, بدلات أخرى, خصومات. Missing bank / ID data and amounts
  that do not reconcile with the net salary are reported before export.
- The same file can also be exported as CSV, with the columns of the CSV the
  bank already receives: Bank, Account, Salary(total), Notice(month), Name,
  ID number, address, wage, house, Others, discount (UTF-8 with BOM).
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
