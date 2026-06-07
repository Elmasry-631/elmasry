# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    # نستخدم product.template ليظهر الحقل في واجهة المنتج العامة
    _inherit = 'product.template'

    qty_restrict = fields.Float(string="الحد الأقصى للكمية", tracking=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('product_uom_qty', 'product_id')
    def _check_product_qty_restriction(self):
        for line in self:
            # نصل للحقل من الـ template المرتبط بالمنتج
            max_allowed = line.product_id.qty_restrict

            if max_allowed > 0 and line.product_uom_qty > max_allowed:
                raise ValidationError(_(
                    "خطأ: المنتج (%s) لديه حد أقصى للكمية مسموح به هو %s. القيمة المدخلة (%s) غير مقبولة."
                ) % (line.product_id.name, max_allowed, line.product_uom_qty))