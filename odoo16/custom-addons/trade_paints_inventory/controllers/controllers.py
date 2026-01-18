# -*- coding: utf-8 -*-
from odoo import http

# class TradePaintsFeatures(http.Controller):
#     @http.route('/trade_paints_features/trade_paints_features/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trade_paints_features/trade_paints_features/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('trade_paints_features.listing', {
#             'root': '/trade_paints_features/trade_paints_features',
#             'objects': http.request.env['trade_paints_features.trade_paints_features'].search([]),
#         })

#     @http.route('/trade_paints_features/trade_paints_features/objects/<model("trade_paints_features.trade_paints_features"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trade_paints_features.object', {
#             'object': obj
#         })