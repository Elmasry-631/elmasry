from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    foodics_id = fields.Char(index=True, copy=False)
    foodics_sync_enabled = fields.Boolean(default=True, copy=False)
    foodics_last_sync_date = fields.Datetime(copy=False, readonly=True)

