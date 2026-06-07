# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountPatchNumber(models.Model):
    _name = 'account.patch.number'
    _description = 'Patch Number'
    _order = 'name'
    _check_company_auto = True

    name = fields.Char(string='Patch Number', required=True, index=True)
    description = fields.Text(string='Description', translate=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_company_uniq', 'unique(name, company_id)',
         'The patch number must be unique per company!'),
    ]

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.description:
                name = '%s - %s' % (name, record.description)
            result.append((record.id, name))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', '=ilike', name + '%'), ('description', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
