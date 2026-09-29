"""Hospital Patient model + allergy + disease sub-models."""

from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPatientAllergy(models.Model):
    """Patient allergy record."""

    _name = 'hospital.patient.allergy'
    _description = 'Patient Allergy'

    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        string='Patient',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(string='Allergy', required=True)
    severity = fields.Selection([
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ], string='Severity', default='mild')
    notes = fields.Text(string='Notes')


class HospitalPatientDisease(models.Model):
    """Patient chronic disease record."""

    _name = 'hospital.patient.disease'
    _description = 'Patient Chronic Disease'

    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        string='Patient',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(string='Disease', required=True)
    diagnosed_date = fields.Date(string='Diagnosed Date')
    notes = fields.Text(string='Notes')


class HospitalPatient(models.Model):
    """Hospital patient — wraps res.partner."""

    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # ─── Identity ──────────────────────────────────────────────────────
    name = fields.Char(string='Name', compute='_compute_name', store=True, index=True, tracking=True)
    ref = fields.Char(string='Patient Code', readonly=True, copy=False, index=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contact',
        required=True,
        ondelete='restrict',
    )

    # ─── Demographics ─────────────────────────────────────────────────
    birth_date = fields.Date(string='Birth Date', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender', tracking=True)
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ], string='Blood Type')

    # ─── Related fields from partner ──────────────────────────────────
    phone = fields.Char(related='partner_id.phone', readonly=False)
    email = fields.Char(related='partner_id.email', readonly=False)
    address = fields.Char(related='partner_id.contact_address', string='Address', readonly=True)
    image_1920 = fields.Image(related='partner_id.image_1920', readonly=False)

    # ─── Medical ──────────────────────────────────────────────────────
    physician_id = fields.Many2one(
        comodel_name='hospital.physician',
        string='Primary Physician',
        ondelete='set null',
        tracking=True,
    )
    department_id = fields.Many2one(
        comodel_name='hospital.department',
        string='Department',
        ondelete='set null',
    )
    allergy_ids = fields.One2many(
        comodel_name='hospital.patient.allergy',
        inverse_name='patient_id',
        string='Allergies',
    )
    chronic_disease_ids = fields.One2many(
        comodel_name='hospital.patient.disease',
        inverse_name='patient_id',
        string='Chronic Diseases',
    )

    # ─── Smart button counts ──────────────────────────────────────────
    appointment_count = fields.Integer(
        string='Appointments',
        compute='_compute_appointment_count',
    )
    admission_count = fields.Integer(
        string='Admissions',
        compute='_compute_admission_count',
    )

    # ─── Misc ─────────────────────────────────────────────────────────
    active = fields.Boolean(default=True, tracking=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    notes = fields.Text(string='Notes')

    # ─── Constraints ──────────────────────────────────────────────────
    _partner_unique = models.Constraint(
        'unique(partner_id)',
        'A patient record already exists for this contact!',
        )

    # ─── Computes ─────────────────────────────────────────────────────
    @api.depends('partner_id.name', 'ref')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.partner_id.name or _('Unnamed Patient')

    @api.depends('name', 'ref')
    def _compute_display_name(self):
        for rec in self:
            if rec.ref:
                rec.display_name = f'[{rec.ref}] {rec.name}'
            else:
                rec.display_name = rec.name

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                born = rec.birth_date
                rec.age = today.year - born.year - (
                    (today.month, today.day) < (born.month, born.day)
                )
            else:
                rec.age = 0

    @api.depends('partner_id')
    def _compute_appointment_count(self):
        Appointment = self.env['hospital.appointment']
        for rec in self:
            rec.appointment_count = Appointment.search_count([
                ('patient_id', '=', rec.id),
            ])

    @api.depends('partner_id')
    def _compute_admission_count(self):
        Admission = self.env['hospital.admission']
        for rec in self:
            rec.admission_count = Admission.search_count([
                ('patient_id', '=', rec.id),
            ])

    # ─── CRUD ─────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('ref'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('PAT/???')
        return super().create(vals_list)

    # ─── Smart buttons ────────────────────────────────────────────────
    def action_open_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Appointments'),
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_open_admissions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Admissions'),
            'res_model': 'hospital.admission',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }
