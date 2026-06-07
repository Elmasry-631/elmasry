# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TransferWizard(models.TransientModel):
    _name = 'transfer.wizard'
    _description = 'Transfer Wizard'

    # ===============================
    # Compute default expected weight
    # ===============================
    @api.model
    def _default_expected_weight(self):
        total = 0.0
        picking_ids = self.env.context.get('active_ids') or []
        pickings = self.env['stock.picking'].browse(picking_ids)

        for picking in pickings:
            total += picking.weight or 0.0   # Odoo 18 standard field

        return total


    expected_weight = fields.Float(
        string='Expected Weight (KG)',
        default=lambda self: self._default_expected_weight()
    )

    driver_name = fields.Many2one('res.partner', string='Driver Name')
    car_number = fields.Char(string='Car Number')

    # ===============================
    # Validate
    # ===============================
    def validate(self):
        picking_ids = self.env.context.get('active_ids') or []
        pickings = self.env['stock.picking'].browse(picking_ids)

        for picking in pickings:
            picking.write({
                'driver_name': self.driver_name.id,
                'car_number': self.car_number,
                'printed_before': True,
            })

        return self.env.ref(
            'trad_paints_delivery_report.trad_paints_delivery_report_action_report_all_picking'
        ).report_action(pickings)





class StockPicking(models.Model):
    _inherit = "stock.picking"

    driver_name = fields.Many2one(
        'res.partner',
        string="Driver"
    )

    car_number = fields.Char(
        string="Car Number"
    )

    printed_before = fields.Boolean(
        string="Printed Before",
        default=False
    )