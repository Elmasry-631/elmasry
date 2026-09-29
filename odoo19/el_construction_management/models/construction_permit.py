from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ConstructionPermit(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.permit'
    _description = 'Construction Permit & Approval'
    _order = 'expiry_date asc, id desc'

    project_id = fields.Many2one('el_construction.project', string='Project', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True, index=True)
    name = fields.Char(string='Permit Name', required=True)
    is_required_for_execution = fields.Boolean(string='Required for Execution', default=False, tracking=True)
    permit_type = fields.Selection([
        ('building', 'Building Permit'),
        ('environmental', 'Environmental Clearance'),
        ('fire', 'Fire Safety'),
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('other', 'Other'),
    ], string='Type', default='building')
    issue_date = fields.Date(string='Issue Date')
    expiry_date = fields.Date(string='Expiry Date')
    issuing_authority = fields.Char(string='Issuing Authority')
    document = fields.Binary(string='Document', attachment=True)
    document_name = fields.Char(string='File Name')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('expired', 'Expired'),
        ('rejected', 'Rejected'),
    ], string='Status', default='pending')
    notes = fields.Text(string='Notes')

    @api.constrains('project_id', 'company_id')
    def _check_company(self):
        for rec in self:
            if rec.project_id and rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('Permit company must match the Project company.'))

    @api.constrains('issue_date', 'expiry_date')
    def _check_dates(self):
        for rec in self:
            if rec.issue_date and rec.expiry_date and rec.issue_date > rec.expiry_date:
                raise ValidationError(_('Permit expiry date must be after the issue date.'))

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Permit Status.'))
        return super().write(vals)

    def action_approve(self):
        return self._transition('approved', {'pending': {'approved'}})

    def action_reject(self):
        return self._transition('rejected', {'pending': {'rejected'}}, manager=True)

    def action_expire(self):
        return self._transition('expired', {'approved': {'expired'}}, manager=True)

    def action_reset_pending(self):
        return self._transition('pending', {'rejected': {'pending'}, 'expired': {'pending'}}, manager=True)
