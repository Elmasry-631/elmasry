# -*- encoding: utf-8 -*-

{
    "name": "Pdf Print Preview",
    "version": "18.0.1.0.0",
    "depends": ["web"],
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    "summary": """Preview and print PDF report in your browser | Pdf direct preview | Print without Download""",
    "description": """
        Preview and print PDF report in your browser without downloading.
    """,

    "data": [
        "views/res_users.xml",
        "report/ir_actions_report_templates.xml",
        "report/ir_actions_report.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "pdf_print_preview/static/src/scss/dialog.scss",
            "pdf_print_preview/static/src/scss/content.scss",
            "pdf_print_preview/static/src/js/dialog.js",
            "pdf_print_preview/static/src/js/pdf_preview.js",
            "pdf_print_preview/static/src/js/user_menu.js",
            "pdf_print_preview/static/src/xml/dialog.xml",
            "pdf_print_preview/static/src/xml/user_menu.xml",
        ],
    },
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": True,
    "license": "OPL-1",
    "currency": "EUR",
    "price": 25.99
}
