{
"name" : "Test App Odoo",
"version" : "1.0",
"summary" : "A test application for Odoo",
"description" : "This is a test application to demonstrate Odoo module structure.",
"category" : "Tools",
"author" : "Ibrahim Elmasry",
"website" : "https://www.woledge.com",
"license" : "LGPL-3",
"depends" : ["base", "sale", "mail"],
"data" : [
    "views/menu_view.xml",
    "views/test_app_odoo_views.xml",
    "views/tag_view.xml",
    "views/sale_order_view.xml",
    "views/test_history_view.xml",
    "wizard/change_state_wizard_view.xml",
    "report/test_app_report.xml",

    "data/ir.sequence.xml"
],
'assets': {
    'web.assets_backend': [
        'test_app_odoo/static/src/css/test_file.css',
        ],
},
"installable" : True,
"application" : True,
"auto_install" : False,

}
