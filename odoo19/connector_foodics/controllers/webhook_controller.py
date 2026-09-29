import hmac
import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class FoodicsWebhookController(http.Controller):

    @http.route("/foodics/webhook/<string:secret>", type="http", auth="public", methods=["GET"], csrf=False)
    def foodics_webhook_health(self, secret, **kwargs):
        connection = request.env["foodics.connection"].sudo().search([
            ("active", "=", True),
            ("webhook_secret", "=", secret),
        ], limit=1)
        status = "ok" if connection else "error"
        message = "Webhook endpoint is active." if connection else "Unknown webhook endpoint."
        return request.make_json_response({
            "status": status,
            "message": message,
            "connection": connection.name if connection else False,
        }, status=200 if connection else 404)

    @http.route("/foodics/webhook/<string:secret>", type="http", auth="public", methods=["POST"], csrf=False)
    def foodics_webhook_http(self, secret, **kwargs):
        try:
            payload = json.loads(request.httprequest.get_data(as_text=True) or "{}")
            result = self._handle(secret, payload)
            return request.make_json_response(result)
        except Exception as exc:
            _logger.exception("Foodics webhook processing failed")
            return request.make_json_response({"status": "error", "message": str(exc)}, status=400)

    def _handle(self, secret, payload):
        connection = request.env["foodics.connection"].sudo().search([
            ("active", "=", True),
            ("webhook_secret", "=", secret),
        ], limit=1)
        if not connection:
            return {"status": "error", "message": "Unknown webhook endpoint"}

        signature = request.httprequest.headers.get("X-Foodics-Signature")
        if signature and connection.api_secret:
            body = request.httprequest.get_data() or json.dumps(payload).encode()
            expected = hmac.new(connection.api_secret.encode(), body, "sha256").hexdigest()
            if not hmac.compare_digest(signature, expected):
                return {"status": "error", "message": "Invalid webhook signature"}

        request.env["foodics.webhook.log"].sudo().create_from_request(connection, payload or {})
        return {"status": "ok"}
