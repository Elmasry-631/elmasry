"""Hospital Invoice Billing + Line — wraps account.move for medical billing."""

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HospitalInvoiceBillingLine(models.Model):
    """One billing line (service item)."""

    _name = 'hospital.invoice.billing.line'
    _description = 'Hospital Billing Line'

    billing_id = fields.Many2one(
        comodel_name='hospital.invoice.billing',
        string='Billing',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(string='Description', required=True)
    service_type = fields.Selection([
        ('consultation', 'Consultation'),
        ('lab', 'Laboratory'),
        ('radiology', 'Radiology'),
        ('pharmacy', 'Pharmacy'),
        ('room', 'Room Charges'),
        ('other', 'Other'),
    ], string='Service Type', default='consultation')
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Monetary(string='Unit Price', default=0.0)
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='billing_id.currency_id',
        store=True,
    )

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.quantity * rec.price_unit


class HospitalInvoiceBilling(models.Model):
    """Medical billing — creates an account.move when confirmed."""

    _name = 'hospital.invoice.billing'
    _description = 'Hospital Invoice Billing'
    _order = 'billing_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        string='Patient',
        required=True,
        ondelete='restrict',
        tracking=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        related='patient_id.partner_id',
        store=True,
        readonly=True,
    )
    physician_id = fields.Many2one(
        comodel_name='hospital.physician',
        string='Physician',
        ondelete='set null',
    )
    move_id = fields.Many2one(
        comodel_name='account.move',
        string='Invoice',
        ondelete='set null',
        readonly=True,
    )
    billing_date = fields.Date(string='Billing Date', default=fields.Date.context_today, required=True)
    line_ids = fields.One2many(
        comodel_name='hospital.invoice.billing.line',
        inverse_name='billing_id',
        string='Lines',
    )
    amount_total = fields.Monetary(string='Total', compute='_compute_amount', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('invoiced', 'Invoiced'),
        ('paid', 'Paid'),
    ], string='State', default='draft', tracking=True, required=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    notes = fields.Text(string='Notes')

    # ─── Computes ─────────────────────────────────────────────────────
    @api.depends('line_ids.price_subtotal')
    def _compute_amount(self):
        for rec in self:
            rec.amount_total = sum(rec.line_ids.mapped('price_subtotal'))

    # ─── CRUD ─────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.invoice.billing') or _('BILL/???')
        return super().create(vals_list)

    # ─── Actions ──────────────────────────────────────────────────────
    def action_create_invoice(self):
        """Create an account.move (draft invoice) from this billing."""
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Only draft billings can be invoiced.'))
            if not rec.line_ids:
                raise UserError(_('Cannot invoice a billing without lines.'))

            # Find the default sales journal
            journal = self.env['account.journal'].search([
                ('type', '=', 'sale'),
                ('company_id', '=', rec.company_id.id),
            ], limit=1)
            if not journal:
                raise UserError(_('No sales journal found for this company.'))

            # Build invoice lines
            invoice_lines = []
            for line in rec.line_ids:
                invoice_lines.append((0, 0, {
                    'name': line.name,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                }))

            # Create the account.move
            move = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': rec.partner_id.id,
                'invoice_date': rec.billing_date,
                'journal_id': journal.id,
                'invoice_line_ids': invoice_lines,
                'ref': rec.name,
            })
            rec.move_id = move.id
            rec.state = 'invoiced'

    def action_view_invoice(self):
        self.ensure_one()
        if not self.move_id:
            raise UserError(_('No invoice created yet.'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice'),
            'res_model': 'account.move',
            'res_id': self.move_id.id,
            'view_mode': 'form',
        }

    def action_print(self):
        """Print the billing PDF."""
        return self.env.ref('el_hospital.action_report_hospital_billing').report_action(self)

    @api.model
    def _cron_update_paid_state(self):
        """Cron job: check invoiced billings and mark as paid if move is paid."""
        billings = self.search([('state', '=', 'invoiced'), ('move_id', '!=', False)])
        for billing in billings:
            if billing.move_id.payment_state == 'paid':
                billing.state = 'paid'
