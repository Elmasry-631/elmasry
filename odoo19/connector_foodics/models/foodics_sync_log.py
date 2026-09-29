import json

from odoo import _, api, fields, models


class FoodicsSyncLog(models.Model):
    _name = "foodics.sync.log"
    _description = "Foodics Sync Log"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc, id desc"

    name = fields.Char(compute="_compute_name", store=True)
    connection_id = fields.Many2one("foodics.connection", required=True, ondelete="cascade", index=True)
    company_id = fields.Many2one(related="connection_id.company_id", store=True)
    sync_type = fields.Selection(
        [
            ("connection", "Connection"),
            ("product", "Product"),
            ("category", "Category"),
            ("customer", "Customer"),
            ("order", "Order"),
            ("payment", "Payment"),
            ("inventory", "Inventory"),
            ("tax", "Tax"),
            ("webhook", "Webhook"),
            ("retry", "Retry"),
        ],
        required=True,
        index=True,
    )
    direction = fields.Selection([("push", "Odoo to Foodics"), ("pull", "Foodics to Odoo")], required=True)
    foodics_resource = fields.Char()
    foodics_record_id = fields.Char(index=True)
    odoo_model = fields.Char()
    odoo_record_id = fields.Integer(index=True)
    status = fields.Selection(
        [
            ("pending", "Pending"),
            ("success", "Success"),
            ("failed", "Failed"),
            ("retry", "Retry Scheduled"),
            ("dead", "Dead"),
            ("skipped", "Skipped"),
        ],
        default="pending",
        required=True,
        tracking=True,
        index=True,
    )
    error_message = fields.Text()
    retry_count = fields.Integer(default=0)
    max_retries = fields.Integer(default=3)
    next_retry_date = fields.Datetime()
    execution_time = fields.Float()
    request_payload = fields.Text()
    response_data = fields.Text()

    @api.depends("sync_type", "status", "foodics_record_id", "odoo_record_id")
    def _compute_name(self):
        for log in self:
            ref = log.foodics_record_id or log.odoo_record_id or log.id or ""
            log.name = f"{dict(log._fields['sync_type'].selection).get(log.sync_type, log.sync_type)} / {ref} / {log.status}"

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            for key in ("request_payload", "response_data"):
                if isinstance(values.get(key), (dict, list)):
                    values[key] = json.dumps(values[key], indent=2, sort_keys=True)
            if values.get("connection_id") and not values.get("max_retries"):
                connection = self.env["foodics.connection"].browse(values["connection_id"])
                values["max_retries"] = connection.max_retries
        return super().create(vals_list)

    def action_retry(self):
        for log in self:
            log.write({"status": "retry", "next_retry_date": fields.Datetime.now()})
        return True

    @api.model
    def cron_retry_failed(self):
        logs = self.search([
            ("status", "in", ("failed", "retry")),
            "|",
            ("next_retry_date", "=", False),
            ("next_retry_date", "<=", fields.Datetime.now()),
        ], limit=100)
        for log in logs:
            if log.retry_count >= log.max_retries:
                log.status = "dead"
                continue
            log.write({"retry_count": log.retry_count + 1, "status": "pending"})
            log.connection_id._log_operation("retry", log.direction, log.foodics_resource or log.sync_type, "success")
        return True

    def action_view_odoo_record(self):
        self.ensure_one()
        if not self.odoo_model or not self.odoo_record_id:
            return False
        return {
            "type": "ir.actions.act_window",
            "res_model": self.odoo_model,
            "res_id": self.odoo_record_id,
            "view_mode": "form",
            "target": "current",
        }
