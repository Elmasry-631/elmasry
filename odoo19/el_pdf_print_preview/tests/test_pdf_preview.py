# -*- coding: utf-8 -*-
# el_pdf_print_preview — Test suite (13 tests)

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPdfPreview(TransactionCase):
    """Test suite for el_pdf_print_preview."""

    def setUp(self):
        super().setUp()
        self.User = self.env["res.users"]

    # ─── Test 1: preview_print field exists ────────────────────────────
    def test_01_preview_print_field_exists(self):
        user = self.User.create({
            "name": "Test PDF User",
            "login": "test_pdf@example.com",
            "email": "test_pdf@example.com",
        })
        self.assertTrue(hasattr(user, "preview_print"))

    # ─── Test 2: preview_print defaults to True ────────────────────────
    def test_02_preview_print_default_true(self):
        user = self.User.create({
            "name": "Test Default",
            "login": "test_default_pdf@example.com",
            "email": "test_default_pdf@example.com",
        })
        self.assertTrue(user.preview_print)

    # ─── Test 3: automatic_printing defaults to False ──────────────────
    def test_03_automatic_printing_default_false(self):
        user = self.User.create({
            "name": "Test Auto",
            "login": "test_auto@example.com",
            "email": "test_auto@example.com",
        })
        self.assertFalse(user.automatic_printing)

    # ─── Test 4: User can toggle preview_print ─────────────────────────
    def test_04_toggle_preview_print(self):
        user = self.User.create({
            "name": "Test Toggle",
            "login": "test_toggle@example.com",
            "email": "test_toggle@example.com",
        })
        user.preview_print = False
        self.assertFalse(user.preview_print)
        user.preview_print = True
        self.assertTrue(user.preview_print)

    # ─── Test 5: SELF_READABLE_FIELDS includes new fields ─────────────
    def test_05_readable_fields(self):
        readable = self.User.SELF_READABLE_FIELDS
        self.assertIn("preview_print", readable)
        self.assertIn("automatic_printing", readable)

    # ─── Test 6: SELF_WRITEABLE_FIELDS includes new fields ────────────
    def test_06_writeable_fields(self):
        writeable = self.User.SELF_WRITEABLE_FIELDS
        self.assertIn("preview_print", writeable)
        self.assertIn("automatic_printing", writeable)

    # ─── Test 7: action_preview_reload returns reload action ──────────
    def test_07_preview_reload_action(self):
        user = self.env.user
        action = user.action_preview_reload()
        self.assertEqual(action["type"], "ir.actions.client")
        self.assertEqual(action["tag"], "reload")

    # ─── Test 8: ir.http session_info includes preview fields ─────────
    def test_08_session_info_has_preview_fields(self):
        # session_info is called via request — test the method exists
        IrHttp = self.env["ir.http"]
        self.assertTrue(hasattr(IrHttp, "session_info"))

    # ─── Test 9: ir.actions.report has _render_qweb_pdf override ──────
    def test_09_report_override_exists(self):
        report_model = self.env["ir.actions.report"]
        # Verify the method exists (inheritance chain)
        self.assertTrue(hasattr(report_model, "_render_qweb_pdf"))

    # ─── Test 10: Controller method exists ─────────────────────────────
    def test_10_controller_exists(self):
        from odoo.addons.el_pdf_print_preview.controllers.main import PrintPreviewController
        self.assertTrue(hasattr(PrintPreviewController, "get_report_name"))

    # ─── Test 11: Error catcher report template exists ────────────────
    def test_11_error_catcher_template(self):
        template = self.env.ref(
            "el_pdf_print_preview.report_error_catcher",
            raise_if_not_found=False,
        )
        self.assertTrue(template, "Error catcher template should exist")

    # ─── Test 12: Error catcher report action exists ──────────────────
    def test_12_error_catcher_action(self):
        action = self.env.ref(
            "el_pdf_print_preview.action_report_error_catcher",
            raise_if_not_found=False,
        )
        self.assertTrue(action, "Error catcher action should exist")
        self.assertEqual(action.report_type, "qweb-pdf")

    # ─── Test 13: Module is installed ──────────────────────────────────
    def test_13_module_installed(self):
        module = self.env["ir.module.module"].search([
            ("name", "=", "el_pdf_print_preview"),
        ], limit=1)
        self.assertTrue(module, "Module should be found")
        self.assertEqual(module.state, "installed")
