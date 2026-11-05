from odoo.exceptions import UserError
from odoo.tests import TransactionCase

from ..models.delete_protection import allow_internal_deletion


class TestGlobalDeleteProtection(TransactionCase):
    def test_regular_user_cannot_delete_records(self):
        partner = self.env["res.partner"].create({"name": "Protected"})
        with self.assertRaises(UserError):
            partner.unlink()

    def test_admin_cannot_delete_attachments(self):
        attachment = self.env["ir.attachment"].create(
            {"name": "protected.txt", "raw": b"content", "type": "binary"}
        )
        admin_attachment = attachment.with_user(self.env.ref("base.user_admin"))
        with self.assertRaises(UserError):
            admin_attachment.unlink()

    def test_context_cannot_enable_bypass(self):
        partner = self.env["res.partner"].create({"name": "Protected"})
        with self.assertRaises(UserError):
            partner.with_context(_el_global_delete_protection=True).unlink()

    def test_trusted_scope_allows_narrow_server_cleanup(self):
        partner = self.env["res.partner"].create({"name": "Cleanup candidate"})
        with allow_internal_deletion():
            partner.unlink()
        self.assertFalse(partner.exists())
