{
    'name': 'Construction Tendering',
    'version': '19.0.1.0.0',
    'summary': 'Client Tenders (Bid Costing & Submission) + Subcontractor/Vendor RFQ & Bid Comparison',
    'description': """
Construction Tendering
=======================
Adds pre-award tendering to Construction Management:

1. Tender Opportunities: track tenders you bid for from clients, build up the
   price per BOQ item (direct cost + overhead % + profit %), submit, and on
   Win automatically generate a Project / Sub Project / BOQ in
   el_construction_management.

2. Subcontractor / Vendor RFQs: invite multiple subcontractors or suppliers
   to bid on a scope of work, capture each vendor's priced lines, compare
   bids per line, and award. An RFQ linked to a live Project generates a
   Subcontract on award. An RFQ linked to a Tender Opportunity feeds its
   awarded prices back into the client bid's cost buildup.

Developed by Ibrahim Elmasry — Senior Odoo Developer & Implementation Consultant.
    """,
    'category': 'Construction',
    'author': 'Ibrahim Elmasry',
    'website': 'https://github.com/Elmasry-631',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'contacts',
        'el_construction_management',
    ],
    'data': [
        'security/construction_tender_security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/tender_opportunity_views.xml',
        'views/tender_rfq_views.xml',
        'wizard/tender_compare_wizard_views.xml',
        'views/menu_views.xml',
        'reports/tender_reports.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'el_construction_tender/static/src/js/tender_dashboard_patch.js',
            'el_construction_tender/static/src/xml/tender_dashboard_patch.xml',
            'el_construction_tender/static/src/css/tender_dashboard.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
