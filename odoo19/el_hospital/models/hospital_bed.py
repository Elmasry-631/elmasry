"""Hospital Bed model — individual beds within wards."""

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HospitalBed(models.Model):
    """Hospital bed — a physical bed within a ward."""

    _name = 'hospital.bed'
    _description = 'Hospital Bed'
    _order = 'ward_id, bed_number'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    ward_id = fields.Many2one(
        comodel_name='hospital.ward',
        string='Ward',
        required=True,
        ondelete='restrict',
    )
    bed_number = fields.Char(string='Bed Number', required=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    ], string='State', default='available', tracking=True, required=True)
    admission_id = fields.Many2one(
        comodel_name='hospital.admission',
        string='Current Admission',
        ondelete='set null',
    )
    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        string='Patient',
        related='admission_id.patient_id',
        store=True,
        readonly=True,
    )
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        comodel_name='res.company',
        related='ward_id.company_id',
        store=True,
    )

    _ward_bed_unique = models.Constraint(
        'unique(ward_id, bed_number)',
        'Bed number must be unique within a ward!',
        )

    @api.depends('ward_id.name', 'ward_id.code', 'bed_number')
    def _compute_name(self):
        for rec in self:
            ward_code = rec.ward_id.code or rec.ward_id.name or ''
            rec.name = f'{ward_code}-{rec.bed_number}' if ward_code else rec.bed_number

    def action_set_maintenance(self):
        for rec in self:
            if rec.state == 'occupied':
                raise UserError(_('Cannot put an occupied bed into maintenance. Discharge the patient first.'))
            rec.state = 'maintenance'

    def action_set_available(self):
        for rec in self:
            if rec.state == 'occupied':
                raise UserError(_('Cannot free an occupied bed manually. Discharge the patient first.'))
            rec.state = 'available'
