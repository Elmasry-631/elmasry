# -*- coding: utf-8 -*-
# el_pdf_print_preview — ir.actions.report extension
#
# Wraps _render_qweb_pdf to catch rendering errors and display a friendly
# error PDF instead of crashing the report action.
#
# v1.1.2 FIX (vs original): log full traceback server-side, show generic
# message to user (security: don't leak stack traces in PDFs).

import logging
import traceback
from odoo import models

_logger = logging.getLogger(__name__)

# Generic error message shown to end users (no internal details)
_GENERIC_ERROR_MSG = (
    "An error occurred while generating this PDF report. "
    "Please contact your system administrator and reference "
    "the server logs for details."
)


class IrActionsReport(models.Model):
    """Catch report rendering errors and show friendly error PDF."""

    _inherit = "ir.actions.report"

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None, **kwargs):
        """Wrap PDF rendering with error handling.

        If the original report fails:
        1. Log the full traceback server-side (for admins)
        2. Render a fallback error PDF with a generic message (for users)
        3. If even the fallback fails, re-raise the original exception
        """
        try:
            return super()._render_qweb_pdf(
                report_ref, res_ids=res_ids, data=data, **kwargs
            )
        except Exception as original_error:
            # Log full traceback server-side (security: don't leak to user)
            _logger.exception(
                "PDF rendering failed for report '%s' (res_ids=%s): %s",
                report_ref, res_ids, original_error,
            )

            # Try to render the friendly error PDF
            try:
                fallback_ref = "el_pdf_print_preview.report_error_catcher"
                fallback_data = {"error": _GENERIC_ERROR_MSG}
                return super()._render_qweb_pdf(
                    fallback_ref, res_ids=[], data=fallback_data, **kwargs
                )
            except Exception as fallback_error:
                _logger.error(
                    "Fallback error PDF also failed: %s", fallback_error
                )
                # Last resort: re-raise the original error
                raise original_error from fallback_error
