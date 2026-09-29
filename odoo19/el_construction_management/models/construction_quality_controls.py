from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

from .workflow_mixin import ConstructionWorkflowMixin


class ConstructionNCR(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.ncr'
    _description = 'Construction Non-Conformance Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(readonly=True, default='New', copy=False)
    project_id = fields.Many2one('el_construction.project', required=True, ondelete='restrict')
    sub_project_id = fields.Many2one('el_construction.sub.project', ondelete='restrict')
    quality_check_id = fields.Many2one('el_construction.quality.check', ondelete='restrict')
    company_id = fields.Many2one(related='project_id.company_id', store=True, index=True)
    date = fields.Date(default=fields.Date.context_today, required=True)
    description = fields.Text(required=True)
    severity = fields.Selection([('minor','Minor'),('major','Major'),('critical','Critical')], default='minor', required=True)
    state = fields.Selection([('draft','Draft'),('open','Open'),('action','Corrective Action'),('verification','Verification'),('closed','Closed'),('cancelled','Cancelled')], default='draft', tracking=True)
    capa_ids = fields.One2many('el_construction.capa', 'ncr_id')
    root_cause = fields.Text()
    verified_by = fields.Many2one('res.users', readonly=True)
    closed_by = fields.Many2one('res.users', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.ncr') or 'NCR/%(year)s/%(month)s/%(seq)s'
        return super().create(vals_list)

    def action_open(self):
        return self._transition('open', {'draft': {'open'}})

    def action_start_capa(self):
        if not self.capa_ids:
            raise UserError(_('Create at least one CAPA action before moving to Corrective Action.'))
        return self._transition('action', {'open': {'action'}})

    def action_verify(self):
        if any(c.state != 'done' for c in self.capa_ids):
            raise UserError(_('All CAPA actions must be Done before verification.'))
        result = self._transition('verification', {'action': {'verification'}})
        self.write({'verified_by': self.env.user.id})
        return result

    def action_close(self):
        self._require_manager()
        return self._transition('closed', {'verification': {'closed'}}, manager=True)

    def action_cancel(self):
        self._require_manager()
        return self._transition('cancelled', {'draft': {'cancelled'}, 'open': {'cancelled'}, 'action': {'cancelled'}, 'verification': {'cancelled'}}, manager=True)

class ConstructionCAPA(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.capa'
    _description = 'Construction CAPA Action'
    _order = 'deadline, id'

    ncr_id = fields.Many2one('el_construction.ncr', required=True, ondelete='cascade')
    project_id = fields.Many2one(related='ncr_id.project_id', store=True, index=True)
    company_id = fields.Many2one(related='ncr_id.company_id', store=True, index=True)
    name = fields.Char(required=True)
    action_type = fields.Selection([('corrective','Corrective'),('preventive','Preventive')], required=True)
    owner_id = fields.Many2one('res.users', required=True)
    deadline = fields.Date(required=True)
    state = fields.Selection([('open','Open'),('done','Done'),('cancelled','Cancelled')], default='open', tracking=True)
    completion_notes = fields.Text()

    def write(self, vals):
        for rec in self:
            if rec.state in ('done', 'cancelled') and set(vals) - {'message_follower_ids'}:
                raise UserError(_('Finalized CAPA actions cannot be modified.'))
        return super().write(vals)

    def action_done(self):
        if any(not rec.completion_notes or not rec.completion_notes.strip() for rec in self):
            raise UserError(_('Completion notes are required before closing a CAPA action.'))
        return self._transition('done', {'open': {'done'}})

    def action_cancel(self):
        self._require_manager()
        return self._transition('cancelled', {'open': {'cancelled'}}, manager=True)
