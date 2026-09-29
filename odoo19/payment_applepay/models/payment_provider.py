# -*- coding: utf-8 -*-

import json
import logging

import requests
from urllib.parse import urljoin

from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons.payment_applepay.const import DEFAULT_PAYMENT_METHOD_CODES

_logger = logging.getLogger(__name__)

TEST_DOMAIN = 'https://eu-test.oppwa.com'
LIVE_DOMAIN = 'https://eu-prod.oppwa.com'


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('applepay', 'Apple Pay')],
        ondelete={'applepay': 'set default'},
    )
    applepay_entity_id = fields.Char(
        string='Merchant ID/Entity Id',
        required_if_provider='applepay',
        groups='base.group_user',
    )
    applepay_authorization_bearer = fields.Char(
        string='Authorization Bearer',
        required_if_provider='applepay',
        groups='base.group_user',
    )

    def _get_default_payment_method_codes(self):
        self.ensure_one()
        if self.code != 'applepay':
            return super()._get_default_payment_method_codes()
        return DEFAULT_PAYMENT_METHOD_CODES

    def _applepay_get_api_url(self):
        self.ensure_one()
        return TEST_DOMAIN if self.state == 'test' else LIVE_DOMAIN

    def _get_authorize_urls(self):
        return urljoin(self.get_base_url(), 'shop/applepay/payment/')

    @staticmethod
    def _partner_split_name(partner_name):
        if not partner_name:
            return ['', 'guest']
        return [' '.join(partner_name.split()[:-1]), ' '.join(partner_name.split()[-1:])]

    def _get_authenticate_apple_pay(self, values):
        self.ensure_one()
        url = f'{self._applepay_get_api_url()}/v1/checkouts'
        authorization_bearer = f'Bearer {self.applepay_authorization_bearer}'
        partner = self.env['res.partner'].browse(values['partner_id'])
        last_name = self._partner_split_name(partner.name)[1]
        data = {
            'entityId': self.applepay_entity_id,
            'amount': str(format(values['amount'], '.2f')),
            'currency': 'SAR',
            'paymentType': 'DB',
            'merchantTransactionId': values.get('reference'),
            'customer.email': partner.email,
            'customer.givenName': partner.name or 'guest',
            'customer.companyName': partner.company_id.name,
            'customer.phone': partner.phone,
            'billing.street1': partner.street or 'Riyadh',
            'billing.state': partner.state_id.name or 'Riyadh',
            'billing.country': partner.country_id.code or 'SA',
            'billing.postcode': partner.zip,
            'customer.surname': last_name or 'guest',
        }
        try:
            response = requests.post(url, headers={'Authorization': authorization_bearer}, data=data)
            response_data = response.json()
            _logger.info('Apple Pay checkout response: %s', response_data)
            return response_data.get('id')
        except Exception as error:
            raise UserError(str(error)) from error

    def applepay_form_generate_values(self, values):
        self.ensure_one()
        currency = self.env['res.currency'].browse(values['currency_id'])
        base_url = self.get_base_url()
        check_out_id = self._get_authenticate_apple_pay(values)
        applepay_tx_values = dict(values)
        applepay_tx_values.update({
            'entityId': self.applepay_entity_id,
            'check_out_id': check_out_id,
            'amount': str(format(values['amount'], '.2f')),
            'currency': currency.name or '',
            'paymentBrand': 'APPLEPAY',
            'paymentType': 'DB',
            'merchantTransactionId': values.get('reference'),
            'shopperResultUrl': urljoin(base_url, '/shop/applepay/payment/'),
            'applepay_return': urljoin(base_url, '/payment/applepay/return'),
            'widget_domain': self._applepay_get_api_url(),
            'custom': json.dumps({
                'return_url': applepay_tx_values.pop('return_url'),
            }) if applepay_tx_values.get('return_url') else False,
        })
        return applepay_tx_values
