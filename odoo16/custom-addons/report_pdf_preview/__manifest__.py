# -*- encoding: utf-8 -*-

{
    "name": "Report Pdf Preview",
    "version": "16.0.1.0.3",
    "summary": "Preview reports in PDF format within the browser.",
    "author": "山西清水欧度信息技术有限公司",
    "website": "http://www.odooqs.com",
    "category": "Productivity",
    "license": "AGPL-3",
    "depends": ["web"],
    "images": [
        'static/description/icon.jpg',
        'static/description/main_screenshot.png'
    ],
    "assets": {
        "web.assets_backend": [
            "report_pdf_preview/static/src/scss/preview_dialog.scss",
            "report_pdf_preview/static/src/scss/preview_content.scss",
            "report_pdf_preview/static/src/js/preview_handler.js",
            "report_pdf_preview/static/src/js/preview_generator.js",
            "report_pdf_preview/static/src/js/preview_dialog.js",
            "report_pdf_preview/static/src/js/web_pdf_preview.js",
            "report_pdf_preview/static/lib/printThis/printThis.js"
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
