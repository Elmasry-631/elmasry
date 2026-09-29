# -*- coding: utf-8 -*-
"""
stock.picking extension
=========================
Holds the "already emailed" guard + the actual send logic. The trigger
itself (deciding *when* to call `_send_ebook_serial_email`) lives in
`stock_move.py`, hooked on `_action_done()` — see that file for why.
"""
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    ebook_email_sent = fields.Boolean(default=False, copy=False)

    def action_resend_ebook_email(self):
        """Manual retry button for support staff (e.g. email failed the
        first time). Available from the picking form/list view.
        """
        for picking in self:
            picking._send_ebook_serial_email()

    def _send_ebook_serial_email(self):
        self.ensure_one()
        order = self.sale_id
        # Chosen in Inventory > Settings > eBook Serial Email, and editable
        # from there; falls back to the module's default template.
        template = self.company_id._get_ebook_serial_mail_template()
        if not template:
            _logger.warning(
                "eBook serial email template not found; delivery %s validated "
                "but no email was sent.", self.name
            )
            return

        # The template's report_template_ids (see mail_template_data.xml)
        # already renders and attaches action_report_ebook_serial — no
        # need to manually render the PDF or build an ir.attachment here.
        # The layout comes from the template's own Layout field.
        try:
            template.with_context(picking_id=self.id).send_mail(
                order.id,
                force_send=True,
            )
            self.ebook_email_sent = True
            self.env['ebook.jawaly.sms.helper'].send_serial_sms(self)
        except Exception:
            _logger.exception(
                "Failed to send eBook serial email for delivery %s (order %s). "
                "Delivery stays done; ebook_email_sent stays False so "
                "action_resend_ebook_email can retry.", self.name, order.name
            )
