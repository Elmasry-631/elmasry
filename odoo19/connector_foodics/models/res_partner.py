from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    foodics_id = fields.Char(index=True, copy=False)
    foodics_loyalty_points = fields.Float(copy=False)
    foodics_sync_enabled = fields.Boolean(default=True, copy=False)
    foodics_last_sync_date = fields.Datetime(copy=False, readonly=True)

