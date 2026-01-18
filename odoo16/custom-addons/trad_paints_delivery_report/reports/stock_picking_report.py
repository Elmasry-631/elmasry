from odoo import api, fields, models
from operator import itemgetter
import operator

class Stock(models.AbstractModel):
    _name = 'report.trad_paints_delivery_report.report_all_picking2'

    def get_location_name(self, location_id):
        return self.env['stock.location'].browse(location_id).name

    @api.model
    def _get_report_values(self, docids, data=None):
        StockMove = self.env['stock.move']
        ProductProduct = self.env['product.product']
        StockPickingType = self.env['stock.picking.type']

        picking_type_outgoing = StockPickingType.search([('code', '=', 'outgoing')])
        stock_moves = StockMove.search([('picking_id', 'in', docids), ('picking_type_id', 'in', picking_type_outgoing.ids)])

        product_lines = {}
        locations = set()
        weight_total = 0.0

        for move in stock_moves:
            for line in move.move_line_ids:
                product = ProductProduct.browse(move.product_id.id)
                weight = product.weight * line.qty_done
                key = (line.product_id.id, line.location_id.id)

                if key not in product_lines:
                    product_lines[key] = {
                        'product_id': line.product_id.id,
                        'weight': product.weight,
                        'qty': 0,  # Initialize quantity
                        'product_name': product.product_tmpl_id.name,
                        'location_id': line.location_id.id,
                        'location_name': line.location_id.name
                    }

                product_lines[key]['qty'] += line.qty_done
                weight_total += weight

                locations.add(line.location_id.id)

        # Convert the dictionary to a list for sorting
        lines = list(product_lines.values())
        sorted_lines = sorted(lines, key=lambda l: (l['location_name'], l['product_name']))

        return {
            'data': data,
            'lines': sorted_lines,
            'locations': list(locations),
            'get_location_name': self.get_location_name,
            'doc_number1': self.env['stock.picking'].browse(docids[0]),
            'weight_total': weight_total
        }


# class Stock(models.AbstractModel):

    # _name = 'report.trad_paints_delivery_report.report_all_picking2'



    # def get_location_name(self,location_id):
        # return self.env['stock.location'].search([('id','=',location_id)]).name

    # @api.model
    # def _get_report_values(self, docids, data=None):
        # print("AAAAAAAAAAAAAAAAAAAAAAAAA",docids)
        # locations = []
        # cr = self._cr

        # if len(docids) > 1: 
            # query="""
           # select stock_move.product_id as product_id,product_product.weight as weight,stock_location.seq_in_report as seq,sum(stock_move.product_uom_qty) as qty,stock_move.name as product_name,stock_move_line.location_id as location_id,stock_location.name as location_name
           # from stock_move
            # join stock_move_line on stock_move_line.picking_id = stock_move.picking_id and  stock_move_line.move_id = stock_move.id and stock_move_line.product_id = stock_move.product_id  
           # join product_product on product_product.id = stock_move.product_id 
           # join stock_location on stock_location.id = stock_move_line.location_id 
           # join stock_picking_type on stock_picking_type.id = stock_move.picking_type_id 
           # where stock_move.picking_id in {picking_ids} and stock_picking_type.code = 'outgoing' 
        # group by stock_move.product_id,stock_move.name,stock_move_line.location_id,product_product.weight,stock_location.name,stock_location.seq_in_report
            # order by stock_location.seq_in_report,TRIM(stock_move.name)
           
            
            # """.format(picking_ids=tuple(id for id in docids))
        # else:
            # query = """
                      # select stock_move.product_id as product_id,product_product.weight as weight,stock_location.seq_in_report as seq ,sum(stock_move.product_uom_qty) as qty,stock_move.name as product_name,stock_move_line.location_id as location_id,stock_location.name as location_name
                      # from stock_move
                      # join stock_move_line on stock_move_line.picking_id = stock_move.picking_id and  stock_move_line.move_id = stock_move.id and stock_move_line.product_id = stock_move.product_id  
                      # join product_product on product_product.id = stock_move.product_id 
                      # join stock_location on stock_location.id = stock_move_line.location_id 
                      # join stock_picking_type on stock_picking_type.id = stock_move.picking_type_id 
                      # where stock_move.picking_id = {picking_id}  and stock_picking_type.code = 'outgoing' 
                       # group by stock_move.product_id,stock_move.name,stock_move_line.location_id,product_product.weight,stock_location.name,stock_location.seq_in_report
                       # order by stock_location.seq_in_report,TRIM(stock_move.name)


                       # """.format(picking_id= docids[0])

        # cr.execute(query)
        # lines = cr.dictfetchall()

        # weight_total=0.0
        # for line in lines:
            # if line.get('weight') and line.get('qty'):
                # weight_total +=line.get('weight') *  line.get('qty')

            # if line.get('location_id') not in locations:
                # locations.append(line.get('location_id'))


        # return {
            # 'data': data,
             # 'lines':lines,
             # 'locations':locations,
            # 'get_location_name':self.get_location_name,
            # 'doc_number1':self.env['stock.picking'].browse(docids[0]),
            # 'weight_total':weight_total

        # }
