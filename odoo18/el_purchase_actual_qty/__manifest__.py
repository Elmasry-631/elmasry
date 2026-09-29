{
    "name": "Purchase Actual Quantity",
    "version": "18.0.2.0.0",
    "summary": "Actual purchase quantity with preserved value, dashboard and reporting",
    "category": "Purchases",
    "author": "Ibrahim Elmasry",
    "license": "LGPL-3",
    "depends": ["purchase", "purchase_stock", "stock_account"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_actions.xml",
        "reports/purchase_actual_report.xml",
        "views/purchase_order_views.xml",
        "views/purchase_actual_report_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "el_purchase_actual_qty/static/src/js/purchase_actual_dashboard.js",
            "el_purchase_actual_qty/static/src/xml/purchase_actual_dashboard.xml",
            "el_purchase_actual_qty/static/src/css/purchase_actual_dashboard.css",
        ],
    },
    "installable": True,
    "application": True,
}
