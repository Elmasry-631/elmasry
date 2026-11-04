"""Hospital Ward model — rooms/wings of the hospital."""

from odoo import api, fields, models, _


class HospitalWard(models.Model):
    """Hospital ward (room or wing)."""

    _name = 'hospital.ward'
    _description = 'Hospital Ward'
    _order = 'code'
    _rec_name = 'display_name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, index=True)
    display_name = fields.Char(compute='_compute_display_name', store=True)
    department_id = fields.Many2one(
        comodel_name='hospital.department',
        string='Department',
        ondelete='set null',
    )
    ward_type = fields.Selection([
        ('general', 'General'),
        ('private', 'Private'),
        ('icu', 'ICU'),
        ('maternity', 'Maternity'),
        ('pediatric', 'Pediatric'),
    ], string='Type', default='general')
    floor = fields.Char(string='Floor')
    bed_capacity = fields.Integer(string='Bed Capacity', default=1)
    bed_count = fields.Integer(string='Beds', compute='_compute_bed_stats')
    occupied_count = fields.Integer(string='Occupied', compute='_compute_bed_stats')
    available_count = fields.Integer(string='Available', compute='_compute_bed_stats')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)

    _code_unique = models.Constraint(
        'unique(code)',
        'Ward code must be unique!',
        )

    @api.depends('name', 'code')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'[{rec.code}] {rec.name}' if rec.code else rec.name

    @api.depends('bed_capacity')
    def _compute_bed_stats(self):
        Bed = self.env['hospital.bed']
        for rec in self:
            beds = Bed.search([('ward_id', '=', rec.id)])
            rec.bed_count = len(beds)
            rec.occupied_count = len(beds.filtered(lambda b: b.state == 'occupied'))
            rec.available_count = len(beds.filtered(lambda b: b.state == 'available'))

    def action_open_beds(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Beds in %s') % self.display_name,
            'res_model': 'hospital.bed',
            'view_mode': 'list,form',
            'domain': [('ward_id', '=', self.id)],
            'context': {'default_ward_id': self.id},
        }
