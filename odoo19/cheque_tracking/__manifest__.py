# -*- coding: utf-8 -*-
{
    "name": "Cheque Tracking",
    "version": "19.0.1.0.0",
    "category": "Accounting/Payment",
    "summary": "Track received and issued cheques with accounting lifecycle entries",
    "description": """
Comprehensive cheque management for Odoo 19.

Features:
- Received and issued cheque lifecycles
- Accounting entries for receipt, deposit, clearance, return, issuing, and cashing
- Batch deposits and return processing
- Post-dated and stale cheque monitoring
- Cheque printing and deposit slip reports
- Partner cheque counters and audit chatter
    """,
    "author": "Ibrahim Elmasry",
    "website": "https://www.woledge.com",
    "license": "LGPL-3",
    "depends": ["base", "mail", "account"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "security/cheque_security.xml",
        "data/sequence_data.xml",
        "data/return_reason_data.xml",
        "data/ir_cron_data.xml",
        "views/cheque_views.xml",
        "views/deposit_views.xml",
        "views/return_views.xml",
        "views/return_reason_views.xml",
        "views/partner_views.xml",
        "views/res_config_settings_views.xml",
        "wizards/deposit_wizard_views.xml",
        "wizards/return_wizard_views.xml",
        "wizards/print_wizard_views.xml",
        "reports/report_deposit_slip.xml",
        "reports/report_cheque_print.xml",
        "reports/report_cheque_register.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
