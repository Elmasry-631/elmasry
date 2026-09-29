"""Hospital Physician model — links to hr.employee + res.partner."""

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalPhysician(models.Model):
    """Hospital physician (doctor)."""

    _name = 'hospital.physician'
    _description = 'Hospital Physician'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', compute='_compute_name', store=True, index=True, tracking=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contact',
        required=True,
        ondelete='restrict',
    )
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        ondelete='set null',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        ondelete='set null',
    )
    specialization = fields.Char(string='Specialization', tracking=True)
    department_id = fields.Many2one(
        comodel_name='hospital.department',
        string='Department',
        ondelete='set null',
        tracking=True,
    )
    medical_license = fields.Char(string='Medical License', required=True, tracking=True)
    phone = fields.Char(related='partner_id.phone', readonly=False)
    email = fields.Char(related='partner_id.email', readonly=False)
    image_1920 = fields.Image(related='partner_id.image_1920', readonly=False)
    active = fields.Boolean(default=True, tracking=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    _medical_license_unique = models.Constraint(
        'unique(medical_license)',
        'Medical license must be unique!',
        )

    @api.depends('partner_id.name')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.partner_id.name or _('Unnamed Physician')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.phone = self.partner_id.phone
            self.email = self.partner_id.email

    def action_open_patients(self):
        """Smart button: open patients for this physician."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Patients of %s') % self.name,
            'res_model': 'hospital.patient',
            'view_mode': 'list,form',
            'domain': [('physician_id', '=', self.id)],
            'context': {'default_physician_id': self.id},
        }
