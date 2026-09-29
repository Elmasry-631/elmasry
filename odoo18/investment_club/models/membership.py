# investment_club/models/membership.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from psycopg2 import IntegrityError
from datetime import timedelta


class InvestmentMembership(models.Model):
    _name = 'investment.membership'
    _description = 'Investment Membership'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'investor_code'

    # ===== Basic Fields =====

    membership_number = fields.Char(
        string='Internal Reference',
        readonly=True,
        copy=False,
        default='New'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        tracking=True,
    )

    club_id = fields.Many2one(
        'investment.club',
        string='Club',
        required=True,
        tracking=True
    )

    membership_product_id = fields.Many2one(
        'product.product',
        string='Membership Product',
        domain="[('type', '=', 'service')]",
        required=True
    )

    initial_membership_fee = fields.Float(
        string='Initial Membership Fee',
        related='membership_product_id.lst_price',
        readonly=True,
        store=True
    )

    subscription_product_id = fields.Many2one(
        'product.product',
        string='Subscription Product',
        domain="[('type', '=', 'service')]"
    )

    annual_subscription_fee = fields.Float(
        string='Annual Subscription Fee',
        required=True
    )

    subscription_period = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly')
    ], string='Subscription Period', default='yearly', required=True)

    membership_date = fields.Date(
        string='Start Date',
        default=fields.Date.today,
        required=True
    )

    expiry_date = fields.Date(
        string='Expiry Date',
        compute='_compute_dates',
        store=True
    )

    auto_renew = fields.Boolean(string='Auto Renew', default=True)

    initial_invoice_id = fields.Many2one(
        'account.move',
        string='Initial Invoice',
        readonly=True,
        copy=False
    )

    current_invoice_id = fields.Many2one(
        'account.move',
        string='Current/Renewal Invoice',
        readonly=True,
        copy=False
    )

    payment_state = fields.Selection(
        related='current_invoice_id.payment_state',
        string='Payment Status',
        readonly=True,
        store=True
    )

    renewal_ids = fields.One2many(
        'membership.renewal',
        'membership_id',
        string='Renewal History'
    )

    next_renewal_date = fields.Date(
        string='Next Renewal Date',
        compute='_compute_next_renewal',
        store=True
    )

    next_renewal_amount = fields.Float(
        string='Next Renewal Amount',
        related='annual_subscription_fee',
        readonly=True,
        store=True
    )

    renewal_status = fields.Selection([
        ('paid', 'Paid'),
        ('due', 'Due'),
        ('overdue', 'Overdue'),
        ('not_due', 'Not Due Yet')
    ], string='Renewal Status', compute='_compute_renewal_status', store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ('initial_invoiced', 'Initial Invoiced'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    investment_ids = fields.One2many(
        'investment.subscription',
        'membership_id',
        string='Investments'
    )

    total_invested = fields.Float(
        string='Total Invested',
        compute='_compute_total',
        store=True
    )

    # ===== Statement Report Fields =====

    total_returns_due = fields.Float(
        string='Total Returns Due',
        compute='_compute_statement_fields',
        store=True,
        help='Total Due Returns'
    )

    total_returns_paid = fields.Float(
        string='Total Returns Paid',
        compute='_compute_statement_fields',
        store=True,
        help='Total Actual Paid Returns'
    )

    returns_remaining = fields.Float(
        string='Returns Remaining',
        compute='_compute_statement_fields',
        store=True,
        help='Remaining = Due Returns - Paid Returns'
    )

    statement_admin_fees = fields.Float(
        string='Admin Fees',
        compute='_compute_statement_fields',
        store=True,
        help='Administrative Fees from Club'
    )

    net_due = fields.Float(
        string='Net Due',
        compute='_compute_statement_fields',
        store=True,
        help='Net Due = Remaining - Administrative Fees'
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        store=True
    )

    notes = fields.Text(string='Notes')

    # ===== Contract Fields =====

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
        help='Indicates whether the membership contract has been printed'
    )

    contract_print_date = fields.Date(
        string='Contract Print Date',
        readonly=True,
        copy=False,
        tracking=True
    )

    # ===== Termination Fields =====

    original_paid_fee = fields.Float(
        string='Original Paid Fee',
        default=0.0,
        help='Amount paid by the customer when membership is activated'
    )

    termination_date = fields.Date(
        string='Termination Date',
        readonly=True,
        copy=False
    )

    termination_reason = fields.Text(
        string='Termination Reason',
        readonly=True
    )

    termination_refund_amount = fields.Float(
        string='Termination Refund Amount',
        readonly=True
    )

    termination_deduction = fields.Float(
        string='Termination Deduction',
        readonly=True,
        help='Termination deduction during the first 3 months'
    )

    investor_code = fields.Char(string='Investor code', store=True)

    invoice_count = fields.Integer(compute='_compute_invoice_count')

    investment_count = fields.Integer(compute='_compute_investment_count')

    contract_count = fields.Integer(compute='_compute_contract_count')

    # ===== Onchange =====

    @api.onchange('subscription_product_id')
    def _onchange_subscription_product(self):
        """Sync annual subscription fee from selected product"""
        if self.subscription_product_id:
            self.annual_subscription_fee = self.subscription_product_id.lst_price

    # ===== Compute Methods =====

    @api.depends('membership_date', 'subscription_period', 'renewal_ids.new_expiry_date')
    def _compute_dates(self):
        """Compute expiry date based on membership date or last renewal."""
        for membership in self:
            if not membership.membership_date:
                membership.expiry_date = False
                continue

            if membership.renewal_ids:
                last_renewal = membership.renewal_ids.sorted('renewal_date', reverse=True)[0]
                membership.expiry_date = last_renewal.new_expiry_date
            else:
                if membership.subscription_period == 'monthly':
                    membership.expiry_date = membership.membership_date + timedelta(days=29)
                elif membership.subscription_period == 'quarterly':
                    membership.expiry_date = membership.membership_date + timedelta(days=89)
                else:  # yearly
                    membership.expiry_date = membership.membership_date + timedelta(days=364)

    @api.depends('expiry_date')
    def _compute_next_renewal(self):
        for membership in self:
            membership.next_renewal_date = membership.expiry_date

    @api.depends('next_renewal_date', 'state')
    def _compute_renewal_status(self):
        today = fields.Date.today()
        for membership in self:
            if membership.state != 'active':
                membership.renewal_status = 'not_due'
            elif not membership.next_renewal_date:
                membership.renewal_status = 'not_due'
            elif membership.next_renewal_date > today:
                membership.renewal_status = 'not_due'
            elif membership.next_renewal_date == today:
                membership.renewal_status = 'due'
            else:
                membership.renewal_status = 'overdue'

    @api.depends('investment_ids.amount', 'investment_ids.state')
    def _compute_total(self):
        for membership in self:
            membership.total_invested = sum(
                membership.investment_ids.filtered(lambda i: i.state == 'active').mapped('amount')
            )

    @api.depends('investment_ids', 'club_id.administrative_fees')
    def _compute_statement_fields(self):
        for mem in self:
            investments = mem.investment_ids.filtered(lambda i: i.state in ('paid', 'active'))

            # Total Due Returns (Total Expected)
            total_due = 0.0
            for inv in investments:
                returns = inv.actual_return_ids.filtered(lambda r: r.state != 'cancelled')
                total_due += sum(r.expected_amount for r in returns)

            # Total Actual Paid Returns
            total_paid = sum(inv.total_actual_returns or 0.0 for inv in investments)

            # Remaining
            remaining = total_due - total_paid

            # Administrative Fees
            admin_fees = mem.club_id.administrative_fees or 0.0

            # Net Due
            net = remaining - admin_fees

            mem.total_returns_due = total_due
            mem.total_returns_paid = total_paid
            mem.returns_remaining = remaining
            mem.statement_admin_fees = admin_fees
            mem.net_due = net

    @api.depends('initial_invoice_id', 'current_invoice_id')
    def _compute_invoice_count(self):
        for rec in self:
            count = 0
            if rec.initial_invoice_id:
                count += 1
            if rec.current_invoice_id and rec.current_invoice_id != rec.initial_invoice_id:
                count += 1
            rec.invoice_count = count

    @api.depends('contract_id')
    def _compute_contract_count(self):
        for rec in self:
            rec.contract_count = 1 if rec.contract_id else 0

    # ===== Actions =====

    def action_create_initial_invoice(self):
        self.ensure_one()

        if not self.investor_code:
            self.investor_code = self._generate_investor_code()

        if not self.membership_product_id:
            raise UserError(_('Please select membership product!'))

        # A draft invoice is created automatically with the membership:
        # this button only confirms (posts) it.
        if self.initial_invoice_id:
            if self.initial_invoice_id.state != 'draft':
                raise UserError(_('Initial invoice already exists!'))
            self.initial_invoice_id.action_post()
            self.write({'state': 'initial_invoiced'})
            # Update ref after post to include invoice number + membership description
            membership_desc = _('Club Membership %s - %s') % (self.club_id.name, self.investor_code or '')
            self.initial_invoice_id.write({
                'ref': '%s - %s' % (self.initial_invoice_id.name, membership_desc),
            })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Invoice',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': self.initial_invoice_id.id,
            }

        invoice = self._prepare_initial_invoice()

        self.write({
            'initial_invoice_id': invoice.id,
            'current_invoice_id': invoice.id,
            'state': 'initial_invoiced'
        })

        invoice.action_post()

        # Update ref after post to include invoice number + membership description
        membership_desc = _('Club Membership %s - %s') % (self.club_id.name, self.investor_code or '')
        invoice.write({
            'ref': '%s - %s' % (invoice.name, membership_desc),
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }

    def _prepare_initial_invoice(self):
        """Build and create the initial membership invoice (kept in DRAFT)."""
        self.ensure_one()

        invoice_lines = [(0, 0, {
            'product_id': self.membership_product_id.id,
            'name': _('Membership Fee %s - %s') % (self.club_id.name, self.investor_code or ''),
            'quantity': 1,
            'price_unit': self.initial_membership_fee,
        })]

        # Add administrative fees as a separate line if configured on the club
        admin_fees = self.club_id.administrative_fees if self.club_id else 0.0
        if admin_fees > 0:
            admin_product = self._get_admin_fees_product()
            invoice_lines.append((0, 0, {
                'product_id': admin_product.id if admin_product else False,
                'name': _('Administrative Fees - %s') % (self.club_id.name,),
                'quantity': 1,
                'price_unit': admin_fees,
            }))

        return self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'investor_code_id': self.id or False,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_lines,
        })

    def _auto_create_initial_draft_invoice(self):
        """Create the initial membership invoice in DRAFT state automatically.

        Called from create() so every new membership (manual or uploaded
        master data) gets its draft invoice ready.
        """
        for membership in self:
            if membership.initial_invoice_id:
                continue
            if not membership.partner_id or not membership.club_id:
                continue
            if not membership.membership_product_id:
                continue
            try:
                invoice = membership._prepare_initial_invoice()
            except Exception as e:
                # Never block record creation/import because of the invoice
                membership.message_post(
                    body=_('Draft invoice could not be created automatically: %s') % e,
                    message_type='notification',
                )
                continue
            membership.write({
                'initial_invoice_id': invoice.id,
                'current_invoice_id': invoice.id,
            })

    def _get_admin_fees_product(self):
        """Get the administrative fees product from settings or create a default one."""
        config_product_id = self._get_config('admin_fees_product_id')
        if config_product_id:
            try:
                return self.env['product.product'].browse(int(config_product_id))
            except (ValueError, TypeError):
                pass
        # Fallback: find or create a generic admin fees product
        admin_product = self.env['product.product'].search([
            ('name', 'ilike', 'Administrative Fee'),
            ('type', '=', 'service'),
        ], limit=1)
        if not admin_product:
            admin_product = self.env['product.product'].search([
                ('name', 'ilike', 'Administrative Fees'),
                ('type', '=', 'service'),
            ], limit=1)
        return admin_product or self.env['product.product']

    def action_open_invoice(self):
        self.ensure_one()

        invoice = self.current_invoice_id or self.initial_invoice_id

        if not invoice:
            raise UserError("No invoice linked to this record.")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }

    def action_create_renewal_invoice(self):
        self.ensure_one()

        if self.annual_subscription_fee <= 0:
            raise UserError(_('Please set annual subscription fee!'))

        renewal_vals = {
            'membership_id': self.id,
            'renewal_date': fields.Date.today(),
            'amount': self.annual_subscription_fee,
            'period': self.subscription_period,
            'old_expiry_date': self.expiry_date,
            'new_expiry_date': self._calculate_new_expiry(),
        }
        renewal = self.env['membership.renewal'].create(renewal_vals)

        product = self.subscription_product_id or self.membership_product_id

        invoice_lines = [(0, 0, {
            'product_id': product.id,
            'name': _('Club Membership Renewal %s - %s') % (self.club_id.name, self.investor_code or ''),
            'quantity': 1,
            'price_unit': self.annual_subscription_fee,
        })]

        # Add administrative fees as a separate line if configured on the club
        admin_fees = self.club_id.administrative_fees if self.club_id else 0.0
        if admin_fees > 0:
            admin_product = self._get_admin_fees_product()
            invoice_lines.append((0, 0, {
                'product_id': admin_product.id if admin_product else False,
                'name': _('Administrative Fees - %s') % (self.club_id.name,),
                'quantity': 1,
                'price_unit': admin_fees,
            }))

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_lines,
        }

        invoice = self.env['account.move'].create(invoice_vals)

        # Post invoice to get the number
        invoice.action_post()

        # Update ref after post to include invoice number + membership description
        membership_desc = _('Club Membership Renewal %s - %s') % (self.club_id.name, self.investor_code or '')
        invoice.write({
            'ref': '%s - %s' % (invoice.name, membership_desc),
        })

        renewal.write({'invoice_id': invoice.id, 'state': 'invoiced'})

        self.write({
            'current_invoice_id': invoice.id,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Renewal Invoice',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
        }

    def action_review_money_bank(self):
        for rec in self:
            rec.state = 'reviewed'


    def _auto_activate_after_payment(self):
        """Activate the membership automatically once its invoice is paid.

        Same logic as the manual "Confirm Payment & Activate" button but
        triggered from the accounting side (invoice fully settled), so
        uploaded memberships become ACTIVE right after payment.

        Safe to call several times (idempotent).
        """
        for membership in self:
            if membership.state in ('active', 'expired', 'terminated', 'cancelled'):
                continue

            vals = {'state': 'active'}
            # Store original paid fee at activation time
            if not membership.original_paid_fee or membership.original_paid_fee <= 0:
                vals['original_paid_fee'] = membership.initial_membership_fee
            membership.write(vals)

            last_renewal = membership.renewal_ids.sorted('renewal_date', reverse=True)[:1]
            if last_renewal and last_renewal.state != 'paid':
                last_renewal.write({'state': 'paid'})

            # ===== Auto-generate Sale Contract (never blocks activation) =====
            try:
                membership._get_or_create_membership_contract()
            except Exception as e:
                membership.message_post(
                    body=_('Contract could not be generated automatically: %s') % e,
                    message_type='notification',
                )

            membership.message_post(
                body=_('<b>Membership activated automatically after invoice payment</b>'),
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

    def action_confirm_payment(self):
        self.ensure_one()
        if self.payment_state == 'paid':
            self._auto_activate_after_payment()

            # ===== Auto-generate Sale Contract =====
            contract = self._get_or_create_membership_contract()
            return {
                'type': 'ir.actions.act_window',
                'name': _('Contract'),
                'res_model': 'sale.contract',
                'res_id': contract.id,
                'view_mode': 'form',
                'target': 'current',
            }
        else:
            raise UserError(_('Invoice is not paid yet!'))

    def _calculate_new_expiry(self):
        """Calculate new expiry starting from the day after current expiry."""
        if not self.expiry_date:
            return fields.Date.today()

        new_start = self.expiry_date + timedelta(days=1)

        if self.subscription_period == 'monthly':
            return new_start + timedelta(days=29)
        elif self.subscription_period == 'quarterly':
            return new_start + timedelta(days=89)
        else:  # yearly
            return new_start + timedelta(days=364)

    def action_terminate(self):
        """Open membership termination wizard."""
        self.ensure_one()
        if self.state not in ('active', 'initial_invoiced'):
            raise UserError(_('Only active memberships can be terminated!'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Terminate Membership'),
            'res_model': 'membership.terminate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_membership_id': self.id,
            },
        }

    def action_death_case(self):
        """Open investor death case wizard."""
        self.ensure_one()
        if self.state not in ('active', 'initial_invoiced'):
            raise UserError(_('Only active memberships can process death case!'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Investor Death Case'),
            'res_model': 'investor.death.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_membership_id': self.id,
            },
        }

    def action_cancel(self):
        """Cancel membership and cancel unpaid related invoices."""
        for membership in self:
            if membership.state == 'cancelled':
                continue
            if membership.current_invoice_id and membership.current_invoice_id.payment_state != 'paid':
                membership.current_invoice_id.button_cancel()
            for renewal in membership.renewal_ids.filtered(lambda r: r.state == 'invoiced'):
                if renewal.invoice_id and renewal.invoice_id.payment_state != 'paid':
                    renewal.invoice_id.button_cancel()
            membership.write({'state': 'cancelled'})
            membership.message_post(
                body=_('<b>Membership cancelled</b>'),
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

    def action_reset_to_draft(self):
        """Re-open a cancelled membership (back to draft)."""
        for membership in self:
            if membership.state != 'cancelled':
                raise UserError(_('Only cancelled memberships can be reset to draft!'))
            membership.write({'state': 'draft'})
            membership.message_post(
                body=_('<b>Membership reset to draft</b>'),
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

    def action_create_investment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Investment',
            'res_model': 'investment.subscription',
            'view_mode': 'form',
            'context': {
                'default_membership_id': self.id,
                'default_partner_id': self.partner_id.id,
            },
            'target': 'current',
        }

    def action_open_investment(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Investments'),
            'res_model': 'investment.subscription',
            'view_mode': 'list,form',
            'domain': [('membership_id', '=', self.id)],
            'target': 'current',
            'context': {
                'default_membership_id': self.id,
                'default_partner_id': self.partner_id.id,
            },
        }

        if self.investment_count == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.investment_ids[:1].id,
            })

        return action

    def _compute_investment_count(self):
        for rec in self:
            rec.investment_count = len(rec.investment_ids)

    # ===== Contract Methods =====

    def action_view_contract(self):
        """Open the linked sale contract, or create one if not exists."""
        self.ensure_one()
        if not self.contract_id:
            return self.action_create_contract()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Contract'),
            'res_model': 'sale.contract',
            'res_id': self.contract_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_create_contract(self):
        """Open sale contract creation form with pre-filled data."""
        self.ensure_one()
        contract_template = self.env['contract.template'].search([], limit=1)
        contract_title = self.env['sale.contract.title'].search([], limit=1)

        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Membership Contract'),
            'res_model': 'sale.contract',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_contract_date': self.membership_date or fields.Date.today(),
                'default_amount_total': self.initial_membership_fee,
                'default_currency_id': self.currency_id.id,
                'default_contract_template_id': contract_template.id if contract_template else False,
                'default_contract_title_name': contract_title.id if contract_title else False,
                'default_investment_membership_id': self.id,
                'default_note': _('Generated automatically from membership %s.') % (self.investor_code or self.membership_number),
            },
        }

    def _get_or_create_membership_contract(self):
        """Create sale contract automatically after membership activation."""
        self.ensure_one()
        if self.contract_id:
            return self.contract_id

        contract_template = self.env['contract.template'].search([], limit=1)
        contract_title = self.env['sale.contract.title'].search([], limit=1)
        agreement_text = contract_template.content if contract_template else self._get_default_membership_contract_terms()

        contract = self.env['sale.contract'].create({
            'partner_id': self.partner_id.id,
            'contract_date': self.membership_date or fields.Date.today(),
            'amount_total': self.initial_membership_fee,
            'currency_id': self.currency_id.id,
            'investment_membership_id': self.id,
            'contract_template_id': contract_template.id if contract_template else False,
            'contract_title_name': contract_title.id if contract_title else False,
            'agreement_terms': agreement_text,
            'note': _('Generated automatically from membership %s.') % (self.investor_code or self.membership_number),
        })
        self.contract_id = contract.id
        return contract

    def _get_default_membership_contract_terms(self):
        """Default contract terms for membership."""
        self.ensure_one()
        return """
            <p>This contract is generated automatically for the activated membership.</p>
            <p><strong>Club:</strong> %s</p>
            <p><strong>Membership Reference:</strong> %s</p>
            <p><strong>Investor Code:</strong> %s</p>
            <p><strong>Membership Date:</strong> %s</p>
            <p><strong>Expiry Date:</strong> %s</p>
            <p><strong>Initial Membership Fee:</strong> %s</p>
            <p><strong>Annual Subscription Fee:</strong> %s</p>
            <p><strong>Subscription Period:</strong> %s</p>
        """ % (
            self.club_id.display_name or '',
            self.membership_number or '',
            self.investor_code or '',
            self.membership_date or '',
            self.expiry_date or '',
            self.initial_membership_fee or 0.0,
            self.annual_subscription_fee or 0.0,
            dict(monthly='Monthly', quarterly='Quarterly', yearly='Yearly').get(self.subscription_period, ''),
        )

    def action_print_contract(self):
        """Print the linked membership contract and mark as printed."""
        self.ensure_one()
        if not self.contract_id:
            raise UserError(_('No contract found for this membership!'))
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
            raise UserError(_('No contract found for this membership!'))
        self.write({
            'contract_printed': True,
            'contract_print_date': fields.Date.today(),
        })
        self.message_post(
            body=_('Contract marked as printed on %s.') % fields.Date.today().strftime('%Y-%m-%d'),
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
        )

    # ===== Sequence / Investor Code (Merged) =====

    def _get_club_sequence(self, club_id=None):
        """Get or create a dedicated sequence for a club (used for prefix/padding)."""
        if club_id:
            club = self.env['investment.club'].browse(club_id)
        elif hasattr(self, 'club_id') and self.club_id:
            club = self.club_id
        else:
            return False

        if not club:
            return False

        club_name = club.name.replace(' ', '')
        sequence_code = f'investor.code.{club.id}'

        sequence = self.env['ir.sequence'].sudo().search([
            ('code', '=', sequence_code),
        ], limit=1)

        if not sequence:
            sequence = self.env['ir.sequence'].sudo().create({
                'name': f'Investor Code - {club.name}',
                'code': sequence_code,
                'prefix': f'INVS-{club_name}-',
                'padding': 5,
                'number_increment': 1,
            })

        return sequence

    def _generate_investor_code(self):
        """Generate: INVS-ElAhly-00001 (per club - consecutive, no gaps)"""
        self.ensure_one()
        return self._generate_code_for_vals(self.club_id.id if self.club_id else False)

    def _generate_code_for_vals(self, club_id, counter_cache=None):
        """Generate the next free investor code for a club.

        The number is derived from the existing records (first unused number)
        instead of a plain counter sequence, so import test runs / retried
        uploads / deleted records never leave permanent gaps (1, 4, 7...):
        deleted numbers are automatically reused for the next records.

        :param counter_cache: dict shared across a whole create() batch so
            several new lines of the same club keep incrementing correctly
            before the rows are actually inserted. It holds the set of used
            numbers per club.
        """
        if not club_id:
            return False

        sequence = self._get_club_sequence(club_id)
        if not sequence:
            return False

        if counter_cache is None:
            counter_cache = {}

        if club_id not in counter_cache:
            # Lock the club row: serializes concurrent code generation per club
            self.env.cr.execute(
                "SELECT id FROM investment_club WHERE id = %s FOR UPDATE",
                [club_id],
            )
            self.env.cr.execute(
                "SELECT investor_code FROM investment_membership "
                "WHERE club_id = %s AND investor_code IS NOT NULL",
                [club_id],
            )
            used = set()
            for (code,) in self.env.cr.fetchall():
                try:
                    used.add(int(str(code).rsplit('-', 1)[-1]))
                except (TypeError, ValueError):
                    continue
            counter_cache[club_id] = used
        else:
            used = counter_cache[club_id]

        next_num = 1
        while next_num in used:
            next_num += 1
        used.add(next_num)

        prefix = sequence.prefix or 'INVS-'
        padding = sequence.padding or 5
        return '%s%s' % (prefix, str(next_num).zfill(padding))

    def _allocate_sequence_number(self, sequence, table, column, cache, cache_key):
        """Allocate the first unused number of a year-based sequence.

        Same gap-proof logic as the investor code but for standard
        references like MEM/2026/00001 or INV/2026/00001: the number is
        computed from the existing data instead of the mutable counter,
        so retried uploads / test runs / deleted records never burn numbers.

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
        code_cache = {}
        seq_cache = {}
        for vals in vals_list:
            if not vals.get('membership_number') or vals.get('membership_number') == 'New':
                # Gap-proof number: first unused MEM/.../xxxxx (from data)
                seq = self.env['ir.sequence'].sudo().search([
                    ('code', '=', 'investment.membership'),
                ], limit=1)
                if seq:
                    prefix, num = self._allocate_sequence_number(
                        seq, 'investment_membership', 'membership_number',
                        seq_cache, 'investment.membership',
                    )
                    vals['membership_number'] = '%s%s' % (prefix, str(num).zfill(seq.padding or 5))
                else:
                    vals['membership_number'] = self.env['ir.sequence'].next_by_code('investment.membership')

            if vals.get('club_id') and not vals.get('investor_code'):
                vals['investor_code'] = self._generate_code_for_vals(vals['club_id'], code_cache)

            # Check club max members limit
            if vals.get('club_id'):
                club = self.env['investment.club'].browse(vals['club_id'])
                if club.max_members > 0:
                    current_count = self.env['investment.membership'].search_count([
                        ('club_id', '=', club.id),
                        ('state', 'not in', ('cancelled', 'terminated')),
                    ])
                    if current_count >= club.max_members:
                        raise ValidationError(_(
                            'Club "%s" has reached the maximum members limit (%s)!'
                        ) % (club.display_name or club.name_ar or club.name_en, club.max_members))

        try:
            with self.env.cr.savepoint():
                records = super().create(vals_list)
        except IntegrityError:
            # Duplicate investor code (e.g. codes coming from the import file):
            # regenerate them from scratch and retry once.
            for vals in vals_list:
                if vals.get('club_id'):
                    vals['investor_code'] = self._generate_code_for_vals(vals['club_id'], code_cache)
            with self.env.cr.savepoint():
                records = super().create(vals_list)

        # Auto-create the initial invoice in DRAFT state (draft invoice)
        if not self.env.context.get('investment_club_no_auto_invoice'):
            records._auto_create_initial_draft_invoice()

        return records

    def copy(self, default=None):
        """Reset investor code and membership number on duplicate."""
        default = dict(default or {})
        default['investor_code'] = False
        default['membership_number'] = 'New'
        return super().copy(default)

    # ===== Cron / Scheduled Actions =====

    def _get_config(self, key, default=False):
        """Read a config parameter value."""
        return self.env['ir.config_parameter'].sudo().get_param(
            'investment_club.%s' % key, default
        )

    def _cron_send_renewal_reminders(self):
        """Send renewal reminder notifications for memberships expiring soon."""
        if not self._get_config('enable_renewal_notifications', 'True') == 'True':
            return

        days_before = int(self._get_config('auto_renewal_days', '7'))
        today = fields.Date.today()
        reminder_date = today + timedelta(days=days_before)

        memberships = self.search([
            ('state', '=', 'active'),
            ('expiry_date', '<=', reminder_date),
            ('expiry_date', '>=', today),
            ('auto_renew', '=', True),
        ])

        for membership in memberships:
            days_left = (membership.expiry_date - today).days
            self._send_renewal_notification(membership, days_left)

        overdue = self.search([
            ('state', '=', 'active'),
            ('expiry_date', '<', today),
        ])

        for membership in overdue:
            days_overdue = (today - membership.expiry_date).days
            self._send_overdue_notification(membership, days_overdue)

    def _send_renewal_notification(self, membership, days_left):
        """Send a renewal reminder via Odoo's chatter/message system."""
        subject = _('Membership Renewal Reminder: %s') % (membership.investor_code or membership.membership_number)
        body = _(
            '<p>Dear <b>%s</b>,</p>'
            '<p>Your membership in <b>%s</b> will expire in <b>%s days</b> on <b>%s</b>.</p>'
            '<p>Renewal Amount: <b>%s %s</b></p>'
            '<p>Please renew your membership to avoid any interruption.</p>'
        ) % (
            membership.partner_id.name or '',
            membership.club_id.name or '',
            days_left,
            membership.expiry_date,
            membership.currency_id.symbol or '',
            membership.annual_subscription_fee,
        )
        membership.message_post(
            subject=subject,
            body=body,
            partner_ids=[membership.partner_id.id],
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
        )

    def _send_overdue_notification(self, membership, days_overdue):
        """Send an overdue notification."""
        subject = _('Membership expiry: %s') % (membership.investor_code or membership.membership_number)

        body = _(
            '<p>Dear <b>%s</b>Details</p>'
            '<p>Your membership in <b>%s</b> has expired since <b>%s day</b> on <b>%s</b>.</p>'
            '<p>Please renew your membership as soon as possible.</p>'
        ) % (
            membership.partner_id.name or '',
            membership.club_id.name or '',
            days_overdue,
            membership.expiry_date,
        )

        membership.message_post(
            subject=subject,
            body=body,
            partner_ids=[membership.partner_id.id],
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
        )

    def _cron_auto_expire_memberships(self):
        """Automatically set active memberships to expired if past expiry."""
        today = fields.Date.today()
        expired = self.search([
            ('state', '=', 'active'),
            ('expiry_date', '<', today),
        ])
        expired.write({'state': 'expired'})

    # ===== SQL Constraints =====

    _sql_constraints = [
        (
            'unique_investor_code_per_club',
            'unique(investor_code, club_id)',
            'Investor code must be unique per club!'
        ),
    ]
