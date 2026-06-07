# -*- coding: utf-8 -*-
{
    'name': 'Meta Lead Ads',
    'version': '18.0.1.0.0',
    'summary': 'Import Meta lead ads into CRM leads',
    'description': """
Meta Lead Ads
=============

Technical CRM module that connects Meta Lead Ads to Odoo CRM.
It manages Meta credentials, pages, forms, field mappings, and lead imports.
    """,
    'category': 'Sales/CRM',
    'author': 'Archer Solutions',
    'license': 'LGPL-3',
    'depends': [
        'crm',
        'mail',
        'contacts',
        'utm',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/meta_app_credential_views.xml',
        'views/meta_page_views.xml',
        'views/meta_lead_form_views.xml',
        'views/meta_sync_log_views.xml',
        'views/crm_lead_views.xml',
        'views/res_config_settings_views.xml',
        'views/menus.xml',
    ],
    'application': False,
    'installable': True,
}
