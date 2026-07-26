{
    "name": "PDF Print Preview",
    "version": "19.0.1.1.0",
    "category": "Extra Tools/Usability",
    "summary": "Preview PDF reports in-browser before printing — no download needed",
    "description": """
PDF Print Preview (Odoo 19)
============================

Intercepts report actions and opens a PDF.js viewer dialog in the browser.
Users can preview the PDF, then print or download — all without leaving Odoo.

Features:
  - In-browser PDF preview via PDF.js viewer
  - Per-user toggle: preview on/off
  - Per-user toggle: automatic printing (opens print dialog)
  - Error catcher: if report fails, shows friendly error PDF
  - User menu entry for quick settings access

How it works:
  1. Registers a handler in 'ir.actions.report handlers' registry
  2. When a qweb-pdf report is triggered, fetches the PDF
  3. Opens it in a PDF.js viewer inside an OWL Dialog
  4. User can preview, print, or download from the viewer

No IoT box required — uses standard browser + PDF.js.
""",
    "author": "Ibrahim Elmasry",
    "maintainer": "Ibrahim Elmasry",
    "website": "https://github.com/Elmasry-631",
    "license": "LGPL-3",
    "depends": [
        "base",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_users_views.xml",
        "report/ir_actions_report_templates.xml",
        "report/ir_actions_report.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "el_pdf_print_preview/static/src/scss/dialog.scss",
            "el_pdf_print_preview/static/src/js/pdf_preview_handler.js",
            "el_pdf_print_preview/static/src/js/pdf_preview_dialog.js",
            "el_pdf_print_preview/static/src/js/user_menu.js",
            "el_pdf_print_preview/static/src/xml/pdf_preview_dialog.xml",
        ],
    },
    "images": ["static/description/icon.png"],
    "installable": True,
    "auto_install": False,
    "application": False,
    "_constitution_version": "1.2.0",
}
