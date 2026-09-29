# -*- coding: utf-8 -*-

from odoo import fields, models

from odoo.addons.payment_hyperpay.const import (
    DEFAULT_PAYMENT_METHOD_CODES,
    LIVE_DOMAIN,
    PAYMENT_ICON_BRANDS,
    TEST_DOMAIN,
)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('hyperpay', 'HyperPay')],
        ondelete={'hyperpay': 'set default'},
    )
    hyperpay_authorization = fields.Char(
        string='Authorization',
        required_if_provider='hyperpay',
        groups='base.group_user',
        help='Authorization header with Bearer authentication scheme',
    )
    hyperpay_merchant_id = fields.Char(
        string='Merchant Id',
        required_if_provider='hyperpay',
        groups='base.group_user',
        help='The Merchant ID is required to authorize the request',
    )
    hyperpay_data_brands = fields.Char(
        string='Payment Brands',
        default='VISA',
        groups='base.group_user',
        help='OPPWA widget data-brands value (e.g. "VISA MASTER MADA"). '
             'Must match the channel configured for this Entity ID in HyperPay.',
    )

    def _get_default_payment_method_codes(self):
        self.ensure_one()
        if self.code != 'hyperpay':
            return super()._get_default_payment_method_codes()
        return DEFAULT_PAYMENT_METHOD_CODES

    def _hyperpay_get_api_domain(self):
        self.ensure_one()
        return LIVE_DOMAIN if self.state == 'enabled' else TEST_DOMAIN

    def _get_hyperpay_data_brands(self):
        self.ensure_one()
        if self.hyperpay_data_brands:
            return self.hyperpay_data_brands.strip()
        payment_method_names = self.payment_method_ids.mapped('name')
        brands = [
            PAYMENT_ICON_BRANDS[name.upper()]
            for name in payment_method_names
            if name.upper() in PAYMENT_ICON_BRANDS
        ]
        return ' '.join(brands) if brands else 'VISA'
