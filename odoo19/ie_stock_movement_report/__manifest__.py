{
    'name': 'Stock Movement Report',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Reporting',
    'summary': 'PDF report of inventory movements with opening/closing balance and running value.',
    'description': """
Stock Movement Report
=====================

Generates a PDF report showing inventory movements per product during a
selected period. Each product gets its own page with:

* Opening Balance (qty + value, computed from all movements before From Date)
* Detailed movement table (Date, Reference, Partner, Source, Destination,
  IN/OUT/BALANCE each split into Qty/Unit/Unit Price/Total)
* Running balance after every transaction
* Product summary (Opening Qty, Total In, Total Out, Closing Qty,
  Inventory Value)

Performance
-----------
Designed for thousands of movements:
* Batch-loads stock.move.line records with a single domain-filtered query
* Prefetches product costs and UoM via read()
* Computes balances in memory after retrieval (no ORM calls in loops)
* Uses product.standard_price (Community Edition) for valuation

Multi-language
--------------
* English (LTR) and Arabic (RTL) supported
* Automatic translation via Odoo i18n
* RTL layout switches based on user language

Paper: A4 Landscape, one product per page, header/footer on every page.
    """,
    'author': 'Ibrahim Elmasry',
    'website': 'https://github.com/Elmasry-631',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'stock',
        'stock_account',
        'web',
    ],
    'data': [
        # LAW 16: order = security → data → wizards → reports → views → menus
        'security/ir.module.privilege.xml',
        'security/ir.model.access.csv',
        'wizard/stock_movement_report_wizard_views.xml',
        'reports/stock_movement_report_template.xml',
        'views/stock_movement_report_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
