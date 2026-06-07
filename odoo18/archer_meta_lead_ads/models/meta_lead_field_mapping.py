# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MetaLeadFieldMapping(models.Model):
    _name = 'meta.lead.field.mapping'
    _description = 'Meta Lead Field Mapping'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    form_id = fields.Many2one('meta.lead.form', required=True, ondelete='cascade')
    company_id = fields.Many2one(related='form_id.company_id', store=True, readonly=True)
    meta_field_key = fields.Char(required=True, help="Meta field key from the lead form.")
    odoo_field_id = fields.Many2one(
        'ir.model.fields',
        string='CRM Lead Field',
        required=True,
        ondelete='cascade',
        domain="[('model', '=', 'crm.lead'), ('store', '=', True), ('ttype', 'not in', ('one2many', 'binary', 'reference', 'html', 'json', 'properties'))]",
    )
    odoo_field_name = fields.Char(related='odoo_field_id.name', store=True, readonly=True)
    odoo_field_ttype = fields.Selection(related='odoo_field_id.ttype', store=True, readonly=True)
    relation = fields.Char(related='odoo_field_id.relation', readonly=True)
    lookup_field = fields.Char(
        help="Field used to match relational targets such as country, state, or tags.",
    )
    transform = fields.Selection(
        [('none', 'None'), ('lowercase', 'Lowercase'), ('strip', 'Strip')],
        default='none',
        required=True,
    )
    is_default = fields.Boolean(default=False)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            'meta_form_field_unique',
            'unique(form_id, meta_field_key)',
            'Meta field key must be unique per form.',
        ),
    ]

    @api.onchange('odoo_field_id')
    def _onchange_odoo_field_id(self):
        for rec in self:
            if rec.odoo_field_id and rec.odoo_field_id.ttype in ('many2one', 'many2many') and not rec.lookup_field:
                rec.lookup_field = 'name'
