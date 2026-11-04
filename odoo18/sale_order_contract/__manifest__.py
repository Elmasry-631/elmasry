{
    'name': "Sale Order Contract",
    'version': '0.1',
    'category': 'Sales',
    'summary': "Automatically generate contracts from sale orders.",
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    'license': 'LGPL-3',

    'depends': [
        'base',
        'sale',
        'account',
    ],

    'data': [
        # 'report/paperformat.xml',
        'report/contract_report.xml',
        'report/contract_print_template.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}