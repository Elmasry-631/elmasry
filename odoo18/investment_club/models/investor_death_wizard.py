from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class InvestorDeathWizard(models.TransientModel):
    _name = 'investor.death.wizard'
    _description = 'Investor Death Case Wizard'

    # ===== Source Reference =====
    membership_id = fields.Many2one(
        'investment.membership',
        string='Membership',
        required=True
    )

    subscription_id = fields.Many2one(
        'investment.subscription',
        string='Investment Subscription (Optional)',
        help='Details Details Details Details Details Details'
    )

    partner_id = fields.Many2one(
        'res.partner',
        related='membership_id.partner_id',
        string='Deceased Investor',
        readonly=True
    )

    investor_code = fields.Char(
        related='membership_id.investor_code',
        string='Investor Code',
        readonly=True
    )

    club_id = fields.Many2one(
        'investment.club',
        related='membership_id.club_id',
        string='Club',
        readonly=True
    )

    membership_date = fields.Date(
        related='membership_id.membership_date',
        string='Membership Start Date',
        readonly=True
    )

    # ===== Death Info =====
    death_date = fields.Date(
        string='Death Date',
        required=True,
        default=fields.Date.today
    )

    inheritance_document = fields.Binary(
        string='Inheritance Document (Inheritance Certificate)',
        required=True,
        attachment=True,
        help='Please attach a copy of the inheritance certificate'
    )

    inheritance_document_name = fields.Char(
        string='Document Name',
        default='inheritance_document.pdf'
    )

    # ===== Action Choice =====
    action_type = fields.Selection([
        ('transfer', 'Transfer Ownership to Authorized Heir (Ownership Transfer)'),
        ('terminate', 'Terminate & Distribute (Termination Details)'),
    ], string='Action', required=True, default='terminate',
        help='Ownership Transfer: Transfer Details Membership/Share to heir Authorized\n'
             'Termination Details: Termination Contract Details Details Details DetailsInheritance Certificate'
    )

    # ===== Transfer Fields =====
    new_partner_id = fields.Many2one(
        'res.partner',
        string='Authorized Heir (Authorized Heir)',
        help='Person authorized by the heirs to receive the ownership transfer'
    )

    new_investor_code = fields.Char(
        string='New Investor Code',
        readonly=True,
        help='It will be generated automatically after confirmation'
    )

    # ===== Financial Fields (for terminate case) =====
    membership_original_paid = fields.Float(
        string='Original Membership Fee Paid',
        compute='_compute_financials',
        store=True
    )

    subscription_total = fields.Float(
        string='Investment Subscription Amount',
        compute='_compute_financials',
        store=True
    )

    subscription_project = fields.Char(
        string='Investment Project',
        compute='_compute_financials',
        store=True
    )

    refund_amount = fields.Float(
        string='Total Refund Amount',
        compute='_compute_refund',
        store=True
    )

    # ===== Payment =====
    refund_journal_id = fields.Many2one(
        'account.journal',
        string='Refund Journal',
        domain="[('type', 'in', ('bank', 'cash'))]",
        required=True
    )

    # ===== Notes =====
    notes = fields.Text(
        string='Notes',
        placeholder='Additional Notes...'
    )

    # ===== Compute Methods =====

    @api.depends('membership_id', 'subscription_id')
    def _compute_financials(self):
        for wizard in self:
            membership = wizard.membership_id
            wizard.membership_original_paid = membership.original_paid_fee or 0.0

            if wizard.subscription_id:
                wizard.subscription_total = wizard.subscription_id.amount or 0.0
                wizard.subscription_project = wizard.subscription_id.project_id.name or ''
            else:
                wizard.subscription_total = 0.0
                wizard.subscription_project = ''

    @api.depends('membership_id', 'subscription_id', 'action_type',
                 'membership_original_paid', 'subscription_total')
    def _compute_refund(self):
        for wizard in self:
            if wizard.action_type != 'terminate':
                wizard.refund_amount = 0.0
                continue

            if wizard.subscription_id:
                # Investment subscription termination: paid share principal
                wizard.refund_amount = wizard.subscription_total
            else:
                # Membership termination: paid membership principal
                wizard.refund_amount = wizard.membership_original_paid

    @api.onchange('action_type')
    def _onchange_action_type(self):
        """Show/hide fields based on action type."""
        if self.action_type == 'transfer' and not self.new_partner_id:
            self.new_partner_id = False

    # ===== Validation =====

    @api.constrains('inheritance_document', 'death_date')
    def _check_required_fields(self):
        for wizard in self:
            if not wizard.inheritance_document:
                raise ValidationError(_('Please attach the inheritance certificate!'))
            if not wizard.death_date:
                raise ValidationError(_('Please specify the date of death!'))

    # ===== Actions =====

    def action_confirm_death_case(self):
        """Main action: process the death case based on selected action type."""
        self.ensure_one()

        if not self.inheritance_document:
            raise UserError(_('Please attach the inheritance certificate!'))

        if not self.death_date:
            raise UserError(_('Please specify the date of death!'))

        if self.action_type == 'transfer':
            return self._action_transfer_ownership()
        else:
            return self._action_terminate_and_distribute()

    def _attach_inheritance_document(self, membership):
        """Attach the inheritance document to the membership record."""
        if self.inheritance_document:
            self.env['ir.attachment'].create({
                'name': 'Inheritance Certificate - %s' % (membership.investor_code or ''),
                'res_model': 'investment.membership',
                'res_id': membership.id,
                'type': 'binary',
                'datas': self.inheritance_document,
                'description': 'Attached inheritance certificate - investor death case',
            })

    def _action_transfer_ownership(self):
        """Transfer ownership to the authorized heir.

        Steps:
        1. Attach inheritance document
        2. Change partner on membership
        3. Change partner on all related active investments
        4. Post chatter messages
        """
        if not self.new_partner_id:
            raise UserError(_('Please select the authorized heir for the ownership transfer!'))

        membership = self.membership_id

        if membership.state not in ('active', 'initial_invoiced'):
            raise UserError(_('The membership must be active to transfer ownership!'))

        # Attach inheritance document
        self._attach_inheritance_document(membership)

        old_partner_name = membership.partner_id.name

        # If there's a specific subscription, just transfer it
        if self.subscription_id:
            sub = self.subscription_id
            if sub.state not in ('paid', 'active'):
                raise UserError(_('The investment subscription must be paid or active to transfer ownership!'))

            sub.write({
                'partner_id': self.new_partner_id.id,
            })

            # Also attach document to subscription
            if self.inheritance_document:
                self.env['ir.attachment'].create({
                    'name': 'Inheritance Certificate - %s' % (sub.name or ''),
                    'res_model': 'investment.subscription',
                    'res_id': sub.id,
                    'type': 'binary',
                    'datas': self.inheritance_document,
                    'description': 'Attached inheritance certificate - investor death case',
                })

            # Post message on subscription
            sub.message_post(
                body=_(
                    '<p><b>Investment subscription ownership transferred - death case</b></p>'
                    '<ul>'
                    '<li>Deceased investor: <b>%s</b></li>'
                    '<li>Project: <b>%s</b></li>'
                    '<li>Transferred to: <b>%s</b></li>'
                    '<li>Date of death: <b>%s</b></li>'
                    '<li>Inheritance certificate attached</li>'
                    '</ul>'
                ) % (
                    old_partner_name,
                    sub.project_id.name or '',
                    self.new_partner_id.name,
                    self.death_date,
                ),
                partner_ids=[self.new_partner_id.id],
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

        # Transfer membership ownership
        membership.write({
            'partner_id': self.new_partner_id.id,
        })

        # Also update all active investments under this membership
        active_investments = membership.investment_ids.filtered(
            lambda i: i.state in ('paid', 'active')
        )
        if active_investments:
            active_investments.write({
                'partner_id': self.new_partner_id.id,
            })

        # Post message on membership
        membership.message_post(
            body=_(
                '<p><b>Membership ownership transferred - death case</b></p>'
                '<ul>'
                '<li>Deceased investor: <b>%s</b></li>'
                '<li>Investor Code: <b>%s</b></li>'
                '<li>Transferred to: <b>%s</b></li>'
                '<li>Date of death: <b>%s</b></li>'
                '<li>Transferred Share Count: <b>%s</b></li>'
                '<li>Inheritance certificate attached</li>'
                '%s'
                '</ul>'
            ) % (
                old_partner_name,
                membership.investor_code or '',
                self.new_partner_id.name,
                self.death_date,
                len(active_investments),
                _('<li>Notes: <b>%s</b></li>') % self.notes if self.notes else '',
            ),
            partner_ids=[self.new_partner_id.id],
            message_type='notification',
            subtype_xmlid='mail.mt_comment',
        )

        return {'type': 'ir.actions.act_window_close'}

    def _action_terminate_and_distribute(self):
        """Terminate membership/subscription and distribute value per inheritance document.

        Steps:
        1. Attach inheritance document
        2. Create refund payment (original investment value - no deductions)
        3. Update state to terminated
        4. Post chatter message
        """
        membership = self.membership_id

        if membership.state not in ('active', 'initial_invoiced'):
            raise UserError(_('The membership must be active for termination!'))

        # Attach inheritance document
        self._attach_inheritance_document(membership)

        # ===== 1. Handle specific subscription termination =====
        if self.subscription_id:
            sub = self.subscription_id
            if sub.state not in ('paid', 'active'):
                raise UserError(_('The investment subscription must be paid or active!'))

            # Create refund payment for the subscription
            if self.refund_amount > 0:
                payment_vals = {
                    'payment_type': 'outbound',
                    'partner_type': 'customer',
                    'partner_id': membership.partner_id.id,
                    'journal_id': self.refund_journal_id.id,
                    'amount': self.refund_amount,
                    'currency_id': sub.currency_id.id,
                    'date': fields.Date.today(),
                    'memo': _(
                        'Death Case - Investment Return - %s'
                    ) % sub.name,
                }
                payment = self.env['account.payment'].create(payment_vals)
                payment.action_post()

                # Attach document to subscription too
                if self.inheritance_document:
                    self.env['ir.attachment'].create({
                        'name': 'Inheritance Certificate - %s' % (sub.name or ''),
                        'res_model': 'investment.subscription',
                        'res_id': sub.id,
                        'type': 'binary',
                        'datas': self.inheritance_document,
                        'description': 'Attached inheritance certificate - investor death case',
                    })

            # Update subscription state
            sub.write({'state': 'terminated'})

            # Post message on subscription
            sub.message_post(
                body=_(
                    '<p><b>Investment subscription terminated - death case</b></p>'
                    '<ul>'
                    '<li>Deceased investor: <b>%s</b></li>'
                    '<li>Project: <b>%s</b></li>'
                    '<li>Share Count: <b>%s</b></li>'
                    '<li>Share Value: <b>%s</b></li>'
                    '<li>Total Refunded Amount: <b>%s</b></li>'
                    '<li>Date of death: <b>%s</b></li>'
                    '<li>Distributed according to the attached inheritance certificate</li>'
                    '</ul>'
                ) % (
                    membership.partner_id.name or '',
                    sub.project_id.name or '',
                    sub.share_count,
                    sub.share_value,
                    self.refund_amount,
                    self.death_date,
                ),
                partner_ids=[membership.partner_id.id],
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

        # ===== 2. Handle full membership termination =====
        if not self.subscription_id:
            # Create refund payment for membership
            if self.refund_amount > 0:
                payment_vals = {
                    'payment_type': 'outbound',
                    'partner_type': 'customer',
                    'partner_id': membership.partner_id.id,
                    'journal_id': self.refund_journal_id.id,
                    'amount': self.refund_amount,
                    'currency_id': membership.currency_id.id,
                    'date': fields.Date.today(),
                    'memo': _(
                        'Death Case - Membership Refund - %s'
                    ) % (membership.investor_code or membership.membership_number),
                }
                payment = self.env['account.payment'].create(payment_vals)
                payment.action_post()

            # Terminate all active investments under this membership
            active_investments = membership.investment_ids.filtered(
                lambda i: i.state in ('paid', 'active')
            )
            if active_investments:
                active_investments.write({'state': 'terminated'})

            # Update membership state
            membership.write({
                'state': 'terminated',
                'termination_date': fields.Date.today(),
                'termination_reason': _(
                    'Death case - distributed according to the inheritance certificate dated %s'
                ) % self.death_date,
                'termination_refund_amount': self.refund_amount,
                'termination_deduction': 0.0,
            })

            # Post message on membership
            membership.message_post(
                body=_(
                    '<p><b>Membership terminated - death case</b></p>'
                    '<ul>'
                    '<li>Deceased investor: <b>%s</b></li>'
                    '<li>Investor Code: <b>%s</b></li>'
                    '<li>Paid Membership Principal: <b>%s</b></li>'
                    '<li>Refund Amount (Principal): <b>%s</b></li>'
                    '<li>Closed Investment Subscription Count: <b>%s</b></li>'
                    '<li>Date of death: <b>%s</b></li>'
                    '<li>Distributed according to the attached inheritance certificate</li>'
                    '<li>No deductions (death case)</li>'
                    '%s'
                    '</ul>'
                ) % (
                    membership.partner_id.name or '',
                    membership.investor_code or '',
                    membership.original_paid_fee or 0.0,
                    self.refund_amount,
                    len(active_investments),
                    self.death_date,
                    _('<li>Notes: <b>%s</b></li>') % self.notes if self.notes else '',
                ),
                partner_ids=[membership.partner_id.id],
                message_type='notification',
                subtype_xmlid='mail.mt_comment',
            )

        return {'type': 'ir.actions.act_window_close'}
