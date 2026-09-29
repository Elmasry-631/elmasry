# investment_club/models/investment_subscription.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class InvestmentSubscription(models.Model):
    _name = 'investment.subscription'
    _description = 'Investment Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    # ===== Basic Fields =====

    name = fields.Char(
        string='Reference',
        readonly=True,
        copy=False,
        default='New'
    )

    membership_id = fields.Many2one(
        'investment.membership',
        string='Membership',
        required=True,
        ondelete='cascade'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Investor',
        related='membership_id.partner_id',
        store=True,
        readonly=True
    )

    club_id = fields.Many2one(
        'investment.club',
        string='Club',
        related='membership_id.club_id',
        store=True,
        readonly=True
    )

    project_id = fields.Many2one(
        'investment.project',
        string='Investment Project',
        required=True,
        domain="[('club_id', '=', club_id), ('state', '=', 'active')]"
    )

    # ===== Project Return Settings (from project) =====

    # --- First Return ---
    return_1_amount = fields.Float(
        related='project_id.return_1_amount',
        string='Return 1 Amount',
        readonly=True,
        store=True
    )
    return_1_grace_months = fields.Integer(
        related='project_id.return_1_grace_months',
        string='Return 1 Grace (Months)',
        readonly=True,
        store=True
    )
    return_1_date = fields.Date(
        related='project_id.return_1_date',
        string='Return 1 Date',
        readonly=True,
        store=True
    )
    return_1_repeat_count = fields.Integer(
        related='project_id.return_1_repeat_count',
        string='Return 1 Repeat Count',
        readonly=True,
        store=True
    )
    return_1_repeat_duration = fields.Integer(
        related='project_id.return_1_repeat_duration',
        string='Return 1 Repeat Duration (Months)',
        readonly=True,
        store=True
    )
    return_1_repeat_until_membership = fields.Boolean(
        related='project_id.return_1_repeat_until_membership',
        string='Repeat Return 1 While Membership Active',
        readonly=True,
        store=True
    )

    # --- Second Return ---
    return_2_amount = fields.Float(
        related='project_id.return_2_amount',
        string='Return 2 Amount',
        readonly=True,
        store=True
    )
    return_2_percentage = fields.Float(
        related='project_id.return_2_percentage',
        string='Return 2 Percentage (%)',
        readonly=True,
        store=True
    )
    return_2_partner_share = fields.Char(
        related='project_id.return_2_partner_share',
        string='Partner Share Ratio',
        readonly=True,
        store=True
    )
    return_2_grace_months = fields.Integer(
        related='project_id.return_2_grace_months',
        string='Return 2 Grace (Months)',
        readonly=True,
        store=True
    )
    return_2_period_months = fields.Integer(
        related='project_id.return_2_period_months',
        string='Return 2 Period (Months)',
        readonly=True,
        store=True
    )
    return_2_duration_years = fields.Integer(
        related='project_id.return_2_duration_years',
        string='Return 2 Duration (Years)',
        readonly=True,
        store=True
    )
    return_2_first_date = fields.Date(
        related='project_id.return_2_first_date',
        string='Return 2 First Date',
        readonly=True,
        store=True
    )
    return_2_last_date = fields.Date(
        related='project_id.return_2_last_date',
        string='Return 2 Last Date',
        readonly=True,
        store=True
    )

    # --- General Settings ---
    contract_start_date = fields.Date(
        related='project_id.contract_start_date',
        string='Contract Start Date',
        readonly=True,
        store=True
    )
    contract_end_date = fields.Date(
        related='project_id.contract_end_date',
        string='Contract End Date',
        readonly=True,
        store=True
    )
    max_shares_per_investor = fields.Integer(
        related='project_id.max_shares_per_investor',
        string='Max Shares per Investor',
        readonly=True,
        store=True
    )

    max_investors = fields.Integer(
        related='project_id.max_investors',
        string='Max Investors',
        readonly=True,
        store=True
    )

    # --- Legacy Fields (for compatibility) ---
    grace_period_months = fields.Integer(
        related='project_id.grace_period_months',
        string='Grace Period (Months)',
        readonly=True,
        store=True
    )

    # ===== Investment Details =====

    investment_date = fields.Date(
        string='Investment Date',
        default=fields.Date.today,
        required=True
    )

    share_count = fields.Integer(string='Number of Shares', default=1, required=True)

    share_value = fields.Float(
        string='Share Value',
        related='project_id.share_value',
        readonly=True,
        store=True
    )

    amount = fields.Float(
        string='Investment Amount',
        compute='_compute_amount',
        store=True
    )

    # ===== Computed Dates =====

    returns_start_date = fields.Date(
        string='Returns Start Date',
        compute='_compute_return_dates',
        store=True
    )

    capital_return_date = fields.Date(
        string='Capital Return Date',
        compute='_compute_return_dates',
        store=True
    )

    expected_period_return = fields.Float(
        string='Expected Period Return',
        compute='_compute_return_dates',
        store=True
    )

    # ===== Return Tracking =====

    actual_return_ids = fields.One2many(
        'investment.actual.return',
        'subscription_id',
        string='Actual Returns History'
    )

    total_actual_returns = fields.Float(
        string='Total Actual Returns Paid',
        compute='_compute_total_returns',
        store=True
    )

    last_return_date = fields.Date(
        string='Last Return Date',
        compute='_compute_last_return',
        store=True
    )

    capital_due = fields.Float(
        string='Capital Due',
        compute='_compute_capital_due',
        store=True,
        help='Maturity Principal = Investment amount minus total paid returns'
    )

    grace_period_passed = fields.Boolean(
        string='Grace Period Passed',
        compute='_compute_grace_period_status',
        store=True
    )

    months_until_returns_start = fields.Integer(
        string='Months Until Returns Start',
        compute='_compute_grace_period_status',
        store=True
    )

    days_until_returns_start = fields.Integer(
        string='Days Until Returns Start',
        compute='_compute_grace_period_status',
        store=True
    )

    # ===== Payment =====

    payment_journal_id = fields.Many2one(
        'account.journal',
        string='Payment Journal',
        domain="[('type', 'in', ('bank', 'cash'))]",
        default=lambda self: self.env['account.journal'].search([
            ('type', '=', 'bank'),
            ('company_id', '=', self.env.company.id),
        ], limit=1)
    )

    payment_id = fields.Many2one(
        'account.payment',
        string='Payment',
        readonly=True,
        copy=False
    )

    contract_id = fields.Many2one(
        'sale.contract',
        string='Contract',
        readonly=True,
        copy=False
    )

    contract_printed = fields.Boolean(
        string='Contract Printed',
        default=False,
        tracking=True,
        help='Indicates whether the investment contract has been printed'
    )

    contract_print_date = fields.Date(
        string='Contract Print Date',
        readonly=True,
        copy=False,
        tracking=True
    )

    payment_state = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('paid', 'Paid')
    ], string='Payment Status', default='not_paid', readonly=True)

    admin_fees_amount = fields.Float(
        related='club_id.administrative_fees',
        string='Admin Fees',
        store=True,
        readonly=True,
        help='Administrative fees (from club) added to the investment amount in the payment'
    )

    payment_total_amount = fields.Float(
        compute='_compute_payment_total',
        string='Total (Investment + Admin Fees)',
        store=True,
        help='Total Payment = Investment Amount + Administrative Fees'
    )

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        related='project_id.analytic_account_id',
        string='Analytic Account',
        readonly=True,
        store=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('terminated', 'Terminated'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    approval_user_id = fields.Many2one(
        'res.users',
        string='Approved By',
        readonly=True,
        copy=False
    )

    approval_date = fields.Date(
        string='Approval Date',
        readonly=True,
        copy=False
    )

    rejection_reason = fields.Text(
        string='Rejection Reason',
        readonly=True
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='membership_id.company_id',
        store=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        store=True
    )

    notes = fields.Text(string='Notes')

    # ===== Compute Methods =====

    @api.depends('share_count', 'share_value')
    def _compute_amount(self):
        for sub in self:
            sub.amount = sub.share_count * sub.share_value

    @api.depends('investment_date', 'return_1_grace_months', 'return_2_grace_months',
                 'return_1_amount', 'return_2_amount', 'return_2_period_months',
                 'return_2_percentage', 'share_count', 'amount', 'contract_end_date')
    def _compute_return_dates(self):
        for sub in self:
            if not sub.investment_date:
                sub.returns_start_date = False
                sub.capital_return_date = False
                sub.expected_period_return = 0.0
                continue

            # Returns start: based on return_2_grace_months (main grace period)
            grace_months = sub.return_2_grace_months or sub.grace_period_months or 3
            sub.returns_start_date = sub.investment_date + relativedelta(months=grace_months)

            # Capital return date (contract end)
            if sub.contract_end_date:
                sub.capital_return_date = sub.contract_end_date
            else:
                sub.capital_return_date = False

            # Expected return per period (Return 2 amount)
            if sub.return_2_amount > 0:
                sub.expected_period_return = sub.return_2_amount * sub.share_count
            elif sub.return_2_percentage > 0:
                sub.expected_period_return = (sub.return_2_percentage / 100) * sub.amount
            else:
                sub.expected_period_return = 0.0

    @api.depends('returns_start_date', 'investment_date')
    def _compute_grace_period_status(self):
        today = fields.Date.today()
        for sub in self:
            if not sub.returns_start_date or not sub.investment_date:
                sub.grace_period_passed = False
                sub.months_until_returns_start = 0
                sub.days_until_returns_start = 0
                continue

            sub.grace_period_passed = today >= sub.returns_start_date

            if sub.grace_period_passed:
                sub.months_until_returns_start = 0
                sub.days_until_returns_start = 0
            else:
                diff = relativedelta(sub.returns_start_date, today)
                sub.months_until_returns_start = diff.months + (diff.years * 12)
                sub.days_until_returns_start = (sub.returns_start_date - today).days

    @api.depends('actual_return_ids.actual_amount', 'actual_return_ids.state')
    def _compute_total_returns(self):
        for sub in self:
            sub.total_actual_returns = sum(
                sub.actual_return_ids.filtered(lambda r: r.state == 'paid').mapped('actual_amount')
            )

    @api.depends('actual_return_ids')
    def _compute_last_return(self):
        for sub in self:
            paid_returns = sub.actual_return_ids.filtered(lambda r: r.state == 'paid')
            sub.last_return_date = max(paid_returns.mapped('date_to')) if paid_returns else False

    @api.depends('amount', 'total_actual_returns')
    def _compute_capital_due(self):
        for sub in self:
            capital = sub.amount - (sub.total_actual_returns or 0.0)
            sub.capital_due = max(capital, 0.0)

    @api.depends('amount', 'admin_fees_amount')
    def _compute_payment_total(self):
        for sub in self:
            sub.payment_total_amount = (sub.amount or 0.0) + (sub.admin_fees_amount or 0.0)

    def _allocate_sequence_number(self, sequence, table, column, cache, cache_key):
        """Allocate the first unused number of a year-based sequence.

        Gap-proof logic: the number is computed from the existing data
        instead of the mutable sequence counter, so retried uploads /
        test runs / deleted records never burn numbers (1, 5, 6, 7...).
        Deleted numbers are automatically reused for the next records.

        :return: (prefix, next_number)
        """
        today = fields.Date.context_today(self)
        mapping = {
            'year': today.year,
            'month': today.month,
            'day': today.day,
            'y': today.year % 100,
            'doy': today.timetuple().tm_yday,
            'woy': today.isocalendar()[1],
            'weekday': today.weekday(),
        }
        try:
            prefix = (sequence.prefix or '') % mapping
        except (KeyError, ValueError, TypeError):
            prefix = sequence.prefix or ''

        if cache_key not in cache:
            # Lock the sequence row: serializes concurrent allocations
            self.env.cr.execute(
                "SELECT id FROM ir_sequence WHERE id = %s FOR UPDATE",
                [sequence.id],
            )
            self.env.cr.execute(
                "SELECT %s FROM %s WHERE %s LIKE %%s" % (column, table, column),
                [prefix + '%'],
            )
            used = set()
            for (val,) in self.env.cr.fetchall():
                try:
                    used.add(int(str(val)[len(prefix):]))
                except (TypeError, ValueError):
                    continue
            cache[cache_key] = used
        else:
            used = cache[cache_key]

        next_num = 1
        while next_num in used:
            next_num += 1
        used.add(next_num)
        return prefix, next_num

    # ===== CRUD Overrides =====

    @api.model_create_multi
    def create(self, vals_list):
        seq_cache = {}
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                # Gap-proof number: first unused INV/.../xxxxx (from data)
                seq = self.env['ir.sequence'].sudo().search([
                    ('code', '=', 'investment.subscription'),
                ], limit=1)
                if seq:
                    prefix, num = self._allocate_sequence_number(
                        seq, 'investment_subscription', 'name',
                        seq_cache, 'investment.subscription',
                    )
                    vals['name'] = '%s%s' % (prefix, str(num).zfill(seq.padding or 5))
                else:
                    vals['name'] = self.env['ir.sequence'].next_by_code('investment.subscription') or 'New'

            # Check max investors limit before creating subscription
            project_id = vals.get('project_id')
            if project_id:
                project = self.env['investment.project'].browse(project_id)
                if project.max_investors > 0:
                    active_states = ('draft', 'reviewed', 'pending_approval', 'approved', 'paid', 'active')
                    current_count = self.env['investment.subscription'].search_count([
                        ('project_id', '=', project_id),
                        ('state', 'in', active_states),
                    ])
                    if current_count >= project.max_investors:
                        raise ValidationError(_(
                            'Maximum number of investors reached for this project!\n'
                            'Maximum number of investors (%s) in this project (%s)已被达到!\n'
                            'New investors cannot be added until an existing investor terminates their subscription.'
                        ) % (project.max_investors, project.name))

        records = super(InvestmentSubscription, self).create(vals_list)

        # Auto-create the payment in DRAFT state (draft payment)
        if not self.env.context.get('investment_club_no_auto_payment'):
            records._auto_create_draft_payment()

        return records

    def copy(self, default=None):
        """Reset payment and status fields on duplicate."""
        default = dict(default or {})
        default['name'] = 'New'
        default['payment_id'] = False
        default['payment_state'] = 'not_paid'
        default['state'] = 'draft'
        return super().copy(default)

    def write(self, vals):
        # Check max investors when changing project_id on existing subscription
        if vals.get('project_id'):
            new_project = self.env['investment.project'].browse(vals['project_id'])
            if new_project.max_investors > 0:
                active_states = ('draft', 'reviewed', 'pending_approval', 'approved', 'paid', 'active')
                current_count = self.env['investment.subscription'].search_count([
                    ('project_id', '=', new_project.id),
                    ('state', 'in', active_states),
                ])
                if current_count >= new_project.max_investors:
                    raise ValidationError(_(
                        'Maximum number of investors reached for this project!\n'
                        'Maximum number of investors (%s) in this project (%s) Limit reached!\n'
                        'New investors cannot be added until an existing investor terminates their subscription.'
                    ) % (new_project.max_investors, new_project.name))
        return super(InvestmentSubscription, self).write(vals)

    # ===== Validation =====
    @api.constrains('share_count', 'max_shares_per_investor')
    def _check_max_shares(self):
        for sub in self:
            if sub.max_shares_per_investor > 0 and sub.share_count > sub.max_shares_per_investor:
                raise ValidationError(_(
                    'Maximum shares per investor is %s! You selected %s shares.'
                ) % (sub.max_shares_per_investor, sub.share_count))

    # ===== Actions =====

    def _get_config(self, key, default=False):
        """Read a config parameter value."""
        return self.env['ir.config_parameter'].sudo().get_param(
            'investment_club.%s' % key, default
        )

    def action_submit_approval(self):
        """Submit investment for manager approval."""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft investments can be submitted for approval!'))
        self.write({'state': 'pending_approval'})
        self.message_post(
            body=_('Investment submitted for approval.'),
            partner_ids=[],
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
        )

    def action_approve(self):
        """Approve the investment (manager action)."""
        self.ensure_one()
        if self.state != 'pending_approval':
            raise UserError(_('Only pending investments can be approved!'))
        self.write({
            'state': 'approved',
            'approval_user_id': self.env.uid,
            'approval_date': fields.Date.today(),
        })
        self.message_post(
            body=_('Investment approved by %s.') % self.env.user.name,
            partner_ids=[],
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
        )

    def action_reject(self):
        """Reject the investment (manager action)."""
        self.ensure_one()
        if self.state != 'pending_approval':
            raise UserError(_('Only pending investments can be rejected!'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reject Investment'),
            'res_model': 'investment.subscription.reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_subscription_id': self.id},
        }
    def action_review_money_bank_inv(self):
        for rec in self:
            rec.state = 'reviewed'

    def action_register_payment(self):
        self.ensure_one()

        if self._get_config('require_approval_for_investment', 'False') == 'True':
            if self.state not in ('approved', 'draft'):
                raise UserError(_('Investment must be approved before payment!'))

        # A draft payment is created automatically with the investment:
        # this button only confirms (posts) it. The investment is then
        # ACTIVATED automatically (state -> active + contract generated).
        if self.payment_id:
            if self.payment_id.state == 'cancelled':
                # Revive a cancelled payment (e.g. investment was cancelled
                # then re-opened): bring it back to draft then post it.
                self.payment_id.action_draft()
            if self.payment_id.state != 'draft':
                raise UserError(_('A payment is already registered for this investment!'))
            self.payment_id.action_post()
            # Activation (state -> active + contract) is done by the
            # payment post hook; called again here just in case.
            self._activate_after_payment()
            return {
                'type': 'ir.actions.act_window',
                'name': 'Payment',
                'res_model': 'account.payment',
                'res_id': self.payment_id.id,
                'view_mode': 'form',
            }

        if not self.payment_journal_id:
            raise UserError(_('Please select payment journal!'))

        admin_fees = self.admin_fees_amount or 0.0
        total = self.amount + admin_fees if admin_fees > 0 else self.amount

        if admin_fees > 0:
            memo = _('Investment %s - %s (Participation: %s + Admin Fees: %s)') % (
                self.name, self.project_id.name, self.amount, admin_fees,
            )
        else:
            memo = _('Investment %s - %s') % (self.name, self.project_id.name)

        payment_vals = {
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'partner_id': self.partner_id.id,
            'investment_subscription_id': self.id,
            'journal_id': self.payment_journal_id.id,

            'amount': total,
            'currency_id': self.currency_id.id,
            'date': fields.Date.today(),
            'memo': memo,
            # Clear breakdown shown on the payment form
            'investment_amount': self.amount,
            'investment_admin_fees': admin_fees,
        }

        payment = self.env['account.payment'].create(payment_vals)

        if admin_fees > 0:
            self._apply_admin_fees_split(payment, self.amount, admin_fees)

        payment.action_post()

        if self.project_id.analytic_account_id:
            payment.move_id.line_ids.write({
                'analytic_distribution': {str(self.project_id.analytic_account_id.id): 100},
            })

        # Activation (state -> active + contract) is done by the payment
        # post hook; called again here just in case.
        self._activate_after_payment()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment',
            'res_model': 'account.payment',
            'res_id': payment.id,
            'view_mode': 'form',
        }

    def _get_fallback_payment_journal(self):
        """Return the first bank/cash journal of the investment company."""
        company = self.company_id or self.env.company
        return self.env['account.journal'].search([
            ('type', 'in', ('bank', 'cash')),
            ('company_id', '=', company.id),
        ], limit=1)

    def _get_admin_fees_income_account(self, admin_product):
        """Income account used for the administrative fees journal line."""
        account = False
        if admin_product:
            account = admin_product.property_account_income_id \
                or admin_product.categ_id.property_account_income_categ_id
        if not account:
            company = self.company_id or self.env.company
            account = self.env['account.account'].search([
                ('account_type', '=', 'income'),
                ('company_id', '=', company.id),
            ], limit=1)
        return account

    def _apply_admin_fees_split(self, payment, participation, admin_fees):
        """Split the payment journal entry into two clear lines
        (like the membership invoice):

        - Bank (liquidity) line -> total (participation + admin fees)
        - Receivable line       -> investment amount only
        - Income line           -> administrative fees

        :return: True if the split was applied
        """
        self.ensure_one()
        if admin_fees <= 0:
            return False

        move = payment.move_id
        if not move or move.state != 'draft':
            return False

        receivable_line = move.line_ids.filtered(
            lambda l: l.account_id.account_type == 'asset_receivable' and l.credit > 0
        )[:1]
        if not receivable_line:
            return False

        admin_product = self.env['investment.membership']._get_admin_fees_product()
        income_account = self._get_admin_fees_income_account(admin_product)
        if not income_account:
            return False

        line_vals = {
            'move_id': move.id,
            'account_id': income_account.id,
            'partner_id': receivable_line.partner_id.id,
            'name': _('Administrative Fees - %s') % (self.club_id.name or ''),
            'debit': 0.0,
            'credit': admin_fees,
            'display_type': 'product',
        }
        if receivable_line.currency_id:
            line_vals['currency_id'] = receivable_line.currency_id.id
            line_vals['amount_currency'] = -admin_fees
        if self.project_id.analytic_account_id:
            line_vals['analytic_distribution'] = {
                str(self.project_id.analytic_account_id.id): 100,
            }

        # One atomic write (new income line + reduced receivable line):
        # the entry stays balanced, no intermediate validity error.
        move.with_context(check_move_validity=False).write({
            'line_ids': [
                (0, 0, line_vals),
                (1, receivable_line.id, {
                    'debit': 0.0,
                    'credit': participation,
                    'amount_currency': -participation if receivable_line.currency_id else 0.0,
                }),
            ],
        })
        return True

    def _auto_create_draft_payment(self):
        """Create the investment payment in DRAFT state automatically.

        The payment total = investment amount + administrative fees
        (when configured on the club), and the journal entry is split
        into clear lines like the membership invoice:
        - investment amount (participation)
        - administrative fees
        """
        for sub in self:
            if sub.payment_id or not sub.partner_id:
                continue
            if not sub.amount or sub.amount <= 0:
                continue

            journal = sub.payment_journal_id or sub._get_fallback_payment_journal()
            if not journal:
                sub.message_post(
                    body=_('Draft payment could not be created automatically: no bank/cash journal found!'),
                    message_type='notification',
                )
                continue

            admin_fees = sub.admin_fees_amount or 0.0
            total = sub.amount + admin_fees if admin_fees > 0 else sub.amount

            if admin_fees > 0:
                memo = _('Investment %s - %s (Participation: %s + Admin Fees: %s)') % (
                    sub.name, sub.project_id.name, sub.amount, admin_fees,
                )
            else:
                memo = _('Investment %s - %s') % (sub.name, sub.project_id.name)

            try:
                payment = self.env['account.payment'].create({
                    'payment_type': 'inbound',
                    'partner_type': 'customer',
                    'partner_id': sub.partner_id.id,
                    'investment_subscription_id': sub.id,
                    'journal_id': journal.id,
                    'amount': total,
                    'currency_id': sub.currency_id.id,
                    'date': sub.investment_date or fields.Date.today(),
                    'memo': memo,
                    # Clear breakdown shown on the payment form
                    'investment_amount': sub.amount,
                    'investment_admin_fees': admin_fees,
                })
                if admin_fees > 0:
                    sub._apply_admin_fees_split(payment, sub.amount, admin_fees)
            except Exception as e:
                # Never block record creation/import because of the payment
                sub.message_post(
                    body=_('Draft payment could not be created automatically: %s') % e,
                    message_type='notification',
                )
                continue

            sub.write({
                'payment_id': payment.id,
                'payment_journal_id': journal.id,
            })

    def _activate_after_payment(self):
        """Activate the investment automatically once its payment is posted.

        - payment_state -> paid
        - state         -> active (skipping the manual 'paid' step)
        - the sale contract is generated automatically as well

        Safe to call several times (idempotent).
        """
        for sub in self:
            if sub.state in ('active', 'closed', 'terminated', 'cancelled'):
                if sub.payment_state != 'paid':
                    sub.write({'payment_state': 'paid'})
                continue

            sub.write({'payment_state': 'paid'})

            # Generate the contract silently (never block activation)
            try:
                sub._get_or_create_sale_contract()
            except Exception as e:
                sub.message_post(
                    body=_('Contract could not be generated automatically: %s') % e,
                    message_type='notification',
                )

            sub.write({'state': 'active'})
            sub.message_post(
                body=_('<b>Investment activated automatically after payment confirmation</b>'),
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

    def _sync_after_payment_cancel(self):
        """Put the investment back to draft when its payment is cancelled."""
        for sub in self:
            if sub.state in ('paid', 'active'):
                sub.write({'payment_state': 'not_paid', 'state': 'draft'})
                sub.message_post(
                    body=_('<b>Investment payment cancelled</b> — Subscription reset to draft.'),
                    message_type='notification',
                    subtype_xmlid='mail.mt_comment',
                )
            elif sub.payment_state != 'not_paid':
                sub.write({'payment_state': 'not_paid'})

    def action_reset_to_draft(self):
        """Re-open a cancelled/rejected investment (back to draft)."""
        for sub in self:
            if sub.state not in ('cancelled', 'rejected'):
                raise UserError(_(
                    'Only cancelled or rejected investments can be reset to draft!'
                ))
            sub.write({
                'state': 'draft',
                'payment_state': 'not_paid',
                'rejection_reason': False,
            })
            sub.message_post(
                body=_('<b>Investment reset to draft</b>'),
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

    def action_activate(self):
        self.ensure_one()
        if self.state == 'active':
            # Already active: just open the contract
            contract = self._get_or_create_sale_contract()
            return {
                'type': 'ir.actions.act_window',
                'name': _('Contract'),
                'res_model': 'sale.contract',
                'res_id': contract.id,
                'view_mode': 'form',
                'target': 'current',
            }
        if self.payment_state != 'paid':
            raise UserError(_('Investment must be paid first!'))
        self.write({'state': 'active'})
        contract = self._get_or_create_sale_contract()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Contract'),
            'res_model': 'sale.contract',
            'res_id': contract.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_contract(self):
        self.ensure_one()
        contract = self._get_or_create_sale_contract()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Contract'),
            'res_model': 'sale.contract',
            'res_id': contract.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_payment(self):
        self.ensure_one()
        if not self.payment_id:
            return False
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payment'),
            'res_model': 'account.payment',
            'res_id': self.payment_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_print_contract(self):
        self.ensure_one()
        if not self.contract_id:
            raise UserError(_('No contract found for this investment!'))
        self.write({
            'contract_printed': True,
            'contract_print_date': fields.Date.today(),
        })
        self.message_post(
            body=_('Contract printed on %s.') % fields.Date.today().strftime('%Y-%m-%d'),
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
        )
        return self.contract_id.print_contract_report()

    def action_mark_contract_printed(self):
        """Manually mark contract as printed without printing."""
        self.ensure_one()
        if not self.contract_id:
            raise UserError(_('No contract found for this investment!'))
        self.write({
            'contract_printed': True,
            'contract_print_date': fields.Date.today(),
        })
        self.message_post(
            body=_('Contract marked as printed on %s.') % fields.Date.today().strftime('%Y-%m-%d'),
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
        )

    def _get_or_create_sale_contract(self):
        self.ensure_one()
        if self.contract_id:
            return self.contract_id

        contract_template = self.env['contract.template'].search([], limit=1)
        contract_title = self.env['sale.contract.title'].search([], limit=1)
        agreement_text = contract_template.content if contract_template else self._get_default_contract_terms()

        contract = self.env['sale.contract'].create({
            'partner_id': self.partner_id.id,
            'contract_date': self.investment_date or fields.Date.today(),
            'amount_total': self.amount,
            'currency_id': self.currency_id.id,
            'investment_subscription_id': self.id,
            'contract_template_id': contract_template.id if contract_template else False,
            'contract_title_name': contract_title.id if contract_title else False,
            'agreement_terms': agreement_text,
            'note': _('Generated automatically from investment %s.') % self.name,
        })
        self.contract_id = contract.id
        return contract

    def _get_default_contract_terms(self):
        self.ensure_one()
        return """
            <p>This contract is generated automatically for the activated investment subscription.</p>
            <p><strong>Club:</strong> %s</p>
            <p><strong>Project:</strong> %s</p>
            <p><strong>Investment Reference:</strong> %s</p>
            <p><strong>Shares:</strong> %s</p>
            <p><strong>Investment Amount:</strong> %s</p>
            <p><strong>Contract Start Date:</strong> %s</p>
            <p><strong>Contract End Date:</strong> %s</p>
        """ % (
            self.club_id.display_name or '',
            self.project_id.display_name or '',
            self.name or '',
            self.share_count or 0,
            self.amount or 0.0,
            self.contract_start_date or '',
            self.contract_end_date or '',
        )

    def action_create_return(self):
        """Create a return payment based on the unified return system."""
        self.ensure_one()

        if self.state != 'active':
            raise UserError(_('Investment must be active to create returns!'))

        today = fields.Date.today()

        # ===== Snooze period: 3 months from investment_date =====
        snooze_months = 3
        if self.investment_date:
            snooze_end = self.investment_date + relativedelta(months=snooze_months)
            if today < snooze_end:
                remaining = relativedelta(snooze_end, today)
                raise UserError(_(
                    'The grace period has not ended yet!\n\n'
                    'Grace period: %s months\n'
                    'Investment date: %s\n'
                    'The grace period ends on: %s\n\n'
                    'Remaining: %s months and %s day'
                ) % (
                    snooze_months,
                    self.investment_date,
                    snooze_end.strftime('%Y-%m-%d'),
                    remaining.months + (remaining.years * 12),
                    remaining.days,
                ))

        # ===== Check Return 1 (Repeats while membership is active) =====
        if self.return_1_amount > 0:
            # Existing Return 1 payments (any state except cancelled)
            return_1_exists = self.actual_return_ids.filtered(
                lambda r: r.return_type == 'return_1' and r.state != 'cancelled'
            )
            occurrence_index = len(return_1_exists)  # 0-based index

            # Base date: Return 1 Payment Date (optional).
            # Fallback: investment date, otherwise today.
            base_date = self.return_1_date or self.investment_date or today

            # Each occurrence is spaced by the repeat duration (months)
            repeat_duration = self.return_1_repeat_duration or 0
            payment_date = base_date + relativedelta(months=repeat_duration * occurrence_index)

            if today >= payment_date:
                # Check whether a new Return 1 occurrence is allowed
                return_1_allowed = False
                if self.return_1_repeat_until_membership:
                    # Repeat as long as the membership is still valid
                    membership = self.membership_id
                    if membership and membership.state == 'active':
                        if membership.expiry_date and membership.expiry_date < today:
                            return_1_allowed = False
                        else:
                            return_1_allowed = True
                else:
                    # Fixed repeat count mode
                    repeat_count = self.return_1_repeat_count or 1
                    return_1_allowed = occurrence_index < repeat_count

                if return_1_allowed:
                    period_name = _('Return 1 (#%s) - %s') % (
                        occurrence_index + 1,
                        payment_date.strftime('%B %Y')
                    )
                    return_payment = self.env['investment.actual.return'].create({
                        'subscription_id': self.id,
                        'return_type': 'return_1',
                        'date_from': payment_date,
                        'date_to': payment_date,
                        'expected_amount': self.return_1_amount * self.share_count,
                        'actual_amount': self.return_1_amount * self.share_count,
                        'period_name': period_name,
                        'state': 'draft',
                    })
                    return {
                        'type': 'ir.actions.act_window',
                        'name': _('Review Return 1 Payment'),
                        'res_model': 'investment.actual.return',
                        'res_id': return_payment.id,
                        'view_mode': 'form',
                        'target': 'current',
                        'context': {'form_view_initial_mode': 'edit'},
                    }

        # ===== Check grace period for Return 2 =====
        if not self.grace_period_passed:
            diff = relativedelta(self.returns_start_date, today)
            months_remaining = diff.months + (diff.years * 12)
            days_remaining = diff.days

            raise UserError(_(
                'The grace period has not ended yet!\n\n'
                'Grace period: %s Month\n'
                'Investment date: %s\n'
                'Return start date: %s\n\n'
                'Remaining: %s months and %s day\n\n'
                'Returns will be available starting: %s'
            ) % (
                self.return_2_grace_months or self.grace_period_months or 0,
                self.investment_date,
                self.returns_start_date,
                months_remaining,
                days_remaining,
                self.returns_start_date.strftime('%Y-%m-%d') if self.returns_start_date else 'N/A'
            ))

        # ===== Determine period for Return 2 =====
        return_2_returns = self.actual_return_ids.filtered(
            lambda r: r.return_type == 'return_2' and r.state != 'cancelled'
        )
        if return_2_returns:
            last_return = return_2_returns.sorted('date_to', reverse=True)[0]
            next_date_from = last_return.date_to + timedelta(days=1)
        else:
            next_date_from = self.return_2_first_date or self.returns_start_date

        if not next_date_from:
            raise UserError(_(
                'Could not determine return start date!\n'
                'Please check the subscription settings.\n'
                'Investment Date: %s\n'
                'Grace Period: %s months'
            ) % (self.investment_date, self.return_2_grace_months or self.grace_period_months or 0))

        if next_date_from > today:
            raise UserError(_(
                'The next return period starts on %s which is in the future!\n'
                'Please wait until the period begins.'
            ) % next_date_from.strftime('%Y-%m-%d'))

        # Check if past last return date
        if self.return_2_last_date and next_date_from > self.return_2_last_date:
            raise UserError(_(
                'All return payments have been completed!\n'
                'Last return date was: %s'
            ) % self.return_2_last_date.strftime('%Y-%m-%d'))

        # Calculate period end
        period_months = self.return_2_period_months or 1
        next_date_to = next_date_from + relativedelta(months=period_months, days=-1)

        # Check if period exceeds last date
        if self.return_2_last_date and next_date_to > self.return_2_last_date:
            next_date_to = self.return_2_last_date

        # Calculate expected amount
        expected_amount = self.expected_period_return or 0.0

        period_name = '%s / %s' % (
            next_date_from.strftime('%B %Y'),
            self.partner_id.name or 'Unknown'
        )

        try:
            return_payment = self.env['investment.actual.return'].create({
                'subscription_id': self.id,
                'return_type': 'return_2',
                'date_from': next_date_from,
                'date_to': next_date_to,
                'expected_amount': expected_amount,
                'actual_amount': expected_amount,
                'period_name': period_name,
                'state': 'draft',
            })
        except Exception as e:
            raise UserError(_(
                'Failed to create return record:\n%s'
            ) % str(e))

        return {
            'type': 'ir.actions.act_window',
            'name': _('Review Return Payment'),
            'res_model': 'investment.actual.return',
            'res_id': return_payment.id,
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'form_view_initial_mode': 'edit',
            }
        }

    def action_close(self):
        self.write({'state': 'closed'})

    def action_terminate(self):
        """Open investment subscription termination wizard."""
        self.ensure_one()
        if self.state not in ('paid', 'active'):
            raise UserError(_('Only paid or active investments can be terminated!'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Terminate Investment Share'),
            'res_model': 'subscription.terminate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_subscription_id': self.id,
            },
        }

    def action_death_case(self):
        """Open investor death case wizard for this subscription."""
        self.ensure_one()
        if self.state not in ('paid', 'active'):
            raise UserError(_('Only paid or active investments can process death case!'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Investor Death Case'),
            'res_model': 'investor.death.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_membership_id': self.membership_id.id,
                'default_subscription_id': self.id,
            },
        }

    def action_cancel(self):
        """Cancel the investment (and its linked payment)."""
        for sub in self:
            if sub.state == 'cancelled':
                continue
            if sub.payment_id and sub.payment_id.state == 'posted':
                # The payment cancel hook puts the subscription back to
                # draft first; we then mark it cancelled.
                sub.payment_id.action_cancel()
            elif sub.payment_id and sub.payment_id.state == 'draft':
                try:
                    sub.payment_id.unlink()
                except Exception:
                    pass
            sub.write({'state': 'cancelled'})
            sub.message_post(
                body=_('<b>Investment cancelled</b>'),
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

    def name_get(self):
        result = []
        for record in self:
            name = "%s (%s shares)" % (record.project_id.name, record.share_count)
            result.append((record.id, name))
        return result

    # ===== SQL Constraints =====

    _sql_constraints = [
        (
            'unique_name',
            'unique(name)',
            'Investment reference must be unique!'
        ),
    ]
