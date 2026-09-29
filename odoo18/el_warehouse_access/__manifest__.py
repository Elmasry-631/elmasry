# -*- coding: utf-8 -*-
{
    'name': 'Warehouse-Based Access Control',
    'version': '18.0.1.0.0',
    'summary': 'Control user access based on warehouse assignments - Global backend security enforcement',
    'description': """
Warehouse-Based Access Control Module
=====================================

This module implements **global backend security** that restricts user access
to stock operations, locations, and reports based on warehouses assigned to
each user.

**Core Features:**
- User-to-Warehouse assignment (single or multiple warehouses)
- Automatic data filtering across ALL stock models
- Record Rules (ir.rule) enforced at database level
- Domain restrictions on relational fields
- Administrator full access bypass
- Support for users with no warehouse assignment

**Security Models Covered:**
- stock.picking (Transfers/Shipments)
- stock.move (Stock Moves)
- stock.move.line (Move Lines)
- stock.quant (Inventory Quantities)
- stock.location (Locations)
- stock.warehouse (Warehouses)
- stock.picking.type (Operation Types)
- stock.scrap (Scraps)

**Important:** This is NOT UI-only filtering. Security rules are enforced
at the ORM/database level, preventing direct URL manipulation or API access
from bypassing restrictions.

Author: Ibrahim Elmasry
License: LGPL-3
    """,
    'author': 'Ibrahim Elmasry',
    'website': 'https://github.com/ibrahimelmasry',
    'category': 'Inventory',
    'depends': ['base', 'stock', 'sale_stock'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',
        'views/res_users_views.xml',
        'views/stock_picking_views.xml',
                'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'data_files': [],
}
