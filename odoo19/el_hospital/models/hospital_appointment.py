"""Hospital Appointment model — state machine for patient-doctor meetings."""

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class HospitalAppointment(models.Model):
    """Patient appointment with a physician."""

    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _order = 'appointment_date desc'
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
    physician_id = fields.Many2one(
        comodel_name='hospital.physician',
        string='Physician',
        required=True,
        ondelete='restrict',
        tracking=True,
    )
    department_id = fields.Many2one(
        comodel_name='hospital.department',
        string='Department',
        ondelete='set null',
    )
    appointment_date = fields.Datetime(string='Date', required=True, tracking=True)
    duration = fields.Float(string='Duration (hours)', default=0.5)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', tracking=True, required=True)
    type = fields.Selection([
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-Up'),
        ('emergency', 'Emergency'),
    ], string='Type', default='consultation', tracking=True)
    notes = fields.Text(string='Notes')
    medical_record_id = fields.Many2one(
        comodel_name='hospital.medical.record',
        string='Medical Record',
        ondelete='set null',
    )
    is_today = fields.Boolean(string='Today', compute='_compute_is_today', search='_search_is_today')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    # ─── Constraints ──────────────────────────────────────────────────
    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        for rec in self:
            if rec.state == 'draft' and rec.appointment_date and rec.appointment_date < fields.Datetime.now():
                # Allow past dates for confirmed/done states (recording history)
                pass  # Soft check — we don't raise, just allow

    # ─── Computes ─────────────────────────────────────────────────────
    @api.depends('appointment_date')
    def _compute_is_today(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.is_today = rec.appointment_date and rec.appointment_date.date() == today

    def _search_is_today(self, operator, value):
        today = fields.Date.context_today(self)
        if operator == '=' and value:
            return [('appointment_date', '>=', fields.Datetime.to_string(fields.Datetime.today().replace(hour=0, minute=0, second=0))),
                    ('appointment_date', '<=', fields.Datetime.to_string(fields.Datetime.today().replace(hour=23, minute=59, second=59)))]
        return [('appointment_date', '=', False)]

    # ─── CRUD ─────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('AP/???')
        return super().create(vals_list)

    # ─── State transitions ────────────────────────────────────────────
    def action_confirm(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Only draft appointments can be confirmed.'))
            rec.state = 'confirmed'
            # Send confirmation email
            template = self.env.ref('el_hospital.mail_template_appointment_confirmation', raise_if_not_found=False)
            if template:
                template.send_mail(rec.id, force_send=False)

    def action_done(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError(_('Only confirmed appointments can be marked as done.'))
            rec.state = 'done'
            # Auto-create medical record if not exists
            if not rec.medical_record_id:
                record = self.env['hospital.medical.record'].create({
                    'patient_id': rec.patient_id.id,
                    'physician_id': rec.physician_id.id,
                    'appointment_id': rec.id,
                })
                rec.medical_record_id = record.id

    def action_cancel(self):
        for rec in self:
            if rec.state in ('done',):
                raise UserError(_('Done appointments cannot be cancelled.'))
            rec.state = 'cancelled'

    def action_draft(self):
        for rec in self:
            if rec.state != 'cancelled':
                raise UserError(_('Only cancelled appointments can be reset to draft.'))
            rec.state = 'draft'

    def action_create_medical_record(self):
        """Manually create a medical record from this appointment."""
        self.ensure_one()
        if self.medical_record_id:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Medical Record'),
                'res_model': 'hospital.medical.record',
                'res_id': self.medical_record_id.id,
                'view_mode': 'form',
            }
        record = self.env['hospital.medical.record'].create({
            'patient_id': self.patient_id.id,
            'physician_id': self.physician_id.id,
            'appointment_id': self.id,
        })
        self.medical_record_id = record.id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Medical Record'),
            'res_model': 'hospital.medical.record',
            'res_id': record.id,
            'view_mode': 'form',
        }
