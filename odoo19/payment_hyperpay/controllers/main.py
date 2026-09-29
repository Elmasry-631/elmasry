# -*- coding: utf-8 -*-

import requests

from odoo import http
from odoo.http import request

from odoo.addons.payment.logging import get_payment_logger
from odoo.addons.payment_hyperpay.const import LIVE_DOMAIN, TEST_DOMAIN

_logger = get_payment_logger(__name__)


def _get_checkout_id(**params):
    auth = params.pop('auth', '')
    env = params.pop('env')
    domain = LIVE_DOMAIN if env == 'enabled' else TEST_DOMAIN
    url_string = f'{domain}/v1/checkouts'
    headers = {'Authorization': auth}
    try:
        response = requests.post(url=url_string, data=params, headers=headers, timeout=60)
        response_data = response.json()
        result = response_data.get('result') or {}
        if result.get('parameterErrors') or result.get('code', '').startswith('8'):
            _logger.error(
                'HyperPay checkout rejected (env=%s): %s',
                env,
                response_data,
            )
            return response_data
        return response_data
    except Exception as error:
        _logger.exception('HyperPay checkout creation failed: %s', error)
        return {}


class HyperPayController(http.Controller):

    @http.route('/payment/hyperpay/checkout/create', type='jsonrpc', auth='public')
    def create_hyperpay_checkout(self, txId=None, **kwargs):
        _logger.info('HyperPay checkout create request: txId=%s', txId)
        tx = request.env['payment.transaction'].sudo().browse(int(txId or 0)).exists()
        if not tx:
            return {}

        provider = tx.provider_id
        partner = tx.partner_id
        partner_phone = tx.partner_phone or partner.phone or ''
        checkout_params = {
            'auth': f'Bearer {provider.hyperpay_authorization}',
            'entityId': provider.hyperpay_merchant_id,
            'amount': f'{tx.amount:.2f}',
            'currency': tx.currency_id.name or '',
            'paymentType': 'DB',
            'env': provider.state,
            'customParameters[SHOPPER_tx_id]': tx.id,
            'merchantTransactionId': tx.id,
            'billing.street1': partner.street or '',
            'billing.street2': partner.street2 or '',
            'billing.city': partner.city or '',
            'billing.state': partner.state_id.name or '',
            'billing.postcode': partner.zip or '',
            'billing.country': partner.country_id.code or '',
            'customer.givenName': partner.name or '',
            'customer.surname': partner.name or '',
            'customer.email': partner.email or '',
            'customer.mobile': partner_phone,
            'customer.phone': partner_phone,
        }
        response_data = _get_checkout_id(**checkout_params)
        checkout_id = response_data.get('id')
        if checkout_id:
            tx.hyperpay_checkout_id = checkout_id

        data_brands = provider._get_hyperpay_data_brands()
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        result = response_data.get('result') or {}
        return {
            'checkoutId': checkout_id or '',
            'domain': provider._hyperpay_get_api_domain(),
            'base_url': base_url,
            'data_brands': data_brands,
            'entityId': provider.hyperpay_merchant_id,
            'acq': provider.id,
            'error_message': result.get('description') if not checkout_id else None,
        }

    @http.route('/payment/hyperpay/result', type='http', auth='public', csrf=False, website=True)
    def hyperpay_shopper_result(self, **post):
        provider = request.env['payment.provider'].sudo().browse(int(post.get('acq') or 0)).exists()
        if not provider or not post.get('resourcePath'):
            return request.redirect('/payment/status')

        domain = provider._hyperpay_get_api_domain()
        url = f"{domain}/{post.get('resourcePath')}?entityId={provider.hyperpay_merchant_id}"
        headers = {'Authorization': f'Bearer {provider.hyperpay_authorization}'}
        response_data = requests.get(url, headers=headers, timeout=60).json()
        _logger.info('HyperPay result response: %r', response_data)

        tx_sudo = request.env['payment.transaction'].sudo()
        tx = tx_sudo.search([('hyperpay_checkout_id', '=', post.get('id', ''))], limit=1)
        shopper_tx_id = response_data.get('customParameters', {}).get('SHOPPER_tx_id')
        if not tx and shopper_tx_id:
            tx = tx_sudo.browse(int(shopper_tx_id)).exists()
        if tx:
            response_data['tx_id'] = tx.id
            tx._process('hyperpay', response_data)
        return request.redirect('/payment/status')
