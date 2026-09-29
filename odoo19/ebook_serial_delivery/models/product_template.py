# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplate(models.Model):
    """Only adds a flag. Availability, quantities and 'out of stock'
    all stay on the standard stock.quant / qty_available computation —
    nothing to compute or sync manually here.
    """
    _inherit = 'product.template'

    is_ebook_with_codes = fields.Boolean(
        string="eBook Delivered by Serial Number",
        help="If checked, each unit sold consumes one available Serial "
             "Number from Inventory. The order's delivery is validated "
             "automatically and the assigned serial is emailed to the "
             "customer as soon as it is confirmed."
    )

    @api.onchange('is_ebook_with_codes')
    def _onchange_is_ebook_with_codes(self):
        # Odoo 19 dropped detailed_type/type='product' for storable
        # products in favor of a dedicated boolean: is_storable.
        if self.is_ebook_with_codes:
            self.is_storable = True    # storable
            self.tracking = 'serial'   # each unit = one license
            # A serial IS the product: never let the website accept an
            # order for a unit that has no serial backing it. Without
            # this, "Add to Cart" stays available even at qty=0 and the
            # customer only finds out there's no license left *after*
            # paying (caught by the UserError in sale_order.py).
            if 'allow_out_of_stock_order' in self._fields:
                self.allow_out_of_stock_order = False
        elif self.tracking == 'serial':
            self.tracking = 'none'
