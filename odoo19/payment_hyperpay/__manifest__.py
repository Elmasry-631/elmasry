{
    'name': 'Hyperpay Payment Acquirer',
    'author': 'Webkul Software Pvt. Ltd.',
    'maintainer': 'Anuj Kumar Chhetri',
    'website': 'https://store.webkul.com/odoo-hyperpay-payment-acquirer.html',
    'category': 'Accounting/Payment Providers',
    'version': '19.0.1.0.1',
    'summary': 'Website Hyper Pay Payment Acquirer',
    'description': 'Odoo HyperPay payment gateway integration for website checkout.',
    'depends': ['account', 'payment', 'website_sale'],
    'data': [
        'views/payment_hyperpay_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_hyperpay/static/src/css/loader.css',
            'payment_hyperpay/static/src/interactions/payment_form.js',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'application': True,
    'license': 'Other proprietary',
}
