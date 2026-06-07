# -*- coding: utf-8 -*-
{
    'name': 'Advanced Accounting Reports',
    'version': '1.20.0',
    'category': 'Accounting',
    'summary': 'Advanced General Ledger, Trial Balance with Analytic Dimensions & Multi-Currency',
    'description': """
Advanced Accounting Reports
===========================

This module extends Odoo 19 Accounting with:

* **Analytic Dimensions**
  - Features
  - Cost Centers
  - Patch Numbers

* **Multi-Currency Support**
  - Secondary Currency
  - Manual Exchange Rate per Journal Entry
  - Automatic Secondary Amount Calculation

* **Advanced Reports**
  - General Ledger (with dimensions & secondary currency)
  - Trial Balance (with dimensions & secondary currency)

* **Professional Export**
  - Excel (XLSX) with formulas, RTL, company header
  - PDF (QWeb) with Arabic fonts, RTL, signatures

* **Full Arabic & English Support**
  - Clean translation files (ar.po / en.po)
  - RTL layouts

* **Enterprise Ready**
  - Multi-company
  - Multi-currency
  - Performance optimized (SQL for heavy reports)
  - Upgrade-safe architecture
""",
    'author': 'Woledge',
    'website': 'https://www.woledge.com',
    'depends': [
        'account',
        'account_reports',
        'base',
        'web',
    ],
    'external_dependencies': {
        'python': ['xlsxwriter'],
    },
    'data': [
        # Security (first)
        'security/security.xml',
        'security/ir.model.access.csv',
        # Data
        'data/sequence.xml',
        # Views - Dimensions
        'views/account_feature_views.xml',
        'views/account_cost_center_views.xml',
        'views/account_patch_number_views.xml',
        # Views - Moves
        'views/account_move_views.xml',
        'views/account_move_line_views.xml',
        # Wizards (must be BEFORE reports that reference them)
        'wizard/general_ledger_wizard_views.xml',
        'wizard/trial_balance_wizard_views.xml',
        # Report Templates (must be BEFORE report actions)
        'report/report_general_ledger.xml',
        'report/report_trial_balance.xml',
        # Report Actions (must be AFTER templates)
        'report/report_actions.xml',
        # Report List Views
        'views/report_general_ledger_views.xml',
        'views/report_trial_balance_views.xml',
        # Menus (must be LAST)
        'views/menus.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'pre_init_hook': '_pre_init_hook',
    'post_init_hook': '_post_init_hook',
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'advanced_accounting_reports/static/src/js/general_ledger_controller.js',
        ],
    },
}