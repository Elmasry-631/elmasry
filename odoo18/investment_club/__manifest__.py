# investment_club/__manifest__.py
{
    'name': 'Investment Clubs Management',
    'version': '18.0.12.0.0',
    'category': 'Investment',
    'summary': 'Complete investment management system with Unified Return System',
    'description': """
        Investment Clubs Management for Al-Namaa - Complete System

        Features:
        1. Customer Membership Number - Unique customer membership number
        2. Clubs Management - Club management (Arabic/English)
        3. Projects Management - Project management
        4. Memberships - Memberships
        5. Investments - Investments (shown by membership number)
        6. Return Payments - Return payments (shown by membership number)

        Unified Return System:
        - Return 1: One-time return with repeat count & duration (One-time return with repetitions)
        - Return 2: Recurring return (Recurring return)
        - Administrative Fees configuration
        - Terms & Conditions per project
        - All fields available per project - fill what you need
        - Grace periods, durations, and dates fully configurable

        Club Features:
        - Bilingual name (Arabic / English)
        - Administrative fees (added as separate invoice line)
        - Max members limit with validation
        - Active/Inactive club status
        - Terms and conditions

        Reports:
        - Unified reports with PDF export (print button) and Excel export
        - Investor Summary, Renewal Due, Monthly Returns
        - Project Summary, Project Profit & Loss
        - Return Payments Summary, Pending Return Payments
        - Return Payment Ledger (Return payment ledger)
        - Investment Maturity Report (Investment Maturity Report)
        - Investor Investment Statement (Investor investment statement)
        - Configurable termination & death case settings
    """,
    'author': 'Woledge',
    'website': 'www.woledge.com',
    'depends': ['base', 'mail', 'account', 'analytic', 'product', 'contacts', 'crm', 'sale_contract_auto', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/cron_data.xml',
        'data/terminate_reason_data.xml',
        'views/contact_view.xml',
        'views/investment_club_views.xml',
        'views/investment_project_views.xml',
        'views/membership_views.xml',
        'views/investment_subscription_views.xml',
        'views/actual_return_views.xml',
        'views/dashboard_views.xml',
        'views/crm_lead_views.xml',
        'views/contact_codes_view.xml',
        'views/res_config_settings_views.xml',
        'views/account_payment_inherit_views.xml',
        'views/sale_contract_inherit_views.xml',
        'views/menu.xml',
        'views/terminate_wizards_views.xml',
        'security/investment_club_security.xml',
        'reports/project_report.xml',
        'reports/returns_report.xml',
        'reports/renewal_due_report.xml',
        'reports/investor_report.xml',
        'reports/project_profit_report.xml',
        'reports/return_payment_ledger_report.xml',
        'reports/investment_maturity_report.xml',
        'reports/investor_statement_report.xml',
        'reports/reports_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'investment_club/static/src/js/dashboard.js',
            'investment_club/static/src/js/dashboard.xml',
            'investment_club/static/src/css/dashboard.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
