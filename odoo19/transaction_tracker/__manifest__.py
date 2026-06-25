# -*- coding: utf-8 -*-
{
    'name': 'Transaction Tracker',
    'version': '1.0.0',
    'category': 'Tools',
    'summary': 'Track all user transactions across every Odoo module',
    'description': """
        Transaction Tracker Module
        ==========================
        Tracks every Create, Write, and Unlink operation performed by users
        across all installed Odoo models. Provides dashboards, reports,
        and configurable tracking settings per model.

        Features:
        - Automatic tracking of Create/Write/Unlink on all models
        - Configurable per-model tracking (enable/disable specific operations)
        - Dashboard with Pivot & Graph views for activity analysis
        - PDF and Excel export reports
        - Suspicious activity detection (bulk deletes, etc.)
        - IP address logging
        - Old/New value tracking for write operations
    """,
    'author': 'Ibrahim Elmasry',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/default_config.xml',
        'views/transaction_log_views.xml',
        'views/tracker_config_views.xml',
        'views/dashboard_views.xml',
        'report/transaction_log_report.xml',
        'report/transaction_log_report_template.xml',
        'views/menu_views.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'transaction_tracker/static/src/js/transaction_dashboard.js',
    #     ],
    # },
    'installable': True,
    'application': True,
    'auto_install': False,
    'post_init_hook': 'post_init_hook',
}
