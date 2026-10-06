# -*- coding: utf-8 -*-
# Part of el_pos_customer_payment_method. See README.md for details.
# Odoo 19 port: smallest module that satisfies the requirement - 2 fields +
# 1 OWL patch + 2 views, no new model.
{
    'name': 'POS Customer Payment Method',
    'summary': 'Restrict POS payment methods per customer, with POS-level '
               'defaults for customers without a specific list.',
    'description': """
POS Customer Payment Method (Odoo 19)
=====================================
Cashiers see only the payment methods each customer is allowed to use.

- *Allowed POS Payment Methods* on the customer form
  (Sales and Purchase tab) - multiple methods allowed
- In the POS payment screen the buttons are filtered live:
  the list refreshes as soon as the order partner changes
- *Default Payment Methods* per POS (Settings > Point of Sale > Payment)
  are shown for customers without a specific list
- No customer selected or no defaults configured: all POS payment
  methods behave as usual

Technical notes
---------------
- res.partner gains el_allowed_pos_payment_method_ids and is exposed to the
  POS frontend through _load_pos_data_fields
- pos.config gains el_pos_default_payment_method_ids (loaded automatically
  with the other config fields)
- The PaymentScreen patch replaces the static payment_methods_from_config
  snapshot with a reactive getter
""",
    'version': '19.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'author': 'Ibrahim Elmasry',
    'website': 'https://github.com/Elmasry-631',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'el_pos_customer_payment_method/static/src/js/payment_screen.js',
        ],
    },
    'installable': True,
    'application': False,
}
