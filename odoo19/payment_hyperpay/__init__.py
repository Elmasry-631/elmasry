# -*- coding: utf-8 -*-

from . import controllers
from . import models

from odoo.addons.payment import reset_payment_provider, setup_provider


def post_init_hook(env):
    env.cr.execute("""
        ALTER TABLE payment_provider
        ADD COLUMN IF NOT EXISTS hyperpay_data_brands VARCHAR
    """)
    setup_provider(env, 'hyperpay')


def uninstall_hook(env):
    reset_payment_provider(env, 'hyperpay')
