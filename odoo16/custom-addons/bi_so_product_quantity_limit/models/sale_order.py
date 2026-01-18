# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
	_inherit = "sale.order"

	@api.model_create_multi
	def create(self, vals_list):
		res = super(SaleOrder, self).create(vals_list)
		for record in res:
			for rec in record.order_line:
				if rec.state == 'draft':
					if not rec.product_uom_qty >= rec.product_id.min_qty:
						raise ValidationError("Please Check Minimum and Maximum Quantity Limit of %s " % (rec.product_id.name))
					elif not rec.product_uom_qty <= rec.product_id.max_qty:
						raise ValidationError("Please Check Minimum and Maximum Quantity Limit of %s " % (rec.product_id.name))
		return res

	def write(self, vals_list):
		res = super(SaleOrder, self).write(vals_list)
		for order in self.order_line:
			for rec in order:
				if rec.state == 'draft':
					if not rec.product_uom_qty >= rec.product_id.min_qty:
						raise ValidationError("Please Check Minimum and Maximum Quantity Limit of %s " % (rec.product_id.name))
					elif not rec.product_uom_qty <= rec.product_id.max_qty:
						raise ValidationError("Please Check Minimum and Maximum Quantity Limit of %s " % (rec.product_id.name))
		return res

	def action_confirm(self):
		res = super(SaleOrder,self).action_confirm()
		for record in self:
			for rec in record.order_line:
				if not rec.product_uom_qty >= rec.product_id.min_qty:
					raise ValidationError("Please Check Minimum and Maximum Quantity Limit of %s " % (rec.product_id.name))
				elif not rec.product_uom_qty <= rec.product_id.max_qty:
					raise ValidationError("Please Check Minimum and Maximum Quantity Limit of %s " % (rec.product_id.name))
		return res