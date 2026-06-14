{
    "name": "Partner Request",
    "version": "19.0.1.0.0",
    "category": "Sales/Sales",
    "summary": "Approval workflow for creating new customers via sales requests.",
    "description": """
Partner Request Module for Odoo 19
===================================

Enables the sales team to submit customer creation requests
through an approval workflow before customers are added to the system.

Key Features:
- 5-state workflow: Draft -> Pending -> Approved / Rejected / Sent Back
- Auto-generated request numbers (PRQ-YYYY-NNNNN)
- Manager approval with reject and send-back capabilities
- Activities and notifications between salesperson and manager
- Direct partner creation restriction for sales users
- Duplicate email detection before partner creation
- Smart button to open created customer
- Chatter and attachments on every request
    """,
    "author": "Ibrahim Elmasry",
    "website": "https://www.odoo.com",
    "license": "LGPL-3",
    "depends": [
        "sale",
        "sales_team",
        "customer_classification",
    ],
    "data": [
        "security/partner_request_security.xml",
        "security/ir.model.access.csv",
        "data/partner_request_data.xml",
        "views/partner_request_views.xml",
        "views/partner_request_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}