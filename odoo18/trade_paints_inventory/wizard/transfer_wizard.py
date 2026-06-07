# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class transfer_wizard(models.TransientModel):
    _name = 'transfer.wizard'

    def get_total_weight(self):
        total_sum=[]
        stock_picking_ids = self.env.context.get('active_ids', False)
        stock_picking_obj = self.env['stock.picking'].browse(stock_picking_ids)
        print(stock_picking_obj)
        for record in stock_picking_obj:
            total_sum.append(record.total_weight)
        return float(sum(total_sum))



    expected_weight = fields.Float('Expected weight KG', default=get_total_weight)
    driver_name = fields.Many2one('res.partner', string='Driver name', readonly=False)
    car_number = fields.Char(string='Car number', readonly=False)

    def validate(self):
        stock_picking_ids = self.env.context.get('active_ids', False)
        stock_picking_obj = self.env['stock.picking'].browse(stock_picking_ids)

        for stock_picking in stock_picking_obj:
            stock_picking.driver_name = self.driver_name
            stock_picking.car_number = self.car_number
            stock_picking.printed_before = True
        return self.env.ref('trad_paints_delivery_report.trad_paints_delivery_report_action_report_all_picking').report_action(docids=stock_picking_ids,config=False)
