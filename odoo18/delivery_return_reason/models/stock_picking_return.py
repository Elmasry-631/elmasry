# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    x_return_reason_id = fields.Many2one(
        'delivery.return.reason',
        string='سبب الرجوع',
        required=True,
        domain="[('company_id', '=', company_id)]",
    )
    x_return_note = fields.Text(string='ملاحظات الرجوع')

    def _prepare_picking_default_values(self):
        if not self.x_return_reason_id:
            raise UserError(_('A return reason is required.'))
        vals = super()._prepare_picking_default_values()
        vals.update({
            'x_returned': True,
            'x_return_reason_id': self.x_return_reason_id.id,
            'x_return_note': self.x_return_note,
        })
        return vals
