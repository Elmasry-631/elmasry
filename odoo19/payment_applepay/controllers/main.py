# -*- coding: utf-8 -*-

import json
import logging
import pprint

import requests
import werkzeug

from odoo import http
from odoo.exceptions import UserError
from odoo.http import request

from odoo.addons.payment.logging import get_payment_logger

_logger = get_payment_logger(__name__)

TEST_DOMAIN = 'https://eu-test.oppwa.com'
LIVE_DOMAIN = 'https://eu-prod.oppwa.com'


class ApplepayController(http.Controller):

    @http.route('/payment/applepay/return', type='http', auth='public', csrf=False)
    def applepay_return(self, **post):
        acquirer = request.env['payment.provider'].sudo().search([('code', '=', 'applepay')], limit=1)
        _logger.info('Apple Pay return post data: %s', pprint.pformat(post))
        if not post.get('resourcePath') or not acquirer:
            return request.redirect('/payment/status')

        domain = TEST_DOMAIN if acquirer.state == 'test' else LIVE_DOMAIN
        url = f"{domain}{post.get('resourcePath')}?entityId={acquirer.applepay_entity_id}"
        authorization_bearer = f'Bearer {acquirer.applepay_authorization_bearer}'
        try:
            response = requests.get(url, headers={'Authorization': authorization_bearer})
            response_data = response.json()
        except Exception as error:
            raise UserError(str(error)) from error

        _logger.info('Apple Pay status response: %s', response_data)
        tx_sudo = request.env['payment.transaction'].sudo()
        tx = tx_sudo.search([('applepay_checkout_id', '=', post.get('id', ''))], limit=1)
        shopper_tx_id = response_data.get('customParameters', {}).get('SHOPPER_tx_id')
        if not tx and shopper_tx_id:
            tx = tx_sudo.browse(int(shopper_tx_id)).exists()
        if tx:
            response_data['tx_id'] = tx.id
            tx._process('applepay', response_data)
        return werkzeug.utils.redirect('/payment/status')

    @http.route('/shop/applepay/payment/', type='http', auth='public', methods=['POST'], csrf=False, website=True)
    def payment_applepay_card(self, **kw):
        acquirer = request.env['payment.provider'].sudo().search([('code', '=', 'applepay')], limit=1)
        kw['currency'] = 'SAR'
        _logger.info('Apple Pay intermediate page values: %s', kw)
        template = (
            'payment_applepay.payment_applepay_card'
            if acquirer.state == 'test'
            else 'payment_applepay.payment_applepay_card_live'
        )
        return request.render(template, {
            'check_out_id': kw.get('check_out_id'),
            'return_url': kw.get('applepay_return'),
            'widget_domain': acquirer._applepay_get_api_url(),
        })
