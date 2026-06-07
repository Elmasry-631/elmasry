# -*- coding: utf-8 -*-
{
    'name': 'POS Daily Sequence',
    'version': '19.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Automatically reset POS order numbering every day',
    'description': """
POS Daily Order Number Reset
============================

This module adds a daily POS order number per Point of Sale configuration.
Each enabled configuration gets its own date-range sequence, so numbering
can restart from 1 every day.

Features
--------

* Daily reset of POS order numbers per POS config.
* Configurable sequence prefix with date placeholders.
* Independent counters for multiple POS configurations.
* Daily order number visible on POS orders in the backend.
""",
    'author': 'Ibrahim Elmasry',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
        'mail',
        'stock',
        'account',
    ],
    'data': [
        'data/ir_sequence_data.xml',
        'views/pos_config_views.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_daily_sequence/static/src/app/**/*',
        ],
    },
    'external_dependencies': {},
    'installable': True,
    'application': False,
    'auto_install': False,
}
