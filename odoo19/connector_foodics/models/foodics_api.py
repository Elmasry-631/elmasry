import json
import time
from urllib.parse import urljoin

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class FoodicsApiClient(models.AbstractModel):
    _name = "foodics.api.client"
    _description = "Foodics API Client"

    @api.model
    def call(self, connection, method, endpoint, payload=None, params=None, timeout=30):
        connection.ensure_one()
        if connection.test_mode:
            connection.write({"last_successful_call": fields.Datetime.now(), "last_error": False})
            return self._mock_response(connection, method, endpoint, payload=payload, params=params)

        url = urljoin(connection.base_url.rstrip("/") + "/", endpoint.lstrip("/"))
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if connection.token:
            headers["Authorization"] = f"Bearer {connection.token}"
        elif connection.api_key:
            headers["Authorization"] = f"Bearer {connection.api_key}"

        started = time.monotonic()
        try:
            response = requests.request(
                method.upper(),
                url,
                data=json.dumps(payload) if payload is not None else None,
                params=params,
                headers=headers,
                timeout=timeout,
            )
        except requests.RequestException as exc:
            raise UserError(_("Foodics API request failed: %s") % exc) from exc

        elapsed = time.monotonic() - started
        if response.status_code >= 400:
            raise UserError(_("Foodics API error %(status)s: %(body)s") % {
                "status": response.status_code,
                "body": response.text[:500],
            })
        connection.write({"last_successful_call": fields.Datetime.now(), "last_error": False})
        try:
            result = response.json() if response.text else {}
        except ValueError:
            result = {"raw": response.text}
        result["_execution_time"] = elapsed
        return result

    @api.model
    def _mock_response(self, connection, method, endpoint, payload=None, params=None):
        resource = endpoint.rstrip("/").split("/")[-1] or "mock"
        if endpoint.rstrip("/") == "/apps":
            return {
                "data": [{
                    "id": connection.business_id or "mock-app",
                    "name": connection.name,
                    "mode": "test",
                }],
                "_execution_time": 0.0,
            }
        if method.upper() == "GET":
            return {
                "data": [],
                "meta": {"mock": True, "resource": resource, "params": params or {}},
                "_execution_time": 0.0,
            }
        return {
            "id": f"mock-{resource}",
            "data": {"id": f"mock-{resource}", "payload": payload or {}},
            "meta": {"mock": True, "resource": resource},
            "_execution_time": 0.0,
        }
