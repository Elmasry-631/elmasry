# -*- coding: utf-8 -*-
{
    'name': 'eBook Serial Delivery',
    'version': '19.0.1.1.0',
    'category': 'Website/eCommerce',
    'summary': 'Deliver eBook licenses using standard Inventory Serial Numbers '
               '(stock.lot) — no custom "activation code" model.',
    'description': """
eBook Serial Delivery (Odoo 19)
================================
Design goal: reuse the standard Inventory stack instead of inventing a
parallel data model.

- eBook products are storable products tracked by Serial Number
  (`tracking = 'serial'`), exactly like Odoo already supports.
- Stock team enters available licenses the normal way:
  Inventory > Products > Update Quantity > Serial Numbers.
- On sale order confirmation, the linked delivery is reserved
  (Odoo's own removal strategy picks the serial — no manual querying)
  and validated automatically, since eBooks don't need a warehouse
  worker to physically pack anything.
- Once the delivery is done, a PDF with the assigned serial(s) is
  emailed to the customer automatically.
- "Out of stock" is the standard `qty_available` = 0 behaviour already
  handled by website_sale — nothing custom to build there.

No new business model is introduced. `stock.lot`, `stock.move`,
`stock.picking` and `sale.order` remain the single source of truth.
""",
    'author': 'Custom Development',
    'license': 'LGPL-3',
    'depends': ['website_sale', 'sale_stock', 'mail'],
    'data': [
        # report must load BEFORE mail_template_data.xml, which ref()'s
        # action_report_ebook_serial from it
        'report/ebook_serial_report_templates.xml',
        'data/mail_template_data.xml',
        'views/product_template_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'post_init_hook': '_assign_default_ebook_serial_mail_template',
    'installable': True,
    'application': False,
    'auto_install': False,
}
