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
        # if stock_picking_obj:
        #     total_weight = sum(stock_picking_obj.mapped('total_weight'))
        #     exist_weight = self.expected_weight
        #     if not exist_weight:
        #         exist_weight = 0
        #     if total_weight > exist_weight:
        #         raise ValidationError('You are not allow to make this operation,'
        #                               'Total weight (%s) greater than Expected weight (%s) '
        #                               % (total_weight, exist_weight))
        #     elif total_weight < exist_weight:
        #         raise ValidationError('You are not allow to make this operation,'
        #                               'Total weight (%s) less than Expected weight (%s) '
        #                               % (total_weight, exist_weight))
        #     else:
        #         print('stock_picking_obj', stock_picking_obj)
        #         for stock_picking in stock_picking_obj:
        #             for pro in stock_picking.move_ids_without_package:
        #                 pro.quantity_done = pro.product_uom_qty
        #             stock_picking.button_validate()

        for stock_picking in stock_picking_obj:
            stock_picking.driver_name = self.driver_name
            stock_picking.car_number = self.car_number
            stock_picking.printed_before = True
        return self.env.ref('trad_paints_delivery_report.trad_paints_delivery_report_action_report_all_picking').report_action(docids=stock_picking_ids,config=False)
