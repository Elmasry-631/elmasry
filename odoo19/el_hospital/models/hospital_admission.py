"""Hospital Admission — patient inpatient stay (admit/discharge workflow)."""

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HospitalAdmission(models.Model):
    """Patient admission (inpatient stay)."""

    _name = 'hospital.admission'
    _description = 'Hospital Admission'
    _order = 'admission_date desc'
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
    ward_id = fields.Many2one(
        comodel_name='hospital.ward',
        string='Ward',
        ondelete='restrict',
    )
    bed_id = fields.Many2one(
        comodel_name='hospital.bed',
        string='Bed',
        ondelete='restrict',
        domain="[('ward_id', '=', ward_id), ('state', '=', 'available')]",
    )
    admission_date = fields.Datetime(string='Admission Date', default=fields.Datetime.now, required=True, tracking=True)
    discharge_date = fields.Datetime(string='Discharge Date', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', tracking=True, required=True)
    reason = fields.Text(string='Reason for Admission', tracking=True)
    discharge_notes = fields.Text(string='Discharge Notes')
    days_count = fields.Integer(string='Days Admitted', compute='_compute_days_count', store=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    # ─── Computes ─────────────────────────────────────────────────────
    @api.depends('admission_date', 'discharge_date')
    def _compute_days_count(self):
        for rec in self:
            if rec.admission_date and rec.discharge_date:
                delta = rec.discharge_date - rec.admission_date
                rec.days_count = delta.days
            elif rec.admission_date:
                delta = fields.Datetime.now() - rec.admission_date
                rec.days_count = delta.days
            else:
                rec.days_count = 0

    # ─── CRUD ─────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.admission') or _('ADM/???')
        return super().create(vals_list)

    # ─── State transitions ────────────────────────────────────────────
    def action_admit(self):
        """Admit the patient: reserve the bed (state → occupied)."""
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Only draft admissions can be admitted.'))
            if not rec.bed_id:
                raise UserError(_('Please select a bed before admitting.'))
            if rec.bed_id.state != 'available':
                raise UserError(_('Selected bed is not available.'))
            rec.state = 'admitted'
            # Reserve the bed
            rec.bed_id.write({
                'state': 'occupied',
                'admission_id': rec.id,
            })

    def action_discharge(self):
        """Discharge the patient: free the bed (state → available)."""
        for rec in self:
            if rec.state != 'admitted':
                raise UserError(_('Only admitted patients can be discharged.'))
            rec.state = 'discharged'
            rec.discharge_date = fields.Datetime.now()
            # Free the bed
            if rec.bed_id:
                rec.bed_id.write({
                    'state': 'available',
                    'admission_id': False,
                })
            # Send discharge email
            template = self.env.ref('el_hospital.mail_template_discharge_summary', raise_if_not_found=False)
            if template:
                template.send_mail(rec.id, force_send=False)

    def action_cancel(self):
        """Cancel the admission — only draft/admitted can be cancelled."""
        for rec in self:
            if rec.state == 'discharged':
                raise UserError(_('Discharged admissions cannot be cancelled.'))
            # Free the bed if was admitted
            if rec.state == 'admitted' and rec.bed_id:
                rec.bed_id.write({
                    'state': 'available',
                    'admission_id': False,
                })
            rec.state = 'cancelled'

    def action_draft(self):
        """Reset a cancelled admission to draft."""
        for rec in self:
            if rec.state != 'cancelled':
                raise UserError(_('Only cancelled admissions can be reset to draft.'))
            rec.state = 'draft'
