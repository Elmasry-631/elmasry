from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_weight = fields.Float('Total weight for products', compute='calc_total_weight_for_products')
    driver_name = fields.Many2one('res.partner', string='Driver name', readonly=False)
    car_number = fields.Char(string='Car number', readonly=False)
    neighborhood_id = fields.Many2one('res.partner.neighborhood', related='partner_id.neighborhood_id',
                                      store=True, string='الحي')

    printed_before = fields.Boolean(default=False)
    active = fields.Boolean(default=True)

    @api.depends('move_ids_without_package')
    def calc_total_weight_for_products(self):
        for rec in self:
            product_weight = sum(
                map(lambda x: x.product_id.weight * x.product_uom_qty, rec.move_ids_without_package))
            if product_weight:
                rec.total_weight = product_weight
            else:
                rec.total_weight = 0

    def get_location_name(self,doc_id,product_id):
        doc=self.env['stock.picking'].search([('id','=',doc_id)])
        for move in  doc.move_ids_without_package.sorted(key=lambda m: m.product_id.id):
            for ml in  move.move_line_ids.sorted(key=lambda ml: ml.location_id.id):
                if ml.product_id.id==product_id:
                    if doc.picking_type_id.code != 'incoming':
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        return ml.location_id.display_name
                    if doc.picking_type_id.code != 'outgoing':
                        print("..............................................")
                        return ml.location_dest_id

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

class ResPartnerNeighborhood(models.Model):
    _name = 'res.partner.neighborhood'

    name = fields.Char()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    neighborhood_id = fields.Many2one('res.partner.neighborhood', string='الحي')

    def get_products_for_vendor(self):
        vendor_id = self.env.context.get('partner_id')
        # Adjust the field name from 'name' to 'partner_id' in your search domain
        supplierinfo_records = self.env['product.supplierinfo'].search([('partner_id', '=', vendor_id)])
        product_ids = list(set([info.product_tmpl_id.id for info in supplierinfo_records]))
        return {
            'name': _('Products'),
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', product_ids)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'product.template',
        }
