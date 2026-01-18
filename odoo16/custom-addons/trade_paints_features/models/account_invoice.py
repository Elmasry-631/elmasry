from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo import exceptions, _
from odoo.exceptions import  ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    before_discount = fields.Monetary("Before Discount", compute="_discount_rate")

    @api.depends('invoice_line_ids.quantity','invoice_line_ids.price_unit')
    def _discount_rate(self):
        for rec in self:
            total_cost = 0
            for line in rec.invoice_line_ids:
                total_cost += (line.quantity * line.price_unit )

            rec.before_discount = total_cost