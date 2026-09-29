# -*- coding: utf-8 -*-

import re

import dateutil.parser
import pytz

from odoo import _, fields, models

from odoo.addons.payment.logging import get_payment_logger

_logger = get_payment_logger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    hyperpay_checkout_id = fields.Char(
        string='Checkout Id',
        groups='base.group_user',
        help='Unique checkout id for every HyperPay transaction',
    )

    def _get_specific_rendering_values(self, processing_values):
        if self.provider_code != 'hyperpay':
            return super()._get_specific_rendering_values(processing_values)

        return {
            'txId': self.id,
            'reference': self.reference,
        }

    def _extract_reference(self, provider_code, payment_data):
        if provider_code != 'hyperpay':
            return super()._extract_reference(provider_code, payment_data)

        reference = payment_data.get('ndc') or payment_data.get('merchantTransactionId')
        if reference and not str(reference).isdigit():
            return reference
        tx_id = payment_data.get('tx_id')
        if tx_id:
            tx = self.browse(int(tx_id))
            if tx.exists():
                return tx.reference
        return None

    def _extract_amount_data(self, payment_data):
        if self.provider_code != 'hyperpay':
            return super()._extract_amount_data(payment_data)
        return None

    def _apply_updates(self, payment_data):
        if self.provider_code != 'hyperpay':
            return super()._apply_updates(payment_data)

        result = payment_data.get('result') or {}
        result_code = result.get('code')
        if not result_code:
            self._set_error(_('HyperPay: missing payment status code.'))
            return

        success_pattern = [
            r'^(000\.000\.|000\.100\.1|000\.[36])',
            r'^(000\.400\.0[^3]|000\.400\.100)',
        ]
        pending_pattern = [
            r'^(000\.200)',
            r'^(800\.400\.5|100\.400\.500)',
        ]
        _logger.info('HyperPay feedback result: %r', result)
        if re.match(success_pattern[0], result_code) or re.match(success_pattern[1], result_code):
            date_validate = dateutil.parser.parse(payment_data.get('timestamp')).astimezone(
                pytz.utc
            ).replace(tzinfo=None)
            self.write({
                'provider_reference': payment_data.get('id'),
                'last_state_change': date_validate,
                'state_message': result.get('description', ''),
            })
            self._set_done()
        elif re.match(pending_pattern[0], result_code) or re.match(pending_pattern[1], result_code):
            self.write({'state_message': result.get('description', '')})
            self._set_pending()
        elif re.match(r'^(000\.100\.2)', result_code):
            self._set_error(result.get('description', ''))
        else:
            self.write({'state_message': result.get('description', '')})
            self._set_canceled()
