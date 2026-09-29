# investment_club/models/investment_club.py
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class InvestmentClub(models.Model):
    _name = 'investment.club'
    _description = 'Investment Club'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'display_name'

    name_ar = fields.Char(
        string='Club Name (Arabic)',
        required=True,
        tracking=True,
        help='Arabic Club Name'
    )

    name_en = fields.Char(
        string='Club Name (English)',
        required=True,
        tracking=True,
        help='Club name in English'
    )

    name = fields.Char(
        string='Club Name',
        compute='_compute_display_name_ar',
        store=False,
    )

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name_ar',
        store=True,
    )

    code = fields.Char(string='Club Code', readonly=True, copy=False)

    is_active = fields.Boolean(
        string='Active Club',
        default=True,
        tracking=True,
        help='Club status: active or inactive'
    )

    active = fields.Boolean(default=True)

    administrative_fees = fields.Float(
        string='Administrative Fees',
        default=0.0,
        tracking=True,
        help='Club administrative fees - added as a separate invoice line'
    )

    max_members = fields.Integer(
        string='Max Members',
        default=0,
        tracking=True,
        help='Maximum number of club members (0 = without Limit)'
    )

    current_members_count = fields.Integer(
        string='Current Members Count',
        compute='_compute_counts',
        store=True
    )

    terms_conditions = fields.Text(
        string='Terms and Conditions',
        help='Club-specific terms and conditions'
    )

    project_ids = fields.One2many(
        'investment.project',
        'club_id',
        string='Projects'
    )

    member_ids = fields.One2many(
        'investment.membership',
        'club_id',
        string='Members'
    )

    active_members_count = fields.Integer(
        string='Active Members',
        compute='_compute_counts',
        store=True
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )

    notes = fields.Text(string='Notes')

    @api.depends('name_ar', 'name_en')
    def _compute_display_name_ar(self):
        for club in self:
            if club.name_ar and club.name_en:
                club.display_name = '%s / %s' % (club.name_ar, club.name_en)
                club.name = club.display_name
            elif club.name_ar:
                club.display_name = club.name_ar
                club.name = club.name_ar
            elif club.name_en:
                club.display_name = club.name_en
                club.name = club.name_en
            else:
                club.display_name = ''
                club.name = ''

    @api.depends('member_ids.state')
    def _compute_counts(self):
        for club in self:
            all_members = club.member_ids
            club.active_members_count = len(all_members.filtered(lambda m: m.state == 'active'))
            club.current_members_count = len(all_members.filtered(
                lambda m: m.state not in ('cancelled', 'terminated')
            ))

    @api.constrains('max_members')
    def _check_max_members(self):
        for club in self:
            if club.max_members > 0 and club.current_members_count > club.max_members:
                raise ValidationError(_(
                    'Cannot exceed maximum members limit (%s) for club %s!'
                ) % (club.max_members, club.display_name))

    def toggle_active(self):
        for club in self:
            club.is_active = not club.is_active

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code'):
                vals['code'] = self.env['ir.sequence'].next_by_code('investment.club') or 'New'
        return super(InvestmentClub, self).create(vals_list)
