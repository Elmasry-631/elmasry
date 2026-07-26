# -*- coding: utf-8 -*-
{
    "name": "EL Cheque Tracking",
    "version": "19.0.1.0.0",
    "category": "Accounting/Payment",
    "summary": "Track received and issued cheques with accounting lifecycle entries",
    "description": """
Comprehensive cheque management for Odoo 19.

Features
--------
- Received and issued cheque lifecycles with full state machine.
- Accounting entries at every state transition (receipt, deposit, clearance,
  return, issue, cash, void) using configurable accounts.
- Batch deposit wizard, return wizard (with bank charges + penalty) and
  print wizard.
- Post-dated cheque (PDC) maturity reminders and stale-cheque detection
  via scheduled actions.
- Multi-company isolation with record rules.
- Three QWeb PDF reports: cheque print, deposit slip, cheque register.
- Partner cheque stat buttons and audit chatter.
- Settings page for required accounting accounts, stale months, PDC
  reminder days, max re-deposits and approval threshold.

Pattern compliance
------------------
- Odoo 19 ``res.groups.privilege`` security pattern (no ir.module.category).
- ``models.Constraint`` for SQL constraints (no _sql_constraints).
- ``<list>`` view tag (no <tree>), modern invisible/readonly/required
  modifiers (no attrs).
- ``read_group`` for partner cheque stats (no N+1).
""",
    "author": "Ibrahim Elmasry",
    "website": "https://github.com/Elmasry-631",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "account",
    ],
    "data": [
        # Security first (loads groups + ACL + record rules)
        "security/groups.xml",
        "security/ir.model.access.csv",
        "security/ir.rule.xml",
        # Data
        "data/sequence_data.xml",
        "data/return_reason_data.xml",
        "data/account_payment_method_data.xml",
        "data/ir_cron_data.xml",
        # Views
        "views/cheque_views.xml",
        "views/deposit_views.xml",
        "views/return_views.xml",
        "views/return_reason_views.xml",
        "views/partner_views.xml",
        "views/res_config_settings_views.xml",
        "views/account_payment_views.xml",
        "views/account_payment_register_views.xml",
        "views/menus.xml",
        # Wizards
        "wizard/deposit_wizard_views.xml",
        "wizard/return_wizard_views.xml",
        "wizard/print_wizard_views.xml",
        # Reports
        "report/report_cheque_print.xml",
        "report/report_deposit_slip.xml",
        "report/report_cheque_register.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "external_dependencies": {},
}
