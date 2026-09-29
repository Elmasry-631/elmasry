from .workflow_mixin import ConstructionWorkflowMixin

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ConstructionQualityPoint(models.Model):
    _name = 'el_construction.quality.point'
    _description = 'Project Quality Point'
    _order = 'sequence, id'

    name = fields.Char(string='Check Point', required=True)
    sequence = fields.Integer(default=10)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True, ondelete='cascade', index=True)
    company_id = fields.Many2one('res.company', related='project_id.company_id', store=True, index=True)
    check_type = fields.Selection([
        ('material', 'Material Inspection'), ('workmanship', 'Workmanship Inspection'),
        ('safety', 'Safety Check'), ('structural', 'Structural Inspection'),
        ('electrical', 'Electrical Inspection'), ('plumbing', 'Plumbing Inspection'),
        ('final', 'Final Inspection'), ('other', 'Other'),
    ], string='Check Type', default='material', required=True)
    description = fields.Text(string='Inspection Requirement')
    standard = fields.Char(string='Standard / Specification')
    active = fields.Boolean(default=True)

    _project_point_name_unique = models.Constraint(
        'UNIQUE(project_id, name)',
        'A quality point with the same name already exists in this project.',
    )


class ConstructionQualityCheckQualityPointExtension(ConstructionWorkflowMixin, models.Model):
    _inherit = 'el_construction.quality.check'

    def action_load_project_quality_points(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_('Project quality points can only be loaded while the Quality Check is Draft.'))
            points = self.env['el_construction.quality.point'].search([
                ('project_id', '=', rec.project_id.id),
                ('active', '=', True),
                ('check_type', '=', rec.check_type),
            ], order='sequence, id')
            if not points:
                points = self.env['el_construction.quality.point'].search([
                    ('project_id', '=', rec.project_id.id), ('active', '=', True)
                ], order='sequence, id')
            existing = set(rec.check_line_ids.mapped('name'))
            commands = []
            for point in points:
                if point.name in existing:
                    continue
                commands.append((0, 0, {
                    'sequence': point.sequence,
                    'name': point.name,
                    'description': point.description,
                    'standard': point.standard,
                    'result': 'na',
                }))
            if commands:
                rec.write({'check_line_ids': commands})
        return True
