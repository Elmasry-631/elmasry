"""Hospital Department model — master data for hospital departments."""

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalDepartment(models.Model):
    """Hospital department (e.g. Cardiology, Pediatrics)."""

    _name = 'hospital.department'
    _description = 'Hospital Department'
    _order = 'name'
    _rec_name = 'display_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, translate=True, tracking=True)
    code = fields.Char(string='Code', required=True, index=True, tracking=True)
    display_name = fields.Char(compute='_compute_display_name', store=True)
    head_physician_id = fields.Many2one(
        comodel_name='hospital.physician',
        string='Head Physician',
        ondelete='set null',
    )
    bed_capacity = fields.Integer(string='Bed Capacity', default=0)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)

    _code_unique = models.Constraint(
        'unique(code)',
        'Department code must be unique!',
        )

    @api.depends('name', 'code')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'[{rec.code}] {rec.name}' if rec.code else rec.name
