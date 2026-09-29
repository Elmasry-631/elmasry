from unittest.mock import patch

import requests

from odoo.tests.common import TransactionCase


class TestMobileWebhook(TransactionCase):
    def test_queue_payload_has_unique_event_id(self):
        event = self.env['mobile.webhook.event'].create({'event_type': 'sale_order.status_changed', 'res_model': 'sale.order', 'res_id': 1, 'record_name': 'SO001', 'company_id': self.env.company.id, 'status': 'sale', 'payload_json': '{}'})
        self.assertTrue(event.event_uuid)

    def test_failed_delivery_is_retried(self):
        self.env['ir.config_parameter'].sudo().set_param('el_mobile_webhook.endpoint', 'https://example.test/webhook')
        self.env['ir.config_parameter'].sudo().set_param('el_mobile_webhook.secret', 'secret')
        event = self.env['mobile.webhook.event'].create({'event_type': 'sale_order.status_changed', 'res_model': 'sale.order', 'res_id': 1, 'record_name': 'SO001', 'company_id': self.env.company.id, 'status': 'sale', 'payload_json': '{}'})
        with patch('requests.post', side_effect=requests.RequestException('network down')):
            self.assertFalse(event._deliver())
        self.assertEqual(event.state, 'retrying')
