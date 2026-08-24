import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class CreditApprovalRequest(models.Model):
    _name = 'credit.approval.request'
    _description = 'Credit Approval Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'display_name'

    # --------------------------------------------------
    # Selections
    # --------------------------------------------------
    _STATES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    # --------------------------------------------------
    # Fields
    # --------------------------------------------------
    name = fields.Char(
        string='Reference',
        readonly=True,
        default=lambda self: _('New'),
        copy=False,
        help='Auto-generated sequence number.',
    )

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order',
        required=True,
        readonly=True,
        ondelete='cascade',
        help='The sale order that triggered this approval request.',
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        required=True,
        readonly=True,
        store=True,
        help='Customer (commercial entity).',
    )

    requested_by = fields.Many2one(
        comodel_name='res.users',
        string='Requested By',
        required=True,
        readonly=True,
        default=lambda self: self.env.user,
        help='The salesperson who created this request.',
    )

    supervisor_id = fields.Many2one(
        comodel_name='res.users',
        string='Supervisor',
        required=True,
        readonly=True,
        help='The sales supervisor who will approve or reject.',
    )

    state = fields.Selection(
        selection=_STATES,
        string='Status',
        default='draft',
        required=True,
        tracking=True,
        help='Current state of the approval request.',
    )

    # Credit details (snapshot at request time)
    credit_limit = fields.Float(
        string='Credit Limit',
        digits=(16, 2),
        readonly=True,
        help='Customer credit limit at the time of request.',
    )

    credit_used = fields.Float(
        string='Credit Used',
        digits=(16, 2),
        readonly=True,
        help='Customer outstanding balance at the time of request.',
    )

    order_amount = fields.Monetary(
        string='Order Amount',
        currency_field='currency_id',
        readonly=True,
        help='Total amount of the sale order.',
    )

    exceeded_by = fields.Float(
        string='Exceeded By',
        digits=(16, 2),
        readonly=True,
        help='How much the projected total exceeds the credit limit.',
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        readonly=True,
        help='Currency of the sale order.',
    )

    # Rejection
    rejection_reason_id = fields.Many2one(
        comodel_name='credit.rejection.reason',
        string='Rejection Reason',
        domain="[('active', '=', True), ('company_id', '=', company_id)]",
        help='Predefined reason for rejection.',
    )

    rejection_notes = fields.Text(
        string='Additional Notes',
        help='Optional additional notes from the supervisor.',
    )

    approval_date = fields.Datetime(
        string='Approval/Rejection Date',
        readonly=True,
        help='When the request was approved or rejected.',
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
    )

    # --------------------------------------------------
    # Computed
    # --------------------------------------------------
    @api.depends('name', 'sale_order_id.name')
    def _compute_display_name(self):
        for rec in self:
            if rec.name == _('New'):
                rec.display_name = f"{rec.sale_order_id.name or ''} — {rec.state}"
            else:
                rec.display_name = f"{rec.name} — {rec.sale_order_id.name or ''}"

    # --------------------------------------------------
    # CRUD
    # --------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'credit.approval.request'
                ) or _('New')
        return super().create(vals_list)

    # --------------------------------------------------
    # Business Methods
    # --------------------------------------------------
    def action_submit(self):
        """Submit the approval request to the supervisor."""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft requests can be submitted.'))
        self.write({'state': 'submitted'})
        self.sale_order_id.write({'credit_approval_state': 'pending'})
        self._notify_supervisor()
        self.sale_order_id.message_post(
            body=_(
                'Credit approval request <a href="#" data-oe-model="credit.approval.request" '
                'data-oe-id="%(id)d">%(name)s</a> submitted to %(supervisor)s.'
            ) % {
                'id': self.id,
                'name': self.name,
                'supervisor': self.supervisor_id.display_name,
            },
            subject=_('Credit Approval Submitted'),
        )

    def action_approve(self):
        """Approve the credit request and confirm the sale order."""
        self.ensure_one()
        if self.state != 'submitted':
            raise UserError(_('Only submitted requests can be approved.'))
        self.write({
            'state': 'approved',
            'approval_date': fields.Datetime.now(),
        })
        # Log on approval request
        self.message_post(
            body=_('Approved by %s.') % self.env.user.display_name,
            subject=_('Credit Approval Approved'),
        )
        # Log on sale order
        self.sale_order_id.write({
            'credit_approval_state': 'approved',
            'credit_approval_id': self.id,
        })
        self.sale_order_id.message_post(
            body=_(
                'Credit limit exceeded — <b>Approved</b> by %(user)s.<br/>'
                'Approval: <a href="#" data-oe-model="credit.approval.request" '
                'data-oe-id="%(id)d">%(name)s</a>'
            ) % {
                'user': self.env.user.display_name,
                'id': self.id,
                'name': self.name,
            },
            subject=_('Credit Approved'),
        )
        # Confirm the sale order
        try:
            self.sale_order_id.with_context(
                credit_approval_bypass=True
            ).action_confirm()
        except Exception as e:
            _logger.exception(
                'Failed to confirm SO %s after credit approval',
                self.sale_order_id.id,
            )
            self.message_post(
                body=_(
                    'Approval was granted, but sale order confirmation failed: %s'
                ) % str(e),
                subject=_('Sale Order Confirmation Failed'),
            )

    def action_reject(self):
        """Reject the credit request — rejection_reason_id must be set."""
        self.ensure_one()
        if self.state != 'submitted':
            raise UserError(_('Only submitted requests can be rejected.'))
        if not self.rejection_reason_id:
            raise ValidationError(_('Please select a rejection reason before rejecting.'))
        self.write({
            'state': 'rejected',
            'approval_date': fields.Datetime.now(),
        })
        reason_name = self.rejection_reason_id.name
        # Log on approval request
        self.message_post(
            body=_('Rejected by %s. Reason: %s') % (
                self.env.user.display_name, reason_name,
            ),
            subject=_('Credit Approval Rejected'),
        )
        # Log on sale order
        self.sale_order_id.write({
            'credit_approval_state': 'rejected',
            'credit_approval_id': self.id,
        })
        self.sale_order_id.message_post(
            body=_(
                'Credit limit exceeded — <b>Rejected</b> by %(user)s.<br/>'
                'Reason: <b>%(reason)s</b><br/>'
                '%(notes)s'
                'Approval: <a href="#" data-oe-model="credit.approval.request" '
                'data-oe-id="%(id)d">%(name)s</a>'
            ) % {
                'user': self.env.user.display_name,
                'reason': reason_name,
                'notes': (
                    self.rejection_notes or ''
                ) + '<br/>' if self.rejection_notes else '',
                'id': self.id,
                'name': self.name,
            },
            subject=_('Credit Approval Rejected'),
        )

    def action_cancel(self):
        """Cancel the approval request."""
        self.ensure_one()
        if self.state not in ('draft', 'submitted'):
            raise UserError(_('Cannot cancel a request that is already processed.'))
        self.write({'state': 'cancelled'})
        self.sale_order_id.write({'credit_approval_state': 'none', 'credit_approval_id': False})
        self.message_post(
            body=_('Cancelled by %s.') % self.env.user.display_name,
            subject=_('Credit Approval Cancelled'),
        )

    def action_resubmit(self):
        """Reset a rejected request back to draft for resubmission."""
        self.ensure_one()
        if self.state != 'rejected':
            raise UserError(_('Only rejected requests can be resubmitted.'))
        self.write({
            'state': 'draft',
            'rejection_reason_id': False,
            'rejection_notes': False,
            'approval_date': False,
        })
        self.sale_order_id.write({'credit_approval_state': 'none'})
        self.message_post(
            body=_('Reset to draft for resubmission by %s.') % self.env.user.display_name,
            subject=_('Credit Approval Resubmission'),
        )

    # --------------------------------------------------
    # Notification
    # --------------------------------------------------
    def _notify_supervisor(self):
        """Send a notification to the supervisor about the new request."""
        self.ensure_one()
        if not self.supervisor_id:
            return
        template = self.env.ref(
            'el_nmo_credit_approval.email_template_credit_approval',
            raise_if_not_found=False,
        )
        if template:
            template.send_mail(self.id, email_values={
                'email_to': self.supervisor_id.email_formatted,
            })
        else:
            # Fallback: post in chatter
            self.message_post(
                body=_(
                    'Approval request created for <a href="#" data-oe-model="sale.order" '
                    'data-oe-id="%(so_id)d">%(so_name)s</a>. '
                    'Please review and approve or reject.'
                ) % {
                    'so_id': self.sale_order_id.id,
                    'so_name': self.sale_order_id.name,
                },
                subject=_('New Credit Approval Request'),
                partner_ids=[self.supervisor_id.partner_id.id],
            )

    # --------------------------------------------------
    # Factory: called from sale.order
    # --------------------------------------------------
    @api.model
    def _create_from_sale_order(self, sale_order):
        """Create and submit a credit approval request from a sale order."""
        partner = sale_order.partner_id.commercial_partner_id.sudo()
        projected = partner.credit + sale_order.amount_total
        exceeded = projected - partner.effective_credit_limit

        # Find supervisor: partner's sales_supervisor_id or fallback
        supervisor = partner.sales_supervisor_id or self._get_supervisor(sale_order.user_id)

        request = self.create({
            'sale_order_id': sale_order.id,
            'partner_id': partner.id,
            'requested_by': sale_order.user_id.id or self.env.uid,
            'supervisor_id': supervisor.id if supervisor else self.env.uid,
            'credit_limit': partner.effective_credit_limit,
            'credit_used': partner.credit,
            'order_amount': sale_order.amount_total,
            'exceeded_by': exceeded,
            'currency_id': sale_order.currency_id.id,
            'company_id': sale_order.company_id.id,
        })
        request.action_submit()
        _logger.info(
            'Credit approval request %s created for SO %s '
            '(partner %s, supervisor %s)',
            request.name, sale_order.name,
            partner.display_name, supervisor.name if supervisor else 'N/A',
        )
        return request


    @api.model
    def _get_supervisor(self, salesperson):
        """Find the supervisor for a salesperson.

        Looks up the sales team's team leader. Falls back to
        the user's parent user if no team leader is found.
        Last fallback: any active user with the Supervisor or Manager group.
        """
        if not salesperson:
            return self.env['res.users'].browse()
        # Check sales team membership
        member = self.env['crm.team.member'].search([
            ('user_id', '=', salesperson.id),
        ], limit=1)
        if member and member.crm_team_id and member.crm_team_id.user_id:
            return member.crm_team_id.user_id
        # Fallback: user's parent
        if salesperson.parent_id:
            return salesperson.parent_id
        # Last fallback: any user with supervisor or manager group
        SupervisorGroup = self.env.ref(
            'el_nmo_credit_approval.group_credit_approval_supervisor',
            raise_if_not_found=False,
        )
        if SupervisorGroup:
            user = self.env['res.users'].search([
                ('group_ids', 'in', SupervisorGroup.id),
                ('active', '=', True),
            ], limit=1)
            if user:
                return user
        ManagerGroup = self.env.ref(
            'el_nmo_credit_approval.group_credit_approval_manager',
            raise_if_not_found=False,
        )
        if ManagerGroup:
            user = self.env['res.users'].search([
                ('group_ids', 'in', ManagerGroup.id),
                ('active', '=', True),
            ], limit=1)
            if user:
                return user
        return self.env['res.users'].browse()