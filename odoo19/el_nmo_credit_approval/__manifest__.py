{
    "name": "El-Nmo - Credit Limit Approval Workflow",
    "version": "19.0.1.0.0",
    "author": "Ibrahim Elmasry",
    "category": "Sales/Sales",
    "summary": "Approval workflow for sale orders exceeding customer credit limits.",
    "description": """
Credit Limit Approval Workflow
================================
When a salesperson confirms a sale order for a credit customer whose
credit policy is 'Block Sale' and whose credit limit is exceeded,
instead of raising a hard error, the system creates an approval request
to the sales supervisor.

Features:
- Automatic credit check on sale order confirmation
- Approval request creation with full credit details
- Supervisor approve/reject workflow
- Predefined rejection reasons (configurable model)
- Chatter integration for audit trail
- Smart alert banner on blocked sale orders
    """,
    "website": "https://www.woledge.com",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        "sale",
        "el_nmo_classification",
    ],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "data/default_rejection_reasons.xml",
        "views/credit_rejection_reason_views.xml",
        "views/credit_approval_request_views.xml",
        "wizard/credit_approval_wizard_views.xml",
        "views/sale_order_views.xml",
        "views/menu.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
