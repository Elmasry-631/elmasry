# -*- coding: utf-8 -*-

import logging

from odoo import _, models
from odoo.exceptions import ValidationError, UserError


_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None, **kwargs):
        result = False, False
        messageError = False
        try:
            result = super()._render_qweb_pdf(report_ref, res_ids=res_ids, data=data, **kwargs)
        except (UserError, ValidationError) as e:
            messageError = str(e)
        except Exception:
            _logger.exception("PDF rendering failed for report %s", report_ref)
            messageError = _(
                "An unexpected error occurred while generating this PDF. "
                "Please contact your system administrator."
            )

        if messageError:
            report_ref = "pdf_print_preview.report_error_catcher"
            data = {'error': messageError}
            result = super()._render_qweb_pdf(report_ref, res_ids=[], data=data, **kwargs)
        return result
