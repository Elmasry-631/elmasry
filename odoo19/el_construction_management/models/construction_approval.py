from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ConstructionApprovalMatrix(models.Model):
    _name = 'el_construction.approval.matrix'
    _description = 'Construction Approval Matrix'
    _order = 'sequence, id'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    # Only workflows wired to the approval ledger are exposed here.
    model_name = fields.Selection([
        ('el_construction.variation.order', 'Variation Order'),
    ], required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, required=True)
    amount_from = fields.Monetary(currency_field='currency_id')
    amount_to = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    approver_ids = fields.Many2many('res.users', relation='el_construction_approval_matrix_user_rel', column1='matrix_id', column2='user_id')
    required_approvals = fields.Integer(default=1, required=True)

    @api.constrains('amount_from','amount_to','required_approvals')
    def _check_matrix(self):
        for rec in self:
            if rec.amount_from < 0 or (rec.amount_to and rec.amount_to < 0):
                raise ValidationError(_('Approval amounts cannot be negative.'))
            if rec.amount_to and rec.amount_to < rec.amount_from:
                raise ValidationError(_('Approval upper amount cannot be below lower amount.'))
            if rec.required_approvals < 1:
                raise ValidationError(_('At least one approval is required.'))
            if len(rec.approver_ids) < rec.required_approvals:
                raise ValidationError(_('The number of approvers must cover the required approval count.'))

    @api.model
    def get_approval_matrix(self, model_name, amount=0.0, company=None):
        company = company or self.env.company
        domain = [
            ('active', '=', True),
            ('model_name', '=', model_name),
            ('company_id', '=', company.id),
            ('amount_from', '<=', amount),
            '|', ('amount_to', '=', 0), ('amount_to', '>=', amount),
        ]
        return self.search(domain, order='sequence, id', limit=1)
