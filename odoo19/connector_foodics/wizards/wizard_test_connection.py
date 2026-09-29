from odoo import _, fields, models


class FoodicsTestConnectionWizard(models.TransientModel):
    _name = "foodics.test.connection.wizard"
    _description = "Foodics Test Connection Wizard"

    connection_id = fields.Many2one("foodics.connection", required=True)
    result = fields.Text(readonly=True)

    def action_test(self):
        self.ensure_one()
        success = self.connection_id._test_connection()
        self.result = _("Connection successful.") if success else self.connection_id.last_error
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }
