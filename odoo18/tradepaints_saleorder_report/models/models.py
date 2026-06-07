# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class tradepaints_saleorder_report(models.Model):
#     _name = 'tradepaints_saleorder_report.tradepaints_saleorder_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100