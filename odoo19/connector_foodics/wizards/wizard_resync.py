from odoo import _, fields, models


class FoodicsResyncWizard(models.TransientModel):
    _name = "foodics.resync.wizard"
    _description = "Foodics Full Resync Wizard"

    connection_id = fields.Many2one("foodics.connection", required=True)
    start_date = fields.Datetime(required=True, default=fields.Datetime.now)
    sync_products = fields.Boolean(default=True)
    sync_categories = fields.Boolean(default=True)
    sync_customers = fields.Boolean(default=True)
    sync_orders = fields.Boolean(default=True)
    sync_inventory = fields.Boolean(default=True)
    sync_taxes = fields.Boolean(default=True)

    def action_resync(self):
        self.ensure_one()
        adapters = [
            (self.sync_products, "foodics.product.adapter"),
            (self.sync_categories, "foodics.category.adapter"),
            (self.sync_customers, "foodics.customer.adapter"),
            (self.sync_orders, "foodics.order.adapter"),
            (self.sync_inventory, "foodics.inventory.adapter"),
            (self.sync_taxes, "foodics.tax.adapter"),
        ]
        for enabled, adapter_name in adapters:
            if enabled:
                self.env[adapter_name].run(self.connection_id, direction="pull")
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {"title": _("Foodics"), "message": _("Full resync completed."), "type": "success"},
        }
