"""Hospital Lab Test model — laboratory test requests and results."""

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HospitalLabTest(models.Model):
    """Laboratory test request."""

    _name = 'hospital.lab.test'
    _description = 'Hospital Lab Test'
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
    test_type = fields.Selection([
        ('blood', 'Blood'),
        ('urine', 'Urine'),
        ('stool', 'Stool'),
        ('tissue', 'Tissue'),
        ('other', 'Other'),
    ], string='Test Type', default='blood', tracking=True)
    test_name = fields.Char(string='Test Name', required=True, tracking=True)
    request_date = fields.Datetime(string='Request Date', default=fields.Datetime.now, required=True)
    result_date = fields.Datetime(string='Result Date', readonly=True)
    state = fields.Selection([
        ('requested', 'Requested'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='requested', tracking=True, required=True)
    result = fields.Text(string='Result')
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
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.lab.test') or _('LAB/???')
        return super().create(vals_list)

    # ─── State transitions ────────────────────────────────────────────
    def action_start(self):
        for rec in self:
            if rec.state != 'requested':
                raise UserError(_('Only requested tests can be started.'))
            rec.state = 'in_progress'

    def action_complete(self):
        for rec in self:
            if rec.state != 'in_progress':
                raise UserError(_('Only in-progress tests can be completed.'))
            if not rec.result:
                raise UserError(_('Please enter the result before completing.'))
            rec.state = 'completed'
            rec.result_date = fields.Datetime.now()
            # Send notification email
            template = self.env.ref('el_hospital.mail_template_lab_result_ready', raise_if_not_found=False)
            if template:
                template.send_mail(rec.id, force_send=False)

    def action_cancel(self):
        for rec in self:
            if rec.state == 'completed':
                raise UserError(_('Completed tests cannot be cancelled.'))
            rec.state = 'cancelled'
