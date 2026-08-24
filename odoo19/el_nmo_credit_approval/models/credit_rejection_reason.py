from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CreditRejectionReason(models.Model):
    _name = 'credit.rejection.reason'
    _description = 'Credit Rejection Reason'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Reason',
        required=True,
        translate=True,
        help='The rejection reason text displayed to the salesperson.',
    )

    description = fields.Text(
        string='Description',
        help='Detailed explanation of when to use this reason.',
    )

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sort order for the selection list.',
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help='Disable without deleting. Inactive reasons are hidden from selection.',
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        help='Each rejection reason belongs to a company.',
    )

    _name_uniq_per_company = models.Constraint(
        'UNIQUE(name, company_id)',
        'Rejection reason must be unique per company!',
    )