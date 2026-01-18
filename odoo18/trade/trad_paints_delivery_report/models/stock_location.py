from odoo import api, fields, models


class Location(models.Model):
    _inherit = 'stock.location'

    seq_in_report = fields.Integer(string="Sequance In Report", required=False)


