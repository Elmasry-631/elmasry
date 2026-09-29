{
    'name': 'Hyperpay Payment Acquirer - Applepay',
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'website': 'http://www.technaureus.com/',
    'category': 'Accounting/Payment Providers',
    'version': '19.0.1.0.0',
    'summary': 'Payment Acquirer: Applepay',
    'description': 'Apple Pay payment acquirer integrated with HyperPay OPPWA.',
    'depends': ['payment', 'website'],
    'data': [
        'views/payment_applepay_templates.xml',
        'views/payment_popup_template.xml',
        'views/payment_provider_views.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_applepay/static/src/interactions/payment_form.js',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'license': 'Other proprietary',
}
