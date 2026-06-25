# -*- coding: utf-8 -*-
{
    "name": "Direct Print Auto",
    "version": "19.0.1.0.0",
    "summary": "Auto-print invoices, SOs, delivery slips and POs to the browser's print dialog when confirmed, plus a manual Direct Print button on each form.",
    "description": """
Direct Print Auto
=================

Auto-print reports to the browser's print dialog (window.print via hidden iframe)
when a document is confirmed, plus an explicit "Direct Print" button on each
supported form view. Works on:

- Sales invoices (account.move, customer invoices/refunds only) — fires on action_post()
- Sales orders (sale.order) — fires on action_confirm()
- Delivery pickings (stock.picking, outgoing only) — fires on button_validate()
- Purchase orders (purchase.order) — fires on button_approve()

The browser's native print dialog is opened instead of generating a PDF for
download. Each document type has an independent toggle in Settings → Sales.
A manual "Direct Print" button is always available on the form header for
on-demand printing regardless of the auto-print setting.

Author: Ibrahim Elmasry
    """,
    "author": "Ibrahim Elmasry",
    "website": "https://www.odoo.com",
    "category": "Sales/Sales",
    "license": "LGPL-3",
    "depends": [
        "base",
        "web",
        "sale_management",
        "account",
        "stock",
        "purchase",
    ],
    "data": [
        "security/direct_print_groups.xml",
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/account_move_views.xml",
        "views/stock_picking_views.xml",
        "views/purchase_order_views.xml",
        "views/client_actions.xml",
        "views/direct_print_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "direct_print_auto/static/src/js/direct_print_action.js",
            "direct_print_auto/static/src/xml/direct_print_templates.xml",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
