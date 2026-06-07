
{
    "name": "Account Fixed Discount",
    "summary": "Allows to apply fixed amount discounts in invoices.",
    "version": "18.0.1.0.0",
    "category": "Accounting & Finance",
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["account"],
    "excludes": ["account_invoice_triple_discount"],
    "data": [
        "security/res_groups.xml",
        "views/account_move_view.xml",
        "reports/report_account_invoice.xml",
    ],
}
