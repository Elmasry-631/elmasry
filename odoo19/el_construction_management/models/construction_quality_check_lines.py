from .workflow_mixin import ConstructionWorkflowMixin

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ConstructionQualityCheckLine(models.Model):
    _name = 'el_construction.quality.check.line'
    _description = 'Quality Check Point'
    _order = 'sequence, id'

    quality_check_id = fields.Many2one(
        'el_construction.quality.check', string='Quality Check', required=True, ondelete='cascade', index=True,
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(string='Check Point', required=True)
    description = fields.Text(string='Description')
    standard = fields.Char(string='Standard / Specification')
    result = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('na', 'N/A'),
    ], string='Result', default='na', required=True)
    remarks = fields.Text(string='Remarks')

    @api.model_create_multi
    def create(self, vals_list):
        checks = self.env['el_construction.quality.check'].browse([v.get('quality_check_id') for v in vals_list if v.get('quality_check_id')])
        if any(check.state in ('pass', 'conditional', 'fail', 'recheck', 'closed', 'cancelled') for check in checks):
            raise UserError(_('Check Points cannot be added after the inspection result is recorded.'))
        return super().create(vals_list)

    def write(self, vals):
        for rec in self:
            if rec.quality_check_id.state in ('pass', 'conditional', 'fail', 'recheck', 'closed', 'cancelled'):
                raise UserError(_('Check Points cannot be changed after the inspection result is recorded.'))
        return super().write(vals)

    def unlink(self):
        if any(rec.quality_check_id.state in ('pass', 'conditional', 'fail', 'recheck', 'closed', 'cancelled') for rec in self):
            raise UserError(_('Check Points cannot be deleted after the inspection result is recorded.'))
        return super().unlink()

    @api.constrains('quality_check_id', 'result', 'name')
    def _check_editable_parent(self):
        for rec in self:
            if rec.quality_check_id.state in ('closed', 'cancelled'):
                raise ValidationError(_('Check Points cannot be changed on a Closed or Cancelled Quality Check.'))
            if rec.quality_check_id.state in ('pass', 'conditional', 'fail'):
                raise ValidationError(_('Check Points cannot be changed after an inspection result is recorded.'))

class ConstructionQualityCheckImage(models.Model):
    _name = 'el_construction.quality.check.image'
    _description = 'Quality Check Evidence Image'
    _order = 'id'

    quality_check_id = fields.Many2one(
        'el_construction.quality.check', string='Quality Check', required=True, ondelete='cascade', index=True,
    )
    name = fields.Char(string='Description', required=True)
    image = fields.Binary(string='Image', attachment=True, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        checks = self.env['el_construction.quality.check'].browse([v.get('quality_check_id') for v in vals_list if v.get('quality_check_id')])
        if any(check.state in ('pass', 'conditional', 'fail', 'recheck', 'closed', 'cancelled') for check in checks):
            raise UserError(_('Evidence cannot be added after the inspection result is recorded.'))
        return super().create(vals_list)

    def write(self, vals):
        for rec in self:
            if rec.quality_check_id.state in ('pass', 'conditional', 'fail', 'recheck', 'closed', 'cancelled'):
                raise UserError(_('Evidence cannot be changed after the inspection result is recorded.'))
        return super().write(vals)

    def unlink(self):
        if any(rec.quality_check_id.state in ('pass', 'conditional', 'fail', 'recheck', 'closed', 'cancelled') for rec in self):
            raise UserError(_('Evidence cannot be deleted after the inspection result is recorded.'))
        return super().unlink()

    @api.constrains('quality_check_id')
    def _check_editable_parent(self):
        for rec in self:
            if rec.quality_check_id.state in ('pass', 'conditional', 'fail', 'closed', 'cancelled'):
                raise ValidationError(_('Evidence cannot be changed after the inspection result is recorded.'))
