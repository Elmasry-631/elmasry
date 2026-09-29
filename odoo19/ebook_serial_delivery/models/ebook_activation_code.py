# -*- coding: utf-8 -*-
"""
4Jawaly SMS helper
====================
Standalone helper used by stock_picking.py to send the activation
Serial Number(s) by SMS, in addition to the email. Kept in its own
file so credentials/HTTP concerns don't clutter stock_picking.py.
"""
import base64
import logging
import requests

from odoo import models, _

_logger = logging.getLogger(__name__)

JAWALY_BASE_URL = 'https://api-sms.4jawaly.com/api/v1/'
JAWALY_TIMEOUT = 10


class StockPickingJawalySms(models.AbstractModel):
    _name = 'ebook.jawaly.sms.helper'
    _description = 'eBook 4Jawaly SMS Helper'

    def send_serial_sms(self, picking):
        """Send the delivered Serial Number(s) by SMS for `picking`
        (a stock.picking already validated with ebook moves done).
        Never raises: failures are logged and posted to the chatter,
        exactly like the email failure path in stock_picking.py.
        """
        order = picking.sale_id
        ICP = self.env['ir.config_parameter'].sudo()
        api_key = ICP.get_param('jawaly.api_key')
        api_secret = ICP.get_param('jawaly.api_secret')
        sender_name = ICP.get_param('jawaly.sender_name')

        if not (api_key and api_secret and sender_name):
            _logger.warning(
                "4Jawaly credentials not configured; skipping SMS for picking %s.",
                picking.name
            )
            return

        phone = order.partner_id.mobile or order.partner_id.phone
        if not phone:
            picking.message_post(body=_(
                "⚠️ Customer has no mobile number on file; activation SMS was not sent."
            ))
            return

        serials = picking.move_line_ids.filtered(
            lambda ml: ml.product_id.is_ebook_with_codes and ml.lot_id
        ).mapped('lot_id.name')

        if not serials:
            return

        message = _("Your eBook Serial Number(s): %s") % ", ".join(serials)

        auth_hash = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_hash}",
        }
        payload = {
            "messages": [{
                "text": message,
                "numbers": [phone],
                "sender": sender_name,
            }]
        }

        try:
            response = requests.post(
                JAWALY_BASE_URL + 'account/area/sms/send',
                headers=headers,
                json=payload,
                timeout=JAWALY_TIMEOUT,
            )
            response_json = response.json()

            if response.status_code == 200:
                picking.message_post(body=_("SMS sent to %s with Serial Number(s).") % phone)
            else:
                error_msg = response_json.get("message", f"HTTP {response.status_code}")
                _logger.error("4Jawaly SMS failed for picking %s: %s", picking.name, error_msg)
                picking.message_post(body=_(
                    "⚠️ SMS sending failed for delivery %(picking)s: %(error)s"
                ) % {'picking': picking.name, 'error': error_msg})

        except Exception:
            _logger.exception("Failed to send activation SMS for picking %s.", picking.name)
            picking.message_post(body=_(
                "⚠️ SMS sending failed for delivery %s (network/API error). "
                "Email delivery is unaffected."
            ) % picking.name)