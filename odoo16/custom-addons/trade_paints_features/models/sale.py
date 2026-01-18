# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo import exceptions, _
from odoo.exceptions import ValidationError
from lxml import etree

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    product_ids = fields.Many2many('product.product', compute='get_product_ids')

    @api.depends('partner_id')
    def get_product_ids(self):
        for order in self:
            products = self.env['product.product'].search([])
            selected_products = []
            for pro in products:
                seller_ids = list(set((map(lambda x: x.partner_id, pro.seller_ids))))  # Adjusted this line
                if order.partner_id in seller_ids:  # Adjusted this line
                    selected_products.append(pro.id)
            lst = [(4, val) for val in selected_products]
            order.product_ids = lst



class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_id = fields.Many2one('product.product', domain="[('id', 'in', parent.product_ids)]")
    
    @api.onchange('product_id')
    def product_id_on_change(self):
      domain = ([('seller_ids.partner_id.id', '=', self.partner_id.id)])
      return {'domain': {'product_id': domain}}
 

class ProductProduct(models.Model):
    _inherit = 'product.product'

    vendor_ids = fields.Many2many('res.partner', compute='get_vendor_ids')

    @api.depends('seller_ids')
    def get_vendor_ids(self):
        if self.seller_ids:
            vals = list(set((map(lambda x: x.name, self.seller_ids))))
            lst = []
            for val in vals:
                lst.append((4, val.id))
            self.vendor_ids = lst


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    vendor_ids = fields.Many2many('res.partner', compute='get_vendor_ids')
    categ_id = fields.Many2one(
        'product.category', 'Product Category',
        change_default=True, default='',
        required=True, help="Select category for the current product")

    current_qty_value = fields.Float(string='قيمة المخزون',compute="_calc_current_qty",store=True )

    @api.onchange('qty_available','standard_price')
    def _calc_current_qty(self):
        for rec in self:
            rec.current_qty_value=rec.standard_price*rec.qty_available

    def change_price(self):
        prods = self.env['product.template'].search([])
        for pro in prods:
            for seller in pro.seller_ids:
                seller.price = pro.standard_price

    @api.depends('seller_ids')
    def get_vendor_ids(self):
        if self.seller_ids:
            vals = list(set((map(lambda x: x.name, self.seller_ids))))
            lst = []
            for val in vals:
                lst.append((4, val.id))
            self.vendor_ids = lst

    @api.model
    def create(self, vals):
        if not self.env.user.has_group('trade_paints_features.allow_create_without_vendor'):
            if not vals.get('seller_ids'):
                raise ValidationError('Please Select at least one vendor')
        return super(ProductTemplate, self).create(vals)
    #
    # @api.constrains('seller_ids')
    # def check_exist_seller(self):
    #     if not self.seller_ids:
    #         raise ValidationError('Please select at least one vendor')


class ResPartnerNeighborhood(models.Model):
    _name = 'res.partner.neighborhood'

    name = fields.Char()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    neighborhood_id = fields.Many2one('res.partner.neighborhood', string='الحي')

    def get_products_for_vendor(self):
        vendor_id = self.env.context.get('partner_id')
        product_ids = list(set(list(map(lambda x: x.product_tmpl_id.id, self.env['product.supplierinfo'].search([('name', '=', vendor_id)])))))
        return {
            'name': _('Products'),
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', product_ids)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'product.template',
            # 'views': [(tree_id, 'tree'), (form_id, 'form')],
            # 'target': 'current',
            # 'context': ctx,
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_available = fields.Float(related='product_id.qty_available')
    virtual_available = fields.Float(related='product_id.virtual_available')
    product_weight = fields.Float(compute='get_total_weight', store=True)

    stored_qty_trade = fields.Char(string='المخزون', compute='compute_stored_qty')
    product_uom_qty = fields.Float(default=0)
    
    @api.constrains('product_uom_qty', 'qty_available')
    def check_product_qty_against_availability(self):
        for record in self:
            if record.qty_available == 0 and record.product_uom_qty > 0:
                raise ValidationError(f"The product {record.product_id.name} is out of stock. You cannot set any quantity.")

            if record.product_uom_qty > record.qty_available:
                raise ValidationError(f"The requested quantity for {record.product_id.name} exceeds the available quantity. Available quantity is {record.qty_available}.")

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            if line.discount:
                discount_before_price_list = line.product_id.lst_price * (line.discount / 100.0)
                price=line.price_unit-discount_before_price_list
                print(">",discount_before_price_list,line.price_unit-discount_before_price_list,(1 - (line.discount or 0.0) / 100.0))
            else:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


    @api.depends('product_uom_qty', 'virtual_available')
    def compute_stored_qty(self):
        if self.state == "draft":
            self.stored_qty_trade = self.virtual_available - self.product_uom_qty
        elif self.state == "sale":
            self.stored_qty_trade = self.virtual_available
        else:
            pass

           
    @api.constrains('product_uom_qty')
    def check_product_qty(self):
        for record in self:
            if record.product_uom_qty % 1 != 0:
                raise ValidationError('Please set an integer value, not a float')



    @api.depends('product_id', 'product_uom_qty')
    def get_total_weight(self):
        for rec in self:
            if rec.product_id and rec.product_uom_qty:
                rec.product_weight = rec.product_id.weight * rec.product_uom_qty


    @api.onchange('discount', 'product_id')
    def on_change_discount(self):
        if self.product_id and self.product_id.categ_id:
            if self.discount > self.product_id.categ_id.limit_discount and self.product_id.categ_id.limit_discount:
                raise ValidationError('You exceed Discount limit  for this product')

            if self.discount > self.env.user.limit_discount and self.env.user.limit_discount:
                raise ValidationError('You exceed Discount limit For Current User!')

    _sql_constraints = [('order_product_uniq', 'unique (id,order_id,product_id)',
                 'Duplicate products in order line not allowed !')]

    @api.constrains('product_uom_qty')
    def check_product_uom_qty_2(self):
        for line in self:
            if line.product_uom_qty==0:
                raise ValidationError("Not Allowed Set Quantity Zero!")
                



    # @api.constrains('product_id', 'price_unit')
    # def check_price(self):
    #     amount = 0.0
    #     for line in self:
    #         res = self.env['product.pricelist.item'].search([
    #             ('pricelist_id', '=', line.order_id.pricelist_id.id)])
    #         print('555555555555555555', res)
    #         for pricelisit in res:
    #             print('????????????', pricelisit.price)
    #             if pricelisit.applied_on == '2_product_category':
    #                 if line.product_id.categ_id.id == pricelisit.categ_id.id:
    #                     if pricelisit.compute_price == 'percentage':
    #                         amount = line.product_id.list_price
    #                         if line.price_unit < amount-(pricelisit.percent_price/100):
    #                             raise ValidationError('Product price should not be less than price in price list')
    #                         elif pricelisit.compute_price == 'fixed':
    #                             if line.price_unit < pricelisit.fixed_price:
    #                                 raise ValidationError('Product price should not be less than price in price list')
    #             elif pricelisit.applied_on == '1_product':
    #                 if line.product_id.id == pricelisit.product_tmpl_id.id:
    #                     print('....................')
    #                     if pricelisit.compute_price == 'percentage':
    #                         amount = line.product_id.list_price
    #                         if line.price_unit < amount-(pricelisit.percent_price/100):
    #                             raise ValidationError('Product price should not be less than price in price list')
    #                         elif pricelisit.compute_price == 'fixed':
    #                             print('>>>>>>>>>>>>>>>>>>>>>')
    #                             if line.price_unit < pricelisit.fixed_price:
    #                                 raise ValidationError('Product price should not be less than price in price list')


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    weigh_total = fields.Float(compute='get_total_weight')
    discount_tot_for_lines = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_discount_for_lines')



    @api.onchange('price_list_id2')
    def price_list_change(self):
        if self.price_list_id2:
            self.pricelist_id=self.price_list_id2.id


    @api.depends('order_line.product_weight')
    def get_total_weight(self):
        for sale in self:
            total = 0
            for rec in sale.order_line:
                total += rec.product_weight
            sale.weigh_total = total

    # @api.constrains('order_line')
    # def check_lines(self):
    #     for order in self:
    #         for line in order.order_line:
    #             if line.product_id.type == 'product':
    #                 if line.product_uom_qty > line.product_id.qty_available:
    #                     # raise ValidationError('error')
    #                     product = line.product_id.with_context(
    #                         warehouse=line.order_id.warehouse_id.id,
    #                         lang=line.order_id.partner_id.lang or self.env.user.lang or 'en_US'
    #                     )
    #                     message = _('You plan to sell %s %s of %s but you only have %s %s available in %s warehouse.') % \
    #                               (line.product_uom_qty, line.product_uom.name, line.product_id.name,
    #                                product.virtual_available, product.uom_id.name, line.order_id.warehouse_id.name)
    #                     raise ValidationError(message)
                    # elif line.product_uom_qty <= 0:
                    #         raise ValidationError('please check qty in lines')
                        # for rec in self:
                        #     if rec.order_line:
                        #         for line in rec.order_line:
                        #             if int( or int(line.stored_qty_trade) <= 0:
                        #                 raise Warning("please review lines , qty or stock is zero")

    @api.depends('order_line.price_total')
    def _amount_discount_for_lines(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_total_bef_discount = amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_total_bef_discount += line.price_subtotal + line.price_unit * ((line.discount or 0.0) / 100.0)\
                                             * line.product_uom_qty
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            
            order.update({
                'discount_tot_for_lines': amount_total_bef_discount - amount_untaxed
            })
