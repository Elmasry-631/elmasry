# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import re

from odoo import _, fields, models

from odoo.addons.payment.logging import get_payment_logger

_logger = get_payment_logger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    applepay_checkout_id = fields.Char(
        string='Checkout Id',
        groups='base.group_user',
        help='Unique checkout id for every Apple Pay transaction',
    )

    def _get_specific_rendering_values(self, processing_values):
        if self.provider_code != 'applepay':
            return super()._get_specific_rendering_values(processing_values)

        rendering_values = self.provider_id.applepay_form_generate_values(processing_values)
        self.applepay_checkout_id = rendering_values.get('check_out_id')
        rendering_values.update({
            'api_url': self.provider_id._get_authorize_urls(),
            'txId': self.id,
            'reference': self.reference,
        })
        return rendering_values

    def _extract_reference(self, provider_code, payment_data):
        if provider_code != 'applepay':
            return super()._extract_reference(provider_code, payment_data)

        reference = payment_data.get('merchantTransactionId') or payment_data.get('ndc')
        if reference:
            return reference
        tx_id = payment_data.get('tx_id')
        if tx_id:
            tx = self.browse(int(tx_id))
            if tx.exists():
                return tx.reference
        return None

    def _extract_amount_data(self, payment_data):
        if self.provider_code != 'applepay':
            return super()._extract_amount_data(payment_data)
        return None

    def _apply_updates(self, payment_data):
        if self.provider_code != 'applepay':
            return super()._apply_updates(payment_data)

        result = payment_data.get('result') or {}
        status_code = result.get('code')
        if not status_code:
            self._set_error(_('Apple Pay: missing payment status code.'))
            return

        success_regex_1 = re.compile(r'000\.000\.|000\.100\.1|000\.[36]').search(status_code)
        success_regex_2 = re.compile(r'000\.400\.0[^3]|000\.400\.100').search(status_code)
        pending_regex_1 = re.compile(r'000\.200').search(status_code)
        pending_regex_2 = re.compile(r'800\.400\.5|100\.400\.500').search(status_code)
        error_regex_1 = re.compile(r'000\.100\.2').search(status_code)

        self.provider_reference = payment_data.get('id')
        if success_regex_1 or success_regex_2:
            _logger.info('Apple Pay success: %s', result.get('description') or 'success')
            self._set_done()
        elif pending_regex_1 or pending_regex_2:
            _logger.info('Apple Pay pending: %s', result.get('description') or 'pending')
            self._set_pending()
        elif error_regex_1:
            error_message = result.get('description') or 'error'
            _logger.info('Apple Pay error: %s', error_message)
            self._set_canceled(state_message=_('Apple Pay: %s', error_message))
        else:
            _logger.info('Apple Pay canceled: %s', result.get('description') or 'cancel')
            self._set_canceled()
