{
    'name': 'Mobile Webhook',
    'summary': 'Reliable outbound status webhooks for mobile backends',
    'version': '18.0.1.0.0',
    'category': 'Technical',
    'author': 'Ibrahim Elmasry',
    'license': 'LGPL-3',
    'depends': ['base_setup', 'sale', 'stock', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/mobile_webhook_event_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'application': False,
    'installable': True,
}
