"""Hospital Radiology Order model — imaging requests and results."""

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HospitalRadiologyOrder(models.Model):
    """Radiology / imaging order."""

    _name = 'hospital.radiology.order'
    _description = 'Hospital Radiology Order'
    _order = 'request_date desc'
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
        string='Requesting Physician',
        required=True,
        ondelete='restrict',
        tracking=True,
    )
    medical_record_id = fields.Many2one(
        comodel_name='hospital.medical.record',
        string='Medical Record',
        ondelete='set null',
    )
    modality = fields.Selection([
        ('xray', 'X-Ray'),
        ('ct', 'CT Scan'),
        ('mri', 'MRI'),
        ('ultrasound', 'Ultrasound'),
        ('mammography', 'Mammography'),
    ], string='Modality', default='xray', tracking=True)
    study_name = fields.Char(string='Study Name', required=True, tracking=True)
    request_date = fields.Datetime(string='Request Date', default=fields.Datetime.now, required=True)
    result_date = fields.Datetime(string='Result Date', readonly=True)
    state = fields.Selection([
        ('requested', 'Requested'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='requested', tracking=True, required=True)
    result = fields.Text(string='Result / Findings')
    image_ids = fields.Many2many(
        comodel_name='ir.attachment',
        string='Images',
    )
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
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.radiology.order') or _('RAD/???')
        return super().create(vals_list)

    # ─── State transitions ────────────────────────────────────────────
    def action_start(self):
        for rec in self:
            if rec.state != 'requested':
                raise UserError(_('Only requested orders can be started.'))
            rec.state = 'in_progress'

    def action_complete(self):
        for rec in self:
            if rec.state != 'in_progress':
                raise UserError(_('Only in-progress orders can be completed.'))
            rec.state = 'completed'
            rec.result_date = fields.Datetime.now()

    def action_cancel(self):
        for rec in self:
            if rec.state == 'completed':
                raise UserError(_('Completed orders cannot be cancelled.'))
            rec.state = 'cancelled'
