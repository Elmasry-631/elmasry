# -*- coding: utf-8 -*-
from odoo import http

# class TradepaintsSaleorderReport(http.Controller):
#     @http.route('/tradepaints_saleorder_report/tradepaints_saleorder_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tradepaints_saleorder_report/tradepaints_saleorder_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tradepaints_saleorder_report.listing', {
#             'root': '/tradepaints_saleorder_report/tradepaints_saleorder_report',
#             'objects': http.request.env['tradepaints_saleorder_report.tradepaints_saleorder_report'].search([]),
#         })

#     @http.route('/tradepaints_saleorder_report/tradepaints_saleorder_report/objects/<model("tradepaints_saleorder_report.tradepaints_saleorder_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tradepaints_saleorder_report.object', {
#             'object': obj
#         })