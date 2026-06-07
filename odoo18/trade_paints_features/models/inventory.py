from odoo import fields, models,api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_weight = fields.Float('Total weight for products', compute='calc_total_weight_for_products')
    driver_name = fields.Many2one('res.partner', string='Driver name', readonly=False)
    car_number = fields.Char(string='Car number', readonly=False)
    neighborhood_id = fields.Many2one('res.partner.neighborhood', related='partner_id.neighborhood_id',
                                      store=True, string='الحي')

    printed_before = fields.Boolean(default=False)


    @api.depends('move_ids_without_package')
    def calc_total_weight_for_products(self):
        for rec in self:
            product_weight = sum(
                map(lambda x: x.product_id.weight * x.product_uom_qty, rec.move_ids_without_package))
            if product_weight:
                rec.total_weight = product_weight
            else:
                rec.total_weight = 0


    # def get_products_sorted(self, lst):
    #     return sorted(lst, key=lambda x: x.id)

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

