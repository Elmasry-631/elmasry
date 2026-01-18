# -*- coding: utf-8 -*-
from odoo import http

# class AccessRightProductPartner(http.Controller):
#     @http.route('/access_right_product_partner/access_right_product_partner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/access_right_product_partner/access_right_product_partner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('access_right_product_partner.listing', {
#             'root': '/access_right_product_partner/access_right_product_partner',
#             'objects': http.request.env['access_right_product_partner.access_right_product_partner'].search([]),
#         })

#     @http.route('/access_right_product_partner/access_right_product_partner/objects/<model("access_right_product_partner.access_right_product_partner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('access_right_product_partner.object', {
#             'object': obj
#         })