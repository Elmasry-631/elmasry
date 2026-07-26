# -*- coding: utf-8 -*-
# el_pdf_print_preview — ir.http extension
#
# Adds preview_print, automatic_printing, and report_layout to session_info
# so the JS client can read them without an extra RPC.

from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    """Inject PDF preview settings into session_info."""

    _inherit = "ir.http"

    def session_info(self):
        """Add preview settings to the session info payload."""
        result = super().session_info()
        user = request.env.user
        result.update({
            "preview_print": user.preview_print,
            "automatic_printing": user.automatic_printing,
            "report_layout": bool(
                user.company_id.external_report_layout_id
            ),
        })
        return result
