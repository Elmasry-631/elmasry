{
    "name": "Open PDF Reports and PDF Attachments in Browser",
    "version": "18.0.1.0.0",
    "summary": """
    Preview reports and pdf attachments in browser instead of downloading them.
    Open Report or PDF Attachment in new tab instead of downloading.
""",
    "category": "Productivity",
    "license": "LGPL-3",
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    "depends": ["web"],
    "images": ["static/description/banner.png"],
    "assets": {
        "web.assets_backend": [
            "prt_report_attachment_preview/static/src/js/tools.esm.js",
            "prt_report_attachment_preview/static/src/js/report.esm.js",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
