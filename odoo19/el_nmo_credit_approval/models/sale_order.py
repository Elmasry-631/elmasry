from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # --------------------------------------------------
    # New Fields
    # --------------------------------------------------
    credit_approval_id = fields.Many2one(
        comodel_name='credit.approval.request',
        string='Credit Approval',
        copy=False,
        help='The credit approval request linked to this sale order.',
    )

    credit_approval_state = fields.Selection(
        selection=[
            ('none', 'None'),
            ('pending', 'Pending Approval'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        string='Credit Approval Status',
        default='none',
        tracking=True,
        help='Credit approval workflow status for this order.',
    )

    is_credit_blocked = fields.Boolean(
        string='Credit Blocked',
        compute='_compute_is_credit_blocked',
        compute_sudo=True,
        store=True,
        help='Whether this order is blocked due to credit limit exceeded.',
    )

    # --------------------------------------------------
    # Computed
    # --------------------------------------------------
    @api.depends(
        'partner_id', 'partner_id.commercial_partner_id.payment_type',
        'partner_id.commercial_partner_id.credit_policy',
        'partner_id.commercial_partner_id.effective_credit_limit',
        'partner_id.commercial_partner_id.credit',
        'amount_total',
        'credit_approval_state',
        'state',
    )
    def _compute_is_credit_blocked(self):
        for order in self:
            if order.state != 'draft' or order.credit_approval_state == 'approved':
                order.is_credit_blocked = False
                continue
            partner = order.partner_id.commercial_partner_id.sudo()
            if partner.payment_type != 'credit':
                order.is_credit_blocked = False
                continue
            if not partner.classification_id or partner.credit_policy != 'block':
                order.is_credit_blocked = False
                continue
            effective_limit = partner.effective_credit_limit
            if effective_limit <= 0:
                order.is_credit_blocked = False
                continue
            projected = partner.credit + order.amount_total
            order.is_credit_blocked = projected > effective_limit

    # --------------------------------------------------
    # Override action_confirm
    # --------------------------------------------------
    def action_confirm(self):
        """Override: route to approval workflow instead of hard-blocking."""
        # If this is a bypass call (after approval), go straight to super
        if self.env.context.get('credit_approval_bypass'):
            return super().action_confirm()

        for order in self:
            partner = order.partner_id.commercial_partner_id.sudo()

            # Only check credit for credit customers with classification
            if partner.payment_type != 'credit':
                continue
            if not partner.classification_id:
                continue
            if partner.credit_policy != 'block':
                # Warning policy — post warning but allow
                self._check_and_warn_credit(order, partner)
                continue

            effective_limit = partner.effective_credit_limit
            if effective_limit <= 0:
                continue

            projected = partner.credit + order.amount_total
            if projected <= effective_limit:
                continue

            # --- Credit limit exceeded + block policy ---
            # Check if already approved
            if order.credit_approval_state == 'approved':
                continue

            # Create approval request
            ApprovalRequest = self.env['credit.approval.request']
            existing = ApprovalRequest.search([
                ('sale_order_id', '=', order.id),
                ('state', 'in', ('draft', 'submitted')),
            ], limit=1)

            if existing:
                raise UserError(_(
                    "Credit limit exceeded! An approval request (%s) "
                    "is already pending for this order."
                ) % existing.name)

            request = ApprovalRequest._create_from_sale_order(order)

            # Create an activity for the supervisor on the SO
            self._create_credit_activity(order, request, partner)

            # Commit now so the request & activity survive the rollback
            self.env.cr.commit()

            raise UserError(_(
                "Credit limit exceeded!\n\n"
                "Customer: %s\n"
                "Credit Limit: %s\n"
                "Outstanding: %s\n"
                "This Order: %s\n"
                "Exceeded By: %s\n\n"
                "An approval request has been sent to your supervisor "
                "with an activity assigned for review."
            ) % (
                partner.display_name,
                f"{effective_limit:,.2f}",
                f"{partner.credit:,.2f}",
                f"{order.amount_total:,.2f}",
                f"{projected - effective_limit:,.2f}",
            ))

        # If any order is approved, call super with bypass context
        # so el_nmo_classification skips its credit check.
        if any(order.credit_approval_state == 'approved' for order in self):
            return self.with_context(credit_approval_bypass=True).action_confirm()

        # All checks passed (or warning policy) — proceed with super
        return super().action_confirm()

    def _create_credit_activity(self, order, request, partner):
        """Create a mail activity on the sale order for the supervisor."""
        activity_type = self.env.ref(
            'el_nmo_credit_approval.mail_activity_type_credit_approval',
            raise_if_not_found=False,
        ) or self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
        if not activity_type:
            return
        self.env['mail.activity'].create({
            'activity_type_id': activity_type.id,
            'res_model_id': self.env['ir.model']._get('sale.order').id,
            'res_id': order.id,
            'user_id': request.supervisor_id.id,
            'summary': _('Credit Approval Required'),
            'note': _(
                'Customer <b>%(customer)s</b> has exceeded their credit limit.\n'
                'Order: <a href=# data-oe-model="sale.order" data-oe-id="%(so_id)d">%(so_name)s</a>\n'
                'Approval Request: <a href=# data-oe-model="credit.approval.request" '
                'data-oe-id="%(req_id)d">%(req_name)s</a>\n'
                'Amount: %(amount)s &gt; Limit: %(limit)s'
            ) % {
                'customer': order.partner_id.display_name,
                'so_id': order.id,
                'so_name': order.name,
                'req_id': request.id,
                'req_name': request.name,
                'amount': f"{order.amount_total:,.2f}",
                'limit': f"{partner.effective_credit_limit:,.2f}",
            },
        })

    def _check_and_warn_credit(self, order, partner):
        """Post a warning message on the order for 'warning' policy."""
        effective_limit = partner.effective_credit_limit
        if effective_limit <= 0:
            return
        projected = partner.credit + order.amount_total
        if projected <= effective_limit:
            return
        exceeded = projected - effective_limit
        order.message_post(
            body=_(
                '<p><b>Credit Limit Warning</b></p>'
                'Limit: <b>%(limit)s</b><br/>'
                'Outstanding: <b>%(outstanding)s</b><br/>'
                'This Order: <b>%(order)s</b><br/>'
                'Exceeded By: <b>%(exceeded)s</b>'
            ) % {
                'limit': f"{effective_limit:,.2f}",
                'outstanding': f"{partner.credit:,.2f}",
                'order': f"{order.amount_total:,.2f}",
                'exceeded': f"{exceeded:,.2f}",
            },
            subject=_('Credit Limit Warning'),
        )