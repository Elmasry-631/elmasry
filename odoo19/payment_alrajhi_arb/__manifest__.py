# -*- coding: utf-8 -*-
{
    "name": "Al Rajhi Bank (ARB) Payment Gateway",
    "version": "19.0.1.4.12",
    "category": "Accounting/Payment Providers",
    "summary": "Official-style ARB integration: token API, encrypted trandata, bank-hosted redirect, KSA Card/Mada checkout (Odoo 19).",
    "description": """
Al Rajhi Bank (ARB) payment acquirer for Odoo
=============================================

Connect Odoo to Al Rajhi Bank's payment gateway with token generation, AES-encrypted ``trandata``, and bank-hosted redirect flows suitable for Saudi merchants (SAR, Card/Mada).

**Suggested retail price:** USD 80 (set final price in your Odoo Apps publisher account).

See ``static/description/index.html`` for full marketing copy, screenshots, and configuration guidance.

**Author:** Sirelkhatim Gamal — https://sirelkhatim.odoo.com
    """,
    "author": "Sirelkhatim Gamal",
    "website": "https://sirelkhatim.odoo.com",
    "license": "LGPL-3",
    "images": ["static/description/cover.png"],
    "price": 98.0,
    "currency": "USD",
    "depends": ["payment"],
    "external_dependencies": {
        "python": ["requests", "pycryptodome"],
    },
    "data": [
        "views/arb_redirect_form_templates.xml",
        "views/payment_provider_views.xml",
        "data/payment_provider_data.xml",
    ],
    "installable": True,
    "application": False,
}
