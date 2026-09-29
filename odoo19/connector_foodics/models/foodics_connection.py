import logging
import secrets

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class FoodicsConnection(models.Model):
    _name = "foodics.connection"
    _description = "Foodics Connection"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    name = fields.Char(required=True, tracking=True)
    sequence = fields.Integer(default=10)
    business_id = fields.Char(required=True, tracking=True)
    api_key = fields.Char(groups="connector_foodics.group_foodics_admin")
    api_secret = fields.Char(groups="connector_foodics.group_foodics_admin")
    token = fields.Char(groups="connector_foodics.group_foodics_admin", copy=False)
    token_expires_at = fields.Datetime(copy=False)
    base_url = fields.Char(
        default="https://api.foodics.com/v5",
        required=True,
        help="Foodics API base URL from the Postman collection baseURL variable, for example https://api.foodics.com/v5.",
    )
    test_mode = fields.Boolean(
        string="Test Mode",
        help="Use local mock responses instead of calling Foodics. Enable this when you do not have Foodics API access yet.",
        tracking=True,
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("connected", "Connected"),
            ("error", "Error"),
            ("disabled", "Disabled"),
        ],
        default="draft",
        tracking=True,
    )
    last_successful_call = fields.Datetime(readonly=True)
    last_sync_date = fields.Datetime(readonly=True)
    last_error = fields.Text(readonly=True)
    webhook_secret = fields.Char(copy=False, groups="connector_foodics.group_foodics_admin")
    webhook_url = fields.Char(compute="_compute_webhook_url")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)

    sync_products = fields.Boolean(default=True)
    sync_categories = fields.Boolean(default=True)
    sync_customers = fields.Boolean(default=True)
    sync_orders = fields.Boolean(default=True)
    sync_inventory = fields.Boolean(default=True)
    sync_taxes = fields.Boolean(default=True)
    sync_mode = fields.Selection(
        [("batch", "Batch"), ("webhook", "Real-time Webhook"), ("both", "Batch and Webhook")],
        default="batch",
        required=True,
    )

    product_sync_interval = fields.Integer(default=30)
    order_sync_interval = fields.Integer(default=15)
    inventory_sync_interval = fields.Integer(default=30)
    customer_sync_interval = fields.Integer(default=60)
    max_retries = fields.Integer(default=3)
    rate_limit = fields.Integer(default=100)

    default_customer_id = fields.Many2one("res.partner")
    order_journal_id = fields.Many2one("account.journal", domain="[('company_id', '=', company_id)]")
    order_import_mode = fields.Selection(
        [("sale_order", "Sales Order"), ("invoice", "Invoice")],
        default="sale_order",
        required=True,
    )
    order_prefix = fields.Char(default="FDC-")

    mapping_ids = fields.One2many("foodics.mapping", "connection_id")
    webhook_event_ids = fields.One2many("foodics.webhook.event", "connection_id")
    branch_mapping_ids = fields.One2many("foodics.branch.mapping", "connection_id")
    sync_log_ids = fields.One2many("foodics.sync.log", "connection_id")
    sync_log_count = fields.Integer(compute="_compute_counts")
    failed_log_count = fields.Integer(compute="_compute_counts")

    _business_company_unique = models.Constraint(
        "unique(business_id, company_id)",
        "Foodics business must be unique per company.",
    )

    @api.depends("sync_log_ids.status")
    def _compute_counts(self):
        Log = self.env["foodics.sync.log"]
        for connection in self:
            connection.sync_log_count = Log.search_count([("connection_id", "=", connection.id)])
            connection.failed_log_count = Log.search_count([
                ("connection_id", "=", connection.id),
                ("status", "in", ("failed", "dead")),
            ])

    def _compute_webhook_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url", "")
        for connection in self:
            connection.webhook_url = (
                f"{base_url}/foodics/webhook/{connection.webhook_secret}"
                if base_url and connection.webhook_secret else False
            )

    @api.constrains("base_url")
    def _check_base_url(self):
        for connection in self:
            if connection.base_url and not connection.test_mode and not connection.base_url.startswith("https://"):
                raise ValidationError(_("Foodics base URL must use HTTPS."))

    def action_generate_webhook_secret(self):
        for connection in self:
            connection.webhook_secret = secrets.token_urlsafe(32)

    def action_open_sync_logs(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Sync Logs"),
            "res_model": "foodics.sync.log",
            "view_mode": "list,form",
            "domain": [("connection_id", "=", self.id)],
            "context": {"default_connection_id": self.id},
        }

    def action_open_failed_sync_logs(self):
        action = self.action_open_sync_logs()
        action["domain"] = [("connection_id", "=", self.id), ("status", "in", ("failed", "dead"))]
        return action

    def action_test_connection(self):
        for connection in self:
            result = connection._test_connection()
            if not result:
                raise UserError(_("Connection test failed. Check the last error field."))
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {"title": _("Foodics"), "message": _("Connection test succeeded."), "type": "success"},
        }

    def _test_connection(self):
        self.ensure_one()
        try:
            payload = self.env["foodics.api.client"].call(self, "GET", "/apps")
        except Exception as exc:
            self.write({"state": "error", "last_error": str(exc)})
            self._log_operation("connection", "pull", "apps", "failed", error_message=str(exc))
            _logger.exception("Foodics connection test failed for %s", self.display_name)
            return False
        self.write({"state": "connected", "last_error": False, "last_successful_call": fields.Datetime.now()})
        self._log_operation("connection", "pull", "apps", "success", response_data=payload)
        return True

    def _log_operation(self, sync_type, direction, resource, status, **values):
        self.ensure_one()
        return self.env["foodics.sync.log"].sudo().create({
            "connection_id": self.id,
            "sync_type": sync_type,
            "direction": direction,
            "foodics_resource": resource,
            "status": status,
            **values,
        })

    def _run_adapter(self, adapter_name, direction="pull"):
        for connection in self.filtered("active"):
            adapter = self.env[adapter_name]
            try:
                adapter.run(connection, direction=direction)
                connection.last_sync_date = fields.Datetime.now()
            except Exception as exc:
                connection.write({"state": "error", "last_error": str(exc)})
                connection._log_operation(
                    adapter_name.replace("foodics.", "").replace(".adapter", ""),
                    direction,
                    adapter_name,
                    "failed",
                    error_message=str(exc),
                )
                _logger.exception("Foodics adapter %s failed for %s", adapter_name, connection.display_name)

    @api.model
    def cron_sync_products(self):
        self.search([("active", "=", True), ("sync_products", "=", True)])._run_adapter("foodics.product.adapter", "push")

    @api.model
    def cron_sync_categories(self):
        self.search([("active", "=", True), ("sync_categories", "=", True)])._run_adapter("foodics.category.adapter", "pull")

    @api.model
    def cron_sync_customers(self):
        self.search([("active", "=", True), ("sync_customers", "=", True)])._run_adapter("foodics.customer.adapter", "pull")

    @api.model
    def cron_sync_orders(self):
        self.search([("active", "=", True), ("sync_orders", "=", True)])._run_adapter("foodics.order.adapter", "pull")

    @api.model
    def cron_sync_inventory(self):
        self.search([("active", "=", True), ("sync_inventory", "=", True)])._run_adapter("foodics.inventory.adapter", "pull")

    @api.model
    def cron_sync_taxes(self):
        self.search([("active", "=", True), ("sync_taxes", "=", True)])._run_adapter("foodics.tax.adapter", "pull")
