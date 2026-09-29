{
    "name": "Product Traceability Dashboard",
    "version": "18.0.2.0.0",
    "summary": "Product traceability dashboard with returns, scrap and manufacturing genealogy",
    "category": "Inventory/Inventory",
    "author": "Ibrahim Elmasry",
    "license": "LGPL-3",
    "depends": ["stock", "purchase", "sale_management", "mrp", "account"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/product_traceability_views.xml",
        "views/product_traceability_report_views.xml",
        "views/product_traceability_menus.xml",
        "report/traceability_report_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "el_product_traceability_dashboard/static/src/js/traceability_dashboard.js",
            "el_product_traceability_dashboard/static/src/xml/traceability_dashboard.xml",
            "el_product_traceability_dashboard/static/src/css/traceability_dashboard.css",
        ],
    },
    "installable": True,
    "application": True,
}
