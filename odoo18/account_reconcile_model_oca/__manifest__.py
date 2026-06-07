{
    "name": "Account Reconcile Model Oca",
    "summary": """
        This includes the logic moved from Odoo Community to Odoo Enterprise""",
    "version": "18.0.1.1.1",
    "license": "LGPL-3",
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    "depends": ["account"],
    "excludes": ["account_accountant"],
    "data": [
        "views/account_reconcile_model_views.xml",
    ],
    "demo": [],
}
