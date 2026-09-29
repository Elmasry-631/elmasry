{
    'name': 'E-Book Store',
    'version': '19.0.1.0.0',
    'category': 'Website/eCommerce',
    'summary': "Sell e-books with unique access codes — online reader + download",
    'description': """
E-Book Store
=============
- Sell e-books on your Odoo eCommerce website
- Generate unique access codes (random or manual)
- Each code is used once per customer
- Online PDF reader (portal)
- Download option per book
- My Library page for customers
- Admin dashboard with sales stats
""",
    'author': 'Ibrahim Elmasry',
    'license': 'LGPL-3',
    'depends': ['base', 'sale', 'sale_management', 'website_sale', 'payment', 'portal', 'mail'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'data/email_templates.xml',
        'wizard/generate_codes_wizard_views.xml',
        'views/ebook_code_views.xml',
        'views/product_template_views.xml',
        'views/ebook_library_views.xml',
        'views/ebook_dashboard_views.xml',
        'views/portal_ebook_views.xml',
        'views/ebook_menus.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'el_ebook_store/static/src/css/ebook_portal.css',
        ],
    },
    'tests': ['tests/test_ebook_store.py'],
    'installable': True,
    'application': True,
    'auto_install': False,
    '_constitution_waivers': [
        {'law': 26, 'reason': 'Build sandbox lacks libldap2-dev/libsasl2-dev; Odoo CLI cannot start. Static validators PASS. User must run L1/L2/L3 on real Odoo 19.'},
    ],
    '_constitution_version': '10.30.8',
}
