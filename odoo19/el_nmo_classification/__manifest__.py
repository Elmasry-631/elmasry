{
    "name": "El-Nmo - Customer Classification",
    "version": "19.0.1.0.0",
    "author": "Ibrahim Elmasry",
    "category": "Sales/Sales",
    "summary": "Customer classification tiers (A-E) with auto-classification criteria.",
    "description": """
Customer Classification
=======================
Defines customer tiers (A through E) with configurable:
- Price list, credit limit, payment term, and credit policy per tier
- Auto-classification criteria based on sales, balance, and age metrics
- Daily cron to automatically re-classify customers
    """,
    "website": "https://www.woledge.com",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "sale",
        "account",
        "el_nmo_sale_payment_gateway",
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
