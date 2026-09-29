from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

from .workflow_mixin import ConstructionWorkflowMixin


class ConstructionTaskControls(ConstructionWorkflowMixin, models.Model):
    _inherit = 'el_construction.task'

    progress_mode = fields.Selection([('time','Time Based'),('quantity','Physical Quantity'),('manual','Manual')], default='time', required=True, tracking=True)
    planned_quantity = fields.Float(string='Planned Quantity')
    completed_quantity = fields.Float(string='Completed Quantity')
    quantity_uom_id = fields.Many2one('uom.uom', string='Progress UoM')
    physical_progress = fields.Float(compute='_compute_physical_progress', store=True)

    @api.depends('planned_quantity','completed_quantity')
    def _compute_physical_progress(self):
        for rec in self:
            rec.physical_progress = min(100.0, max(0.0, rec.completed_quantity / rec.planned_quantity * 100.0)) if rec.planned_quantity > 0 else 0.0

    @api.depends('state', 'planned_hours', 'total_hours', 'progress_mode', 'planned_quantity', 'completed_quantity')
    def _compute_progress(self):
        super()._compute_progress()
        for rec in self:
            if rec.progress_mode == 'quantity': rec.progress = rec.physical_progress
            elif rec.progress_mode == 'manual': rec.progress = min(100.0, max(0.0, rec.progress))
