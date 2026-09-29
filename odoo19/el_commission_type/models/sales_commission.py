# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SalesCommission(models.Model):
    _name = 'sales.commission'
    _description = 'Sales Commission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True,
        readonly=True,
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        tracking=True,
    )

    team_member_type = fields.Selection([
        ('general_manager', 'General Manager'),
        ('team_manager', 'Team Manager'),
        ('team_leader', 'Team Leader'),
        ('salesperson', 'Salesperson'),
    ],
        string='Team Member Type',
        default='salesperson',
        required=True,
        tracking=True,
    )

    commission_percentage = fields.Float(
        string='Commission Percentage',
        default=0.0,
        required=True,
        tracking=True,
        help='Commission percentage for this role (0-100%)',
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        tracking=True,
    )

    @api.depends('partner_id', 'team_member_type', 'commission_percentage')
    def _compute_name(self):
        for record in self:
            type_dict = dict(self._fields['team_member_type'].selection)
            type_name = type_dict.get(record.team_member_type, '')
            record.name = f"{record.partner_id.display_name or ''} / {type_name} {int(round(record.commission_percentage * 100))}%"
