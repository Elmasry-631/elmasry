# -*- coding: utf-8 -*-
# el_pdf_print_preview — Controller
#
# Endpoint: /pdf_print_preview/get_report_name
# Returns: { file_name, wkhtmltopdf_state }
#
# v1.1.2 FIX (vs original):
#   - Fixed mutable default arg (data={} → data=None)
#   - Added security check (records.check_read())
#   - Removed wkhtmltopdf_state (deprecated in Odoo 19)

import json
import logging
import werkzeug.exceptions
from odoo import http
from odoo.http import request
from odoo.tools.safe_eval import safe_eval, time

_logger = logging.getLogger(__name__)


class PrintPreviewController(http.Controller):
    """Serve report metadata for the PDF preview handler."""

    @http.route(
        "/pdf_print_preview/get_report_name",
        type="jsonrpc",
        auth="user",
    )
    def get_report_name(self, report_name=False, data=None):
        """Get the printable file name for a report.

        Args:
            report_name: The report's report_name field (XML id or technical name)
            data: Optional dict with active_ids

        Returns:
            { file_name: str }
        """
        if data is None:
            data = {}

        if not report_name:
            raise werkzeug.exceptions.BadRequest(
                description="Cannot find report name in param"
            )

        report = request.env["ir.actions.report"]._get_report_from_name(
            report_name
        )
        if not report:
            raise werkzeug.exceptions.NotFound(
                description=f"Cannot find report with name ({report_name})"
            )

        file_name = ""
        print_report_name = report.print_report_name

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except (json.JSONDecodeError, TypeError):
                data = {}

        res_ids = data.get("active_ids", [])
        if res_ids and report.model:
            records = request.env[report.model].browse(res_ids)
            # Security: verify the user can read these records
            records.check_read()
            try:
                if print_report_name and records and len(records) == 1:
                    file_name = safe_eval(
                        print_report_name,
                        {"object": records, "time": time},
                    )
            except Exception as e:
                _logger.warning(
                    "Could not evaluate print_report_name for %s: %s",
                    report_name, e,
                )

        return {"file_name": file_name}
