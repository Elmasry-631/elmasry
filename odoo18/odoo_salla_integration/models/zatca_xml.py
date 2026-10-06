# -*- coding: utf-8 -*-
from odoo import models


class AccountEdiXmlUbl21Zatca(models.AbstractModel):
    _inherit = 'account.edi.xml.ubl_21.zatca'

    def _get_invoice_line_price_vals(self, line):
        """A credit note switched from a negative invoice (sale order adjustment, refund of a down
        payment) keeps a negative quantity and a negative price on its lines. ZATCA gets the quantity
        as a positive number, so the price must be positive too: quantity x price has to give the
        line amount, otherwise ZATCA refuses the document (BR-S-08, BR-O-08, BR-CO-17)."""
        vals = super()._get_invoice_line_price_vals(line)
        if line.quantity < 0 and vals.get('price_amount', 0) < 0:
            vals['price_amount'] = -vals['price_amount']
        return vals
