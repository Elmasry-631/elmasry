from odoo import _, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    foodics_id = fields.Char(index=True, copy=False)
    foodics_sync_enabled = fields.Boolean(default=True, copy=False)
    foodics_last_sync_date = fields.Datetime(copy=False, readonly=True)

    def action_foodics_sync_now(self):
        connection = self.env["foodics.connection"].search([
            ("active", "=", True),
            ("sync_products", "=", True),
            ("company_id", "=", self.env.company.id),
        ], limit=1)
        if not connection:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {"title": _("Foodics"), "message": _("No active Foodics connection found."), "type": "warning"},
            }
        self.env["foodics.product.adapter"].run(connection, direction="push", records=self)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {"title": _("Foodics"), "message": _("Product sync queued."), "type": "success"},
        }


class ProductTemplate(models.Model):
    _inherit = "product.template"

    foodics_sync_enabled = fields.Boolean(default=True, copy=False)

