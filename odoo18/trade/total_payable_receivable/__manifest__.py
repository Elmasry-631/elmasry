{
    'name': 'Payable And Receivable Amount',
    'version': '18.0.1.0.1',
    'category': 'Accounting',
    'summary': """Amount Payable & Receivable In Partner Form""",
    'description': "Shows Amount Payable & Receivable In customer/vendor Form",
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    'depends': ['account'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}

