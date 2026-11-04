"""Hospital Prescription + Prescription Line models."""

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HospitalPrescriptionLine(models.Model):
    """One medication line in a prescription."""

    _name = 'hospital.prescription.line'
    _description = 'Prescription Line'

    prescription_id = fields.Many2one(
        comodel_name='hospital.prescription',
        string='Prescription',
        required=True,
        ondelete='cascade',
    )
    medicament_id = fields.Many2one(
        comodel_name='hospital.medicament',
        string='Medicament',
        required=True,
        ondelete='restrict',
    )
    dosage = fields.Char(string='Dosage', help='e.g. "500mg"')
    frequency = fields.Char(string='Frequency', help='e.g. "2x/day"')
    duration = fields.Char(string='Duration', help='e.g. "7 days"')
    quantity = fields.Float(string='Quantity', default=1.0)
    instructions = fields.Text(string='Instructions')
    company_id = fields.Many2one(
        comodel_name='res.company',
        related='prescription_id.company_id',
        store=True,
    )


class HospitalPrescription(models.Model):
    """Medical prescription."""

    _name = 'hospital.prescription'
    _description = 'Hospital Prescription'
    _order = 'prescription_date desc'
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
    medical_record_id = fields.Many2one(
        comodel_name='hospital.medical.record',
        string='Medical Record',
        ondelete='set null',
    )
    prescription_date = fields.Datetime(string='Date', default=fields.Datetime.now, required=True)
    line_ids = fields.One2many(
        comodel_name='hospital.prescription.line',
        inverse_name='prescription_id',
        string='Lines',
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='State', default='draft', tracking=True, required=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    # ─── CRUD ─────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.prescription') or _('RX/???')
        return super().create(vals_list)

    # ─── Actions ──────────────────────────────────────────────────────
    def action_done(self):
        for rec in self:
            if not rec.line_ids:
                raise UserError(_('Cannot confirm a prescription without medication lines.'))
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_print(self):
        """Print the prescription PDF."""
        return self.env.ref('el_hospital.action_report_hospital_prescription').report_action(self)
