from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderS(models.Model):
    _inherit = "sale.order"

    show_discount = fields.Boolean(string='Show Discount')
    is_return = fields.Boolean(string='Return')
    # credit = fields.Float(compute="compute_balance")
    # debit = fields.Float(compute="compute_balance", string="رصيد العميل ")
    balance = fields.Float(compute="compute_balance", string="رصيد العميل ")

    @api.depends('partner_id')
    def compute_balance(self):
        for rec in self:
            # rec.debit = rec.partner_id.debit
            # rec.credit = rec.partner_id.credit
            rec.balance=abs(rec.partner_id.debit-rec.partner_id.credit)

