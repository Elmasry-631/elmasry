# -*- coding: utf-8 -*-
# el_pdf_print_preview — res.users extension
#
# Adds per-user toggles for PDF preview and automatic printing.

import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    """Add PDF preview preferences to users."""

    _inherit = "res.users"

    preview_print = fields.Boolean(
        string="Preview PDF before print",
        default=True,
        help="When enabled, clicking a Print button opens a PDF.js viewer "
             "dialog instead of downloading the PDF file.",
    )

    automatic_printing = fields.Boolean(
        string="Automatic printing",
        default=False,
        help="When enabled, the browser's print dialog opens automatically "
             "after the PDF is generated (requires popup permission).",
    )

    def action_preview_reload(self):
        """Reload the interface after settings change."""
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    @property
    def SELF_READABLE_FIELDS(self):
        """Expose preview_print + automatic_printing to the client session."""
        return super().SELF_READABLE_FIELDS + [
            "preview_print",
            "automatic_printing",
        ]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        """Allow users to write their own preview settings."""
        return super().SELF_WRITEABLE_FIELDS + [
            "preview_print",
            "automatic_printing",
        ]
