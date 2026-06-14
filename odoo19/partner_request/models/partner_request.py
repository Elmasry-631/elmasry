import re
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError, ValidationError

_logger = logging.getLogger(__name__)


class PartnerRequest(models.Model):
    """
    Partner Request — approval workflow for creating new customers.
    Sales users submit requests; managers approve/reject/send back.

    Technical details:
        - Table: partner_request
        - Inherits: mail.thread, mail.activity.mixin
        - Order: create_date desc, id desc

    State Machine:
        draft --Submit--> pending --Create Partner--> approved
                          |  ^
                          |  |
                    Send Back |
                          |  |
                          v  |
                       sent_back --Submit--> pending
                          |
                    Reject |
                          v
                       rejected

    Relationships:
        - Belongs to: res.partner (field: partner_id)
        - Belongs to: res.users (field: salesperson_id)
        - Belongs to: res.users (field: sales_supervisor_id)
        - Belongs to: res.country (field: country_id)
        - Belongs to: res.country.state (field: state_id)
    """

    _name = 'partner.request'
    _description = 'Partner Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'
    _rec_name = 'sequence'

    # ── Basic Info ───────────────────────────────────────────────

    name = fields.Char(
        string='Customer Name',
        required=True,
        tracking=True,
        help='Name of the customer to be created.',
    )

    customer_code = fields.Char(
        string='Customer Code',
        tracking=True,
        help='Manual customer code / reference.',
    )

    classification_id = fields.Many2one(
        comodel_name='customer.classification',
        string='Customer Classification',
        tracking=True,
        help='Classification tier for the customer.',
    )

    contact_person = fields.Char(
        string='Contact Person',
        tracking=True,
        help='Name of the primary contact person.',
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Created Customer',
        readonly=True,
        tracking=True,
        help='The customer record created after approval.',
    )

    sequence = fields.Char(
        string='Request Number',
        readonly=True,
        default=lambda self: 'New',
        copy=False,
        help='Auto-generated request number (PRQ-YYYY-NNNNN).',
    )

    # ── Address ──────────────────────────────────────────────────

    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country',
        tracking=True,
    )

    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State / Province',
        domain="[('country_id', '=', country_id)]",
        tracking=True,
    )

    city = fields.Char(
        string='City',
        tracking=True,
    )

    area = fields.Char(
        string='Area',
        tracking=True,
        help='Neighborhood or area within the city.',
    )

    street = fields.Char(
        string='Street',
        tracking=True,
    )

    zip = fields.Char(
        string='ZIP Code',
        tracking=True,
    )

    pobox = fields.Char(
        string='P.O. Box',
        tracking=True,
    )

    # ── Contact Info ─────────────────────────────────────────────

    phone = fields.Char(
        string='Phone',
        tracking=True,
    )

    email = fields.Char(
        string='Email',
        tracking=True,
    )

    vat = fields.Char(
        string='Tax ID / VAT',
        tracking=True,
        help='Saudi VAT number: must start with 3 and be exactly 15 digits.',
    )

    @api.constrains('vat')
    def _check_vat(self):
        for rec in self:
            if not rec.vat:
                continue
            if not rec.vat.isdigit() or len(rec.vat) != 15 or rec.vat[0] != '3':
                raise ValidationError(_(
                    'VAT number must be exactly 15 digits starting with 3.'
                ))

    # ── Sales ────────────────────────────────────────────────────

    sales_supervisor_id = fields.Many2one(
        comodel_name='res.users',
        string='Sales Supervisor',
        tracking=True,
        help='Supervisor who will approve the request.',
    )

    salesperson_id = fields.Many2one(
        comodel_name='res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
        tracking=True,
        help='Requester - defaults to the current user.',
    )

    # ── State Machine ────────────────────────────────────────────

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('sent_back', 'Sent Back'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        string='Status',
        default='draft',
        required=True,
        tracking=True,
        help='Current status of the partner request.',
    )

    rejection_reason = fields.Text(
        string='Rejection Reason',
        tracking=True,
        help='Reason provided when the request is rejected.',
    )

    send_back_reason = fields.Text(
        string='Send Back Reason',
        tracking=True,
        help='Reason provided when the request is sent back for revision.',
    )

    # ── Create Override (Sequence Generation) ────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', 'New') == 'New':
                vals['sequence'] = (
                    self.env['ir.sequence'].next_by_code('partner.request')
                    or 'New'
                )
        return super().create(vals_list)

    # ── State Machine Safety ─────────────────────────────────────

    def _validate_state(self, allowed_states):
        """
        Validate that the record is in one of the allowed states.

        Args:
            allowed_states: list/tuple of valid state values.

        Raises:
            UserError: if current state is not in allowed_states.
        """
        for rec in self:
            if rec.state not in allowed_states:
                raise UserError(_(
                    "Cannot perform this action.\n"
                    "Expected: %s\n"
                    "Actual: %s"
                ) % (
                    ', '.join(allowed_states),
                    dict(self._fields['state'].selection).get(
                        rec.state, rec.state
                    ),
                ))

    # ── Action: Submit ───────────────────────────────────────────

    def action_submit(self):
        """
        Submit the request for approval.
        Transition: draft/sent_back -> pending.

        Schedules an activity on the supervisor.
        Clears previous rejection/send-back reasons.
        """
        self._validate_state(('draft', 'sent_back'))

        for request in self:
            request.write({
                'state': 'pending',
                'rejection_reason': False,
                'send_back_reason': False,
            })

            # Determine the reviewer (supervisor or salesperson's manager)
            reviewer = request.sales_supervisor_id
            if not reviewer:
                employee = request.salesperson_id.employee_id if hasattr(request.salesperson_id, 'employee_id') else None
                if employee and employee.parent_id.user_id:
                    reviewer = employee.parent_id.user_id

            # Fallback: find any sales manager
            if not reviewer:
                try:
                    mgr_group = self.env.ref('sales_team.group_sale_manager')
                    manager_users = self.env['res.users'].search([
                        ('groups_id', 'in', [mgr_group.id]),
                    ], limit=1)
                    reviewer = manager_users
                except Exception:
                    pass

            # Schedule activity on the reviewer
            if reviewer and reviewer.partner_id:
                try:
                    request.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('New partner request awaiting your approval'),
                        note=_(
                            '<b>%s</b> submitted a new partner request '
                            'for <b>%s</b>.'
                        ) % (
                            request.salesperson_id.name or _('Salesperson'),
                            request.name,
                        ),
                        user_id=reviewer.id,
                    )
                except Exception:
                    _logger.warning(
                        'Could not schedule activity for request %s',
                        request.sequence,
                    )

    # ── Action: Create Partner ───────────────────────────────────

    def action_create_partner(self):
        """
        Approve and create the customer.
        Transition: pending -> approved.

        Creates a res.partner, links it, and notifies the salesperson.
        """
        self._validate_state(('pending',))

        for request in self:
            # 1. Validate data
            if not request.name:
                raise UserError(_('Customer name is required.'))

            if request.email and not re.match(
                r'^[^@]+@[^@]+\.[^@]+$', request.email
            ):
                raise ValidationError(
                    _('Invalid email format: %s') % request.email
                )

            if request.phone and not re.match(
                r'^[\d\s\+\-\(\)]+$', request.phone
            ):
                raise ValidationError(
                    _('Invalid phone format: %s') % request.phone
                )

            # 2. Check for duplicate by email
            if request.email:
                existing = self.env['res.partner'].search([
                    ('email', '=', request.email),
                    ('is_company', '=', True),
                ], limit=1)
                if existing:
                    raise UserError(_(
                        'A customer with email "%s" already exists: %s.\n'
                        'Please verify before creating a duplicate.'
                    ) % (request.email, existing.name))

            # 3. Create partner
            partner_vals = {
                'name': request.name,
                'is_company': True,
                'customer_rank': 1,
                'classification_id': request.classification_id.id if request.classification_id else False,
                'country_id': request.country_id.id if request.country_id else False,
                'state_id': request.state_id.id if request.state_id else False,
                'city': request.city or False,
                'street': request.street or False,
                'zip': request.zip or False,
                'phone': request.phone or False,
                'email': request.email or False,
                'vat': request.vat or False,
                'comment': _('Created via Partner Request: %s') % request.sequence,
            }

            partner = self.env['res.partner'].with_context(
                partner_request_bypass=True
            ).create(partner_vals)

            # 4. Update request
            request.write({
                'state': 'approved',
                'partner_id': partner.id,
            })

            # 5. Notify salesperson
            if request.salesperson_id.partner_id:
                try:
                    request.message_post(
                        body=_(
                            'Your partner request <b>%s</b> has been '
                            'approved. Customer <b>%s</b> has been created.'
                        ) % (request.sequence, partner.name),
                        partner_ids=request.salesperson_id.partner_id.ids,
                        subject=_('Partner Request Approved'),
                    )
                except Exception:
                    _logger.warning(
                        'Could not notify salesperson for request %s',
                        request.sequence,
                    )

            request.message_post(
                body=_(
                    'Partner <a href="#" data-oe-model="res.partner" '
                    'data-oe-id="%d">%s</a> created successfully.'
                ) % (partner.id, partner.name),
            )

    # ── Action: Send Back ────────────────────────────────────────

    def action_send_back(self):
        """
        Send the request back to the salesperson for revision.
        Transition: pending -> sent_back.

        Requires a reason. Schedules an activity on the salesperson.
        """
        self._validate_state(('pending',))

        for request in self:
            if not request.send_back_reason:
                raise UserError(_(
                    'Please provide a reason for sending back the request.'
                ))

            request.write({'state': 'sent_back'})

            if request.salesperson_id.partner_id:
                try:
                    request.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Partner request sent back for revision'),
                        note=_('<b>Reason:</b> %s') % request.send_back_reason,
                        user_id=request.salesperson_id.id,
                    )
                except Exception:
                    _logger.warning(
                        'Could not schedule activity for request %s',
                        request.sequence,
                    )

    # ── Action: Reject ───────────────────────────────────────────

    def action_reject(self):
        """
        Reject the request permanently.
        Transition: pending -> rejected.

        Requires a reason. Notifies the salesperson.
        """
        self._validate_state(('pending',))

        for request in self:
            if not request.rejection_reason:
                raise UserError(_(
                    'Please provide a reason for rejecting the request.'
                ))

            request.write({'state': 'rejected'})

            if request.salesperson_id.partner_id:
                try:
                    request.message_post(
                        body=_(
                            'Your partner request <b>%s</b> for '
                            '<b>%s</b> has been rejected.\n'
                            '<b>Reason:</b> %s'
                        ) % (
                            request.sequence,
                            request.name,
                            request.rejection_reason,
                        ),
                        partner_ids=request.salesperson_id.partner_id.ids,
                        subject=_('Partner Request Rejected'),
                    )
                except Exception:
                    _logger.warning(
                        'Could not notify salesperson for request %s',
                        request.sequence,
                    )

    # ── Smart Button: Open Partner ───────────────────────────────

    def action_open_partner(self):
        """Open the created customer's form view."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Customer'),
            'res_model': 'res.partner',
            'view_mode': 'form',
            'res_id': self.partner_id.id,
            'target': 'current',
        }


class ResPartner(models.Model):
    """
    Extension of res.partner to restrict direct customer creation
    for users in the partner_request_user group (non-managers).

    Users in partner_request.group_partner_request_user cannot create
    company-type partners directly — they must use a Partner Request.
    Contacts and addresses are still allowed.

    The context key 'partner_request_bypass' skips this check,
    used by the partner_request module when creating approved partners.
    """

    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        bypass = self.env.context.get('partner_request_bypass')
        if not bypass:
            is_request_user = self.env.user.has_group(
                'partner_request.group_partner_request_user'
            )
            is_request_manager = self.env.user.has_group(
                'partner_request.group_partner_request_manager'
            )
            if is_request_user and not is_request_manager:
                for vals in vals_list:
                    if vals.get('is_company'):
                        raise AccessError(_(
                            "You cannot create customers directly.\n"
                            "Please submit a Partner Request for approval."
                        ))
        return super().create(vals_list)