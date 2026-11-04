"""Hospital Medical Record (EMR) — the patient's electronic medical record."""

from odoo import api, fields, models, _


class HospitalMedicalRecord(models.Model):
    """Electronic Medical Record (EMR) for a patient."""

    _name = 'hospital.medical.record'
    _description = 'Hospital Medical Record (EMR)'
    _order = 'record_date desc'
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
    appointment_id = fields.Many2one(
        comodel_name='hospital.appointment',
        string='Appointment',
        ondelete='set null',
    )
    record_date = fields.Datetime(string='Record Date', default=fields.Datetime.now, required=True)
    chief_complaint = fields.Text(string='Chief Complaint', tracking=True)
    diagnosis = fields.Text(string='Diagnosis', tracking=True)
    treatment = fields.Text(string='Treatment', tracking=True)
    notes = fields.Text(string='Notes')

    # ─── Related records ──────────────────────────────────────────────
    prescription_ids = fields.One2many(
        comodel_name='hospital.prescription',
        inverse_name='medical_record_id',
        string='Prescriptions',
    )
    lab_test_ids = fields.One2many(
        comodel_name='hospital.lab.test',
        inverse_name='medical_record_id',
        string='Lab Tests',
    )
    radiology_order_ids = fields.One2many(
        comodel_name='hospital.radiology.order',
        inverse_name='medical_record_id',
        string='Radiology Orders',
    )
    prescription_count = fields.Integer(compute='_compute_counts')
    lab_test_count = fields.Integer(compute='_compute_counts')
    radiology_count = fields.Integer(compute='_compute_counts')

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    # ─── Computes ─────────────────────────────────────────────────────
    def _compute_counts(self):
        for rec in self:
            rec.prescription_count = len(rec.prescription_ids)
            rec.lab_test_count = len(rec.lab_test_ids)
            rec.radiology_count = len(rec.radiology_order_ids)

    # ─── CRUD ─────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.medical.record') or _('MR/???')
        return super().create(vals_list)

    # ─── Actions ──────────────────────────────────────────────────────
    def action_create_prescription(self):
        """Open a new prescription form pre-filled with this record's data."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Prescription'),
            'res_model': 'hospital.prescription',
            'view_mode': 'form',
            'context': {
                'default_patient_id': self.patient_id.id,
                'default_physician_id': self.physician_id.id,
                'default_medical_record_id': self.id,
            },
        }

    def action_open_lab_tests(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Lab Tests'),
            'res_model': 'hospital.lab.test',
            'view_mode': 'list,form',
            'domain': [('medical_record_id', '=', self.id)],
            'context': {
                'default_patient_id': self.patient_id.id,
                'default_physician_id': self.physician_id.id,
                'default_medical_record_id': self.id,
            },
        }

    def action_open_radiology(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Radiology Orders'),
            'res_model': 'hospital.radiology.order',
            'view_mode': 'list,form',
            'domain': [('medical_record_id', '=', self.id)],
            'context': {
                'default_patient_id': self.patient_id.id,
                'default_physician_id': self.physician_id.id,
                'default_medical_record_id': self.id,
            },
        }
