from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderS(models.Model):
    _inherit = "sale.order"

    seq_in_report = fields.Integer(string="Sequance In Report", required=False)


