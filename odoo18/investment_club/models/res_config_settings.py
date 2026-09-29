# investment_club/models/res_config_settings.py
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # ===== Membership Settings =====
    membership_product_id = fields.Many2one(
        'product.product',
        string='Default Membership Product',
        config_parameter='investment_club.membership_product_id',
        domain="[('type', '=', 'service')]",
        help='Default product used when creating a new membership invoice.',
    )

    subscription_product_id = fields.Many2one(
        'product.product',
        string='Default Subscription Product',
        config_parameter='investment_club.subscription_product_id',
        domain="[('type', '=', 'service')]",
        help='Default product used when creating a renewal subscription invoice.',
    )

    admin_fees_product_id = fields.Many2one(
        'product.product',
        string='Default Administrative Fees Product',
        config_parameter='investment_club.admin_fees_product_id',
        domain="[('type', '=', 'service')]",
        help='Default product used for administrative fees on membership invoices.',
    )

    subscription_period = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly')
    ], string='Default Subscription Period',
       config_parameter='investment_club.subscription_period',
       default='yearly',
       help='Default subscription period applied to new memberships.')

    auto_renewal_days = fields.Integer(
        string='Auto Renewal Days Before Expiry',
        config_parameter='investment_club.auto_renewal_days',
        default=7,
        help='Number of days before membership expiry to send renewal reminder.',
    )

    # ===== Payment Settings =====
    payment_journal_id = fields.Many2one(
        'account.journal',
        string='Default Payment Journal',
        config_parameter='investment_club.payment_journal_id',
        domain="[('type', 'in', ('bank', 'cash'))]",
        help='Default journal for membership and investment payments.',
    )

    return_payment_journal_id = fields.Many2one(
        'account.journal',
        string='Returns Payment Journal',
        config_parameter='investment_club.return_payment_journal_id',
        domain="[('type', 'in', ('bank', 'cash'))]",
        help='Default journal for paying out investment returns to investors.',
    )

    # ===== Project Settings =====
    auto_activate_projects = fields.Boolean(
        string='Auto Activate Projects',
        config_parameter='investment_club.auto_activate_projects',
        default=False,
        help='Automatically set new projects to active status upon creation.',
    )

    grace_period_months = fields.Integer(
        string='Default Grace Period (Months)',
        config_parameter='investment_club.grace_period_months',
        default=3,
        help='Default grace period before investment returns start accruing.',
    )

    # ===== Notification Settings =====
    enable_renewal_notifications = fields.Boolean(
        string='Enable Renewal Notifications',
        config_parameter='investment_club.enable_renewal_notifications',
        default=True,
        help='Send automated notifications before membership expiry.',
    )

    enable_payment_notifications = fields.Boolean(
        string='Enable Payment Notifications',
        config_parameter='investment_club.enable_payment_notifications',
        default=True,
        help='Send notifications when investment returns are paid.',
    )

    # ===== Access Settings =====
    restrict_project_creation = fields.Boolean(
        string='Restrict Project Creation to Managers',
        config_parameter='investment_club.restrict_project_creation',
        default=True,
        help='Only users with manager role can create new investment projects.',
    )

    require_approval_for_investment = fields.Boolean(
        string='Require Approval for Investments',
        config_parameter='investment_club.require_approval_for_investment',
        default=False,
        help='Investments require manager approval before activation.',
    )

    # ===== Module Access Control =====
    module_access_enabled = fields.Boolean(
        string='Enable Investment Club Module Access',
        config_parameter='investment_club.module_access_enabled',
        default=True,
        help='When checked, users have full access to the Investment Club module. When unchecked, users have no access.',
    )

    # ===== Invoice Settings =====
    invoice_prefix = fields.Char(
        string='Invoice Reference Prefix',
        config_parameter='investment_club.invoice_prefix',
        default='INV-CLUB',
        help='Prefix used in invoice references for membership invoices.',
    )

    # ===== Termination & Death Case Settings =====
    termination_allowed_months = fields.Integer(
        string='Termination Allowed Period (Months)',
        config_parameter='investment_club.termination_allowed_months',
        default=3,
        help='Number of months during which contract termination is allowed (default: 3 months)',
    )

    termination_deduction_amount = fields.Float(
        string='Early Termination Deduction Amount',
        config_parameter='investment_club.termination_deduction_amount',
        default=6500.0,
        help='Termination deduction during the allowed period (default: 6500)',
    )

    termination_client_share_pct = fields.Float(
        string='Client Share of Increase (%)',
        config_parameter='investment_club.termination_client_share_pct',
        default=70.0,
        help='Customer share of the increase after the allowed period (default: 70%%)',
    )

    termination_company_share_pct = fields.Float(
        string='Company Share of Increase (%)',
        config_parameter='investment_club.termination_company_share_pct',
        default=30.0,
        help='Company share of the increase after the allowed period (default: 30%%)',
    )

    death_case_allow_transfer = fields.Boolean(
        string='Allow Ownership Transfer in Death Case',
        config_parameter='investment_club.death_case_allow_transfer',
        default=True,
        help='Allow ownership transfer to an heir in case of death',
    )

    death_case_allow_terminate = fields.Boolean(
        string='Allow Terminate & Distribute in Death Case',
        config_parameter='investment_club.death_case_allow_terminate',
        default=True,
        help='Allow termination and distribution in case of death',
    )

    death_case_deduction_pct = fields.Float(
        string='Death Case Deduction (%)',
        config_parameter='investment_club.death_case_deduction_pct',
        default=0.0,
        help='Death case deduction percentage (0 = no deduction) = No deduction)',
    )

    death_case_require_inheritance_doc = fields.Boolean(
        string='Require Inheritance Document',
        config_parameter='investment_club.death_case_require_inheritance_doc',
        default=True,
        help='Require inheritance certificate attachment for death cases',
    )

    # ===== Report Settings =====
    report_company_header = fields.Boolean(
        string='Show Company Header in Reports',
        config_parameter='investment_club.report_company_header',
        default=True,
        help='Show company logo and details in PDF report headers.',
    )

    report_show_currency = fields.Boolean(
        string='Show Currency Symbol in Reports',
        config_parameter='investment_club.report_show_currency',
        default=True,
        help='Display currency symbols next to amounts in reports.',
    )
