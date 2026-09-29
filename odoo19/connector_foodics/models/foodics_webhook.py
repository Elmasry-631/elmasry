import json

from odoo import api, fields, models


class FoodicsWebhookEvent(models.Model):
    _name = "foodics.webhook.event"
    _description = "Foodics Webhook Event Subscription"
    _order = "connection_id, event_type"

    connection_id = fields.Many2one("foodics.connection", ondelete="cascade")
    name = fields.Char(required=True)
    event_type = fields.Char(required=True)
    active = fields.Boolean(default=True)


class FoodicsWebhookLog(models.Model):
    _name = "foodics.webhook.log"
    _description = "Foodics Webhook Log"
    _order = "received_at desc, id desc"

    connection_id = fields.Many2one("foodics.connection", required=True, ondelete="cascade", index=True)
    event_type = fields.Char(required=True, index=True)
    event_id = fields.Char(index=True)
    payload = fields.Text(required=True)
    received_at = fields.Datetime(default=fields.Datetime.now, required=True)
    processed = fields.Boolean(default=False)
    processing_date = fields.Datetime()
    status = fields.Selection(
        [("pending", "Pending"), ("done", "Done"), ("failed", "Failed"), ("skipped", "Skipped")],
        default="pending",
        required=True,
        index=True,
    )
    error_message = fields.Text()
    sync_log_id = fields.Many2one("foodics.sync.log")

    _event_unique = models.Constraint(
        "unique(connection_id, event_id)",
        "Webhook event was already received.",
    )

    @api.model
    def create_from_request(self, connection, payload):
        event_type = payload.get("event") or payload.get("event_type") or "unknown"
        event_id = payload.get("id") or payload.get("event_id")
        webhook_log = self.create({
            "connection_id": connection.id,
            "event_type": event_type,
            "event_id": event_id,
            "payload": json.dumps(payload, indent=2, sort_keys=True),
        })
        webhook_log.process()
        return webhook_log

    def process(self):
        for webhook in self:
            try:
                payload = json.loads(webhook.payload or "{}")
                sync_log = webhook.connection_id._log_operation(
                    "webhook",
                    "pull",
                    webhook.event_type,
                    "success",
                    foodics_record_id=payload.get("resource_id") or payload.get("id"),
                    response_data=payload,
                )
                webhook.write({
                    "processed": True,
                    "processing_date": fields.Datetime.now(),
                    "status": "done",
                    "sync_log_id": sync_log.id,
                })
            except Exception as exc:
                webhook.write({
                    "processing_date": fields.Datetime.now(),
                    "status": "failed",
                    "error_message": str(exc),
                })
