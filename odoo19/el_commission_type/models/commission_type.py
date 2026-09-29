# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SalesCommissionType(models.Model):
    _name = 'sales.commission.type'
    _description = 'Sales Commission Type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'

    # Team Member Type Selection
    team_member_type = fields.Selection([
        ('general_manager', 'General Manager'),
        ('team_manager', 'Team Manager'),
        ('team_leader', 'Team Leader'),
        ('salesperson', 'Salesperson'),
    ],
        string='Team Member Type',
        default='general_manager',
        required=True,
        tracking=True
    )

    # Commission Percentage
    commission_percentage = fields.Float(
        string='Commission Percentage',
        default=0.0,
        required=True,
        tracking=True,
        help='Commission percentage for this role (0-100%)'
    )

    # Company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        tracking=True
    )

    # Computed Name Field (READONLY - Auto-generated)
    name = fields.Char(
        string='Commission Name',
        compute='_compute_name',
        store=True,
        readonly=True,
        translate=False
    )

    @api.depends('team_member_type', 'commission_percentage')
    def _compute_name(self):
        for record in self:
            type_dict = dict(self._fields['team_member_type'].selection)
            type_name = type_dict.get(record.team_member_type, '')
            record.name = f"{type_name} {int(round(record.commission_percentage * 100))}%"




    @api.constrains('name', 'company_id')
    def _check_unique_name_per_company(self):
        """Ensure commission name is unique per company."""
        for record in self:
            domain = [
                ('name', '=', record.name),
                ('company_id', '=', record.company_id.id),
                ('id', '!=', record.id)
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(_('Commission name must be unique per company!'))

    def name_get(self):
        """Return the display name for records."""
        result = []
        for record in self:
            result.append((record.id, record.name))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100):
        """Search by computed name or team member type."""
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('team_member_type', operator, name)]
        return self._search(domain + args, limit=limit)