from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    foodics_id = fields.Char(index=True, copy=False)
    foodics_sync_enabled = fields.Boolean(default=True, copy=False)
    foodics_last_sync_date = fields.Datetime(copy=False, readonly=True)

