# investment_club/models/investment_project.py
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class InvestmentProject(models.Model):
    _name = 'investment.project'
    _description = 'Investment Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Project Name', required=True, tracking=True)
    code = fields.Char(string='Project Code', readonly=True, copy=False)

    club_id = fields.Many2one(
        'investment.club',
        string='Club',
        required=True,
        ondelete='cascade'
    )

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account',
        required=True
    )

    share_value = fields.Float(string='Share Value', required=True)

    # ===== Contract Settings =====
    contract_start_date = fields.Date(
        string='Contract Start Date',
        default=fields.Date.today,
        help='Contract Start Date'
    )

    contract_end_date = fields.Date(
        string='Contract End Date',
        help='Contract End Date'
    )

    max_shares_per_investor = fields.Integer(
        string='Max Shares per Investor',
        default=0,
        help='Maximum shares per investor (0 = No limit)'
    )

    max_investors = fields.Integer(
        string='Max Investors',
        default=0,
        help='Maximum investors in the project (0 = No limit)'
    )

    active_investor_count = fields.Integer(
        string='Active Investors Count',
        compute='_compute_active_investor_count',
        help='Current active investor count in the project'
    )

    # Comment translated/normalized to English.
    similar_items_count = fields.Integer(
        string='Number of Similar Items',
        default=1,
        help='Number of identical units'
    )

    admin_fees_value = fields.Float(
        string='Administrative Fees Value',
        default=0.0,
        help='Administrative fee amount'
    )

    # ===== Return 1 - One-time Return =====
    return_1_amount = fields.Float(
        string='Return 1 Amount',
        default=0.0,
        help='First Investment Return (One-time)'
    )

    return_1_grace_months = fields.Integer(
        string='Return 1 Grace Period (Months)',
        default=0,
        help='Grace period before first return payment (months)'
    )

    return_1_date = fields.Date(
        string='Return 1 Payment Date',
        help='First Return Payment Date'
    )

    return_1_repeat_count = fields.Integer(
        string='Return 1 Repeat Count',
        default=1,
        help='Number of repetitions for the first investment return'
    )

    return_1_repeat_duration = fields.Integer(
        string='Return 1 Repeat Duration (Months)',
        default=0,
        help='First investment return repetition duration (months)'
    )

    return_1_repeat_until_membership = fields.Boolean(
        string='Repeat Return 1 While Membership Active',
        default=False,
        help='If enabled, Return 1 keeps repeating every (Repeat Duration) months '
             'as long as the membership is still valid - the Repeat Count is ignored.'
    )

    # ===== Return 2 - Recurring Return =====
    return_2_amount = fields.Float(
        string='Return 2 Amount',
        default=0.0,
        help='Second Return Amount (Recurring)'
    )

    return_2_percentage = fields.Float(
        string='Return 2 Percentage (%)',
        default=0.0,
        help='Second Return Rate on Investment'
    )

    return_2_partner_share = fields.Char(
        string='Partner Share Ratio',
        help='Participation ratio, e.g. 60:40',
        default=''
    )

    return_2_grace_months = fields.Integer(
        string='Return 2 Grace Period (Months)',
        default=0,
        help='Grace period before second return starts (months)'
    )

    return_2_period_months = fields.Integer(
        string='Return 2 Period (Months)',
        default=1,
        help='Second return payment frequency (months) - 0 = No There is'
    )

    return_2_duration_years = fields.Integer(
        string='Return 2 Duration (Years)',
        default=0,
        help='Second return repetition duration (years) - 0 = No There is'
    )

    return_2_first_date = fields.Date(
        string='Return 2 First Payment Date',
        help='Second Return First Payment Date'
    )

    return_2_last_date = fields.Date(
        string='Return 2 Last Payment Date',
        help='Second Return Last Payment Date'
    )

    # ===== Terms & Conditions =====
    terms_conditions = fields.Text(
        string='Terms and Conditions',
        help='Project-specific terms and conditions'
    )

    # ===== Legacy fields (kept for compatibility, computed from new fields) =====
    grace_period_months = fields.Integer(
        string='Grace Period (Months)',
        compute='_compute_grace_period',
        store=True,
        help='General grace period (taken from second return)'
    )

    return_percentage = fields.Float(
        string='Return Percentage (%)',
        compute='_compute_return_percentage',
        store=True,
        help='Return rate (from second return)'
    )

    fixed_return_amount = fields.Float(
        string='Fixed Return Amount per Period',
        compute='_compute_fixed_return',
        store=True,
        help='Fixed return amount (from second return)'
    )

    capital_return_period = fields.Integer(
        string='Capital Return Period (Months)',
        default=0,
        help='Number of months until full principal is returned'
    )

    # ===== Status =====
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed')
    ], string='Status', default='draft', tracking=True)

    active = fields.Boolean(default=True)

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    description = fields.Text(string='Description')

    # ===== Compute Methods =====
    def _compute_active_investor_count(self):
        for project in self:
            active_states = ('draft', 'reviewed', 'pending_approval', 'approved', 'paid', 'active')
            project.active_investor_count = self.env['investment.subscription'].search_count([
                ('project_id', '=', project.id),
                ('state', 'in', active_states),
            ])

    def _get_active_investor_count(self):
        """Return the active investor count (usable from other models)."""
        active_states = ('draft', 'reviewed', 'pending_approval', 'approved', 'paid', 'active')
        return self.env['investment.subscription'].search_count([
            ('project_id', '=', self.id),
            ('state', 'in', active_states),
        ])

    def _check_max_investors(self):
        """Check if the project can accept more investors. Returns True if OK, False if full."""
        self.ensure_one()
        if self.max_investors <= 0:
            return True
        current_count = self._get_active_investor_count()
        return current_count < self.max_investors

    @api.depends('return_2_grace_months')
    def _compute_grace_period(self):
        for project in self:
            project.grace_period_months = project.return_2_grace_months

    @api.depends('return_2_percentage')
    def _compute_return_percentage(self):
        for project in self:
            project.return_percentage = project.return_2_percentage

    @api.depends('return_2_amount')
    def _compute_fixed_return(self):
        for project in self:
            project.fixed_return_amount = project.return_2_amount

    # ===== Validation =====
    @api.constrains('return_2_period_months')
    def _check_return_2_period(self):
        for project in self:
            if project.return_2_amount > 0 or project.return_2_percentage > 0:
                if project.return_2_period_months <= 0:
                    raise ValidationError(_(
                        'Return 2 Period must be greater than 0 when Return 2 Amount or Percentage is set!'
                    ))

    # NOTE: Return 1 Payment Date (return_1_date) is now OPTIONAL.
    # The old constraint that forced return_1_date when return_1_amount > 0
    # was removed. When the date is empty, the system falls back to the
    # investment date (or today) as the base date for Return 1 payments.

    @api.constrains('contract_start_date', 'contract_end_date')
    def _check_contract_dates(self):
        for project in self:
            if project.contract_start_date and project.contract_end_date:
                if project.contract_end_date < project.contract_start_date:
                    raise ValidationError(_(
                        'Contract End Date must be after Contract Start Date!'
                    ))

    # ===== CRUD =====
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('investment.project') or 'New'
        return super(InvestmentProject, self).create(vals_list)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_close(self):
        self.write({'state': 'closed'})
