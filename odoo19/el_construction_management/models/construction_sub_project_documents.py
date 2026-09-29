from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ConstructionSubProjectDocument(models.Model):
    _name = 'el_construction.sub.project.document'
    _description = 'Sub Project Document'

    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project', required=True, ondelete='cascade')
    name = fields.Char(string='Document Name', required=True)
    document = fields.Binary(string='Document', attachment=True, required=True)
    document_name = fields.Char(string='File Name')
    doc_type = fields.Selection([
        ('drawing', 'Drawing'),
        ('specification', 'Specification'),
        ('contract', 'Contract'),
        ('report', 'Report'),
        ('other', 'Other'),
    ], string='Type', default='other')
    notes = fields.Text(string='Notes')
