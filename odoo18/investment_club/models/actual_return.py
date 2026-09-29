# investment_club/models/actual_return.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class InvestmentActualReturn(models.Model):
    _name = 'investment.actual.return'
    _description = 'Actual Return Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_from desc'

    name = fields.Char(
        string='Reference',
        readonly=True,
        copy=False,
        default='New'
    )

    subscription_id = fields.Many2one(
        'investment.subscription',
        string='Investment',
        required=True,
        ondelete='cascade'
    )

    membership_id = fields.Many2one(
        'investment.membership',
        related='subscription_id.membership_id',
        string='Membership',
        store=True,
        readonly=True
    )

    partner_id = fields.Many2one(
        'res.partner',
        related='subscription_id.partner_id',
        string='Investor',
        store=True,
        readonly=True
    )

    project_id = fields.Many2one(
        'investment.project',
        related='subscription_id.project_id',
        string='Project',
        store=True,
        readonly=True
    )

    # ===== Return Type =====
    return_type = fields.Selection([
        ('return_1', 'Return 1 (One-time)'),
        ('return_2', 'Return 2 (Recurring)'),
    ], string='Return Type', default='return_2', required=True)

    period_name = fields.Char(
        string='Period',
        compute='_compute_period_name',
        store=True
    )

    date_from = fields.Date(string='From Date', required=True)
    date_to = fields.Date(string='To Date', required=True)

    expected_amount = fields.Float(
        string='Expected Amount',
        compute='_compute_expected_amount',
        store=True,
        readonly=True
    )

    actual_amount = fields.Float(
        string='Actual Amount',
        required=True,
        help='Actual amount paid to the customer',
        default=0.0
    )

    difference = fields.Float(
        string='Difference',
        compute='_compute_difference',
        store=True
    )

    payment_journal_id = fields.Many2one(
        'account.journal',
        string='Payment Journal',
        domain="[('type', 'in', ('bank', 'cash'))]"
    )

    payment_id = fields.Many2one(
        'account.payment',
        string='Payment',
        readonly=True,
        copy=False
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    notes = fields.Text(string='Notes')

    company_id = fields.Many2one(
        'res.company',
        related='subscription_id.company_id',
        store=True
    )

    @api.depends('subscription_id', 'return_type', 'date_from', 'date_to')
    def _compute_expected_amount(self):
        for rec in self:
            if not rec.subscription_id:
                rec.expected_amount = 0.0
                continue

            sub = rec.subscription_id

            if rec.return_type == 'return_1':
                # First Return (One-time)
                rec.expected_amount = (sub.return_1_amount or 0.0) * sub.share_count
            else:
                # Second Return (Recurring)
                if sub.return_2_amount > 0:
                    rec.expected_amount = sub.return_2_amount * sub.share_count
                elif sub.return_2_percentage > 0:
                    rec.expected_amount = (sub.return_2_percentage / 100) * sub.amount
                else:
                    rec.expected_amount = sub.expected_period_return or 0.0

    @api.depends('expected_amount', 'actual_amount')
    def _compute_difference(self):
        for rec in self:
            rec.difference = rec.actual_amount - rec.expected_amount

    @api.depends('return_type', 'date_from', 'date_to', 'subscription_id')
    def _compute_period_name(self):
        for rec in self:
            if rec.return_type == 'return_1':
                date_str = rec.date_from.strftime('%B %Y') if rec.date_from else ''
                # Count how many return_1 exist before this one to show occurrence number
                if rec.subscription_id:
                    existing = rec.subscription_id.actual_return_ids.filtered(
                        lambda r: r.return_type == 'return_1' and r.state != 'cancelled'
                    )
                    occ = len(existing)
                    rec.period_name = _('Return 1 (#%s) - %s') % (occ, date_str)
                else:
                    rec.period_name = _('Return 1 - %s') % date_str
            else:
                if rec.date_from and rec.date_to:
                    rec.period_name = '%s - %s' % (
                        rec.date_from.strftime('%B %Y'),
                        rec.date_to.strftime('%B %Y')
                    )
                else:
                    rec.period_name = _('Return 2')

    @api.onchange('subscription_id', 'return_type')
    def _onchange_subscription(self):
        if not self.subscription_id:
            return

        sub = self.subscription_id
        today = fields.Date.today()

        # ===== Return 1 (with repeat duration / while membership active) =====
        if self.return_type == 'return_1':
            if sub.return_1_amount <= 0:
                raise UserError(_(
                    'Return 1 is not configured for this project!\n'
                    'Please set Return 1 Amount in the project.'
                ))

            # Check how many Return 1 payments already exist
            return_1_exists = sub.actual_return_ids.filtered(
                lambda r: r.return_type == 'return_1' and r.state != 'cancelled'
            )
            occurrence_index = len(return_1_exists)  # 0-based index

            # ===== Limit check =====
            if sub.return_1_repeat_until_membership:
                # Repeats as long as the membership is still valid
                membership = sub.membership_id
                if not membership or membership.state != 'active':
                    raise UserError(_(
                        'Return 1 repeats only while the membership is active!\n'
                        'Current membership status: %s'
                    ) % (membership.state if membership else 'N/A'))
                if membership.expiry_date and membership.expiry_date < today:
                    raise UserError(_(
                        'Return 1 repeats only while the membership is valid!\n'
                        'Membership expired on: %s'
                    ) % membership.expiry_date.strftime('%Y-%m-%d'))
            else:
                # Fixed repeat count mode
                repeat_count = sub.return_1_repeat_count or 1
                if occurrence_index >= repeat_count:
                    raise UserError(_(
                        'Return 1 has already been created %s time(s) for this investment!\n'
                        'Maximum repeat count is %s.'
                    ) % (occurrence_index, repeat_count))

            # ===== Calculate the date for this Return 1 payment =====
            # Return 1 Payment Date is optional: fallback to investment date or today
            base_date = sub.return_1_date or sub.investment_date or today
            repeat_duration = sub.return_1_repeat_duration or 0

            if repeat_duration > 0 and occurrence_index > 0:
                # Each occurrence is spaced by repeat_duration months
                payment_date = base_date + relativedelta(months=repeat_duration * occurrence_index)
            else:
                payment_date = base_date

            if today < payment_date:
                raise UserError(_(
                    'Return 1 date (%s) is in the future!\n'
                    'Please wait until the payment date.'
                ) % payment_date.strftime('%Y-%m-%d'))
            
            self.date_from = payment_date
            self.date_to = payment_date
            self.expected_amount = sub.return_1_amount * sub.share_count
            self.actual_amount = self.expected_amount
            return

        # ===== Return 2 (Recurring) =====
        # Check grace period
        if not sub.grace_period_passed:
            diff = relativedelta(sub.returns_start_date, today)
            months_remaining = diff.months + (diff.years * 12)
            days_remaining = (sub.returns_start_date - today).days

            raise UserError(_(
                '⛔ A return payment cannot be created now!\n\n'
                'Grace period: %s months\n'
                'Investment date: %s\n'
                'Return start date: %s\n\n'
                'Time remaining: %s month (%s days)\n\n'
                'You can create the return payment after: %s'
            ) % (
                sub.return_2_grace_months or sub.grace_period_months or 0,
                sub.investment_date,
                sub.returns_start_date,
                months_remaining,
                days_remaining,
                sub.returns_start_date.strftime('%Y-%m-%d') if sub.returns_start_date else 'N/A'
            ))

        # Calculate next period
        return_2_returns = sub.actual_return_ids.filtered(
            lambda r: r.return_type == 'return_2' and r.state != 'cancelled'
        )
        if return_2_returns:
            last_return = return_2_returns.sorted('date_to', reverse=True)[0]
            next_date_from = last_return.date_to + timedelta(days=1)
        else:
            next_date_from = sub.return_2_first_date or sub.returns_start_date

        if not next_date_from:
            raise UserError(_('Error: Return start date is not defined!'))

        if next_date_from > today:
            raise UserError(_(
                '⏳ Next return date (%s) is in the future!'
            ) % next_date_from.strftime('%Y-%m-%d'))

        # Check last date
        if sub.return_2_last_date and next_date_from > sub.return_2_last_date:
            raise UserError(_(
                'All return payments have been completed!\n'
                'Last return date was: %s'
            ) % sub.return_2_last_date.strftime('%Y-%m-%d'))

        self.date_from = next_date_from
        period_months = sub.return_2_period_months or 1
        self.date_to = next_date_from + relativedelta(months=period_months, days=-1)

        if sub.return_2_last_date and self.date_to > sub.return_2_last_date:
            self.date_to = sub.return_2_last_date

        # Calculate expected amount
        if sub.return_2_amount > 0:
            self.expected_amount = sub.return_2_amount * sub.share_count
        elif sub.return_2_percentage > 0:
            self.expected_amount = (sub.return_2_percentage / 100) * sub.amount
        else:
            self.expected_amount = sub.expected_period_return or 0.0
        
        self.actual_amount = self.expected_amount

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('investment.actual.return') or 'New'
        return super(InvestmentActualReturn, self).create(vals_list)

    def action_register_payment(self):
        self.ensure_one()

        if not self.payment_journal_id:
            raise UserError(_('Please select payment journal!'))

        if self.actual_amount <= 0:
            raise UserError(_('Actual amount must be greater than zero!'))

        payment_vals = {
            'payment_type': 'outbound',
            'partner_type': 'customer',
            'partner_id': self.partner_id.id,
            'journal_id': self.payment_journal_id.id,
            'amount': self.actual_amount,
            'date': fields.Date.today(),
            'memo': _('Return Payment - %s - %s [%s]') % (self.period_name, self.subscription_id.name, self.return_type),
        }

        payment = self.env['account.payment'].create(payment_vals)
        payment.action_post()

        self.write({
            'payment_id': payment.id,
            'state': 'paid'
        })

    def action_cancel(self):
        if self.payment_id and self.payment_id.state == 'posted':
            self.payment_id.action_cancel()
        self.write({'state': 'cancelled'})

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.period_name} - {record.actual_amount:,.2f}"
            result.append((record.id, name))
        return result
