# -*- coding: utf-8 -*-
{
    'name': 'Balance Confirmation',
    'version': '19.0.3.6.0',
    'summary': 'Customer Balance Confirmation (Imdad / Namo templates)',
    'description': """
Customer Balance Confirmation (مطابقة رصيد العميل)
==================================================

Features
--------
- "Print Confirmation" button in the customer screen
- Template selection: Imdad or Namo
- Auto-fills: date, customer name, balance (as of confirmation date), employee name
- PDF output 100% identical to the Word template (same fonts, stamps, layout)
- Word (.docx) export with the same original template and filled fields
- Email the confirmation to the customer
- Bilingual: Arabic + English (UI follows the user's language)
- Only the balance value appears inside parentheses (per business requirement)
- Works on Odoo 19 with no external Python dependencies

Conversion pipeline (PDF)
-------------------------
  1. MS Word COM automation  — Windows + MS Word installed (BEST match)
  2. LibreOffice headless    — any OS (auto-detected)
  3. QWeb rendering          — last resort (no external tool needed)

Word template processing
------------------------
- Direct XML (lxml) manipulation of <w:t> nodes preserves all images,
  stamps, logos, and font formatting
- Red placeholder color (#EE0000) is changed to black after replacement
- Surrounding parentheses are stripped for non-balance fields
""",
    'author': 'Z.ai',
    'website': 'https://www.z.ai',
    'license': 'LGPL-3',
    'category': 'Accounting',
    'depends': [
        'base',
        'mail',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'wizard/balance_confirmation_wizard_views.xml',
        'reports/balance_confirmation_report.xml',
        'reports/balance_confirmation_templates.xml',
        'data/mail_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'icon': '/partner_balance_confirmation/static/icon.png',
}
