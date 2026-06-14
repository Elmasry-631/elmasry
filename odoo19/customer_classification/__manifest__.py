{
    "name": "Customer Classification & Credit Control",
    "version": "19.0.1.0.0",
    "category": "Sales/Sales",
    "summary": "Classify customers into tiers (A-E) with inherited price lists, credit limits, and payment terms.",
    "description": """
Customer Classification Module for Odoo 19
============================================

Classify customers into tiers (A, B, C, D, E) where each tier defines:
- Default Price List (inherited by all customers in the tier)
- Default Credit Limit (with Block/Warning policy)
- Default Payment Term

Key Features:
- Automatic pricelist cascade: change it on the classification, all customers update
- Individual override per customer for pricelist, credit limit, and payment term
- Credit check on sale order confirmation (block or warning)
- Auto-classification via configurable criteria (cron-based, disabled by default)
- Multi-company support
- Role-based access (Manager: CRUD, User: Read-only)
    """,
    "author": "Ibrahim Elmasry",
    "website": "https://www.odoo.com",
    "license": "LGPL-3",
    "depends": [
        "sale",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/default_data.xml",
        "data/classification_cron.xml",
        "views/customer_classification_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}