from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestFoodicsModels(TransactionCase):

    def test_connection_generates_webhook_url(self):
        connection = self.env["foodics.connection"].create({
            "name": "Test Foodics",
            "business_id": "business-1",
            "api_key": "key",
            "base_url": "https://api.foodics.com",
            "company_id": self.env.company.id,
        })
        connection.action_generate_webhook_secret()
        self.assertTrue(connection.webhook_secret)

    def test_sync_log_serializes_payloads(self):
        connection = self.env["foodics.connection"].create({
            "name": "Test Foodics",
            "business_id": "business-2",
            "api_key": "key",
            "base_url": "https://api.foodics.com",
            "company_id": self.env.company.id,
        })
        log = self.env["foodics.sync.log"].create({
            "connection_id": connection.id,
            "sync_type": "product",
            "direction": "push",
            "status": "success",
            "request_payload": {"name": "Burger"},
        })
        self.assertIn("Burger", log.request_payload)

