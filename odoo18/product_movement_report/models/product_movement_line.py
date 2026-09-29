# -*- coding: utf-8 -*-
from odoo import fields, models

MOVE_TYPES = [
    ('receipt', 'Receipt (Vendor)'),
    ('vendor_return', 'Return to Vendor'),
    ('delivery', 'Delivery (Customer)'),
    ('customer_return', 'Customer Return'),
    ('internal', 'Internal Transfer'),
    ('mo_consume', 'Manufacturing Consumption'),
    ('mo_produce', 'Manufacturing Production'),
    ('scrap', 'Scrap'),
    ('adjust_in', 'Inventory Adjustment (+)'),
    ('adjust_out', 'Inventory Adjustment (-)'),
    ('transit_in', 'Transit In'),
    ('transit_out', 'Transit Out'),
    ('other', 'Other'),
]

SUMMARY_GROUPS = [
    ('opening', 'Opening Balance'),
    ('purchase', 'Purchases (Vendor Receipts)'),
    ('production', 'Manufacturing (Produced)'),
    ('sales', 'Sales (Deliveries)'),
    ('returns', 'Returns (Customer & Vendor)'),
    ('scrap', 'Scrap'),
    ('misc', 'Other (Consumptions, Adjustments, Transit)'),
    ('closing', 'Closing Balance'),
]

# move_type -> summary group (internal transfers excluded, they are net-zero)
LINE_GROUP = {
    'receipt': 'purchase',
    'transit_in': 'purchase',
    'mo_produce': 'production',
    'mo_consume': 'misc',
    'delivery': 'sales',
    'customer_return': 'returns',
    'vendor_return': 'returns',
    'scrap': 'scrap',
    'adjust_in': 'misc',
    'adjust_out': 'misc',
    'transit_out': 'misc',
    'other': 'misc',
}


class ProductMovementLine(models.TransientModel):
    _name = 'product.movement.line'
    _description = 'Product Movement Report Line'
    _order = 'sequence, id'

    wizard_id = fields.Many2one('product.movement.wizard', ondelete='cascade', index=True)
    sequence = fields.Integer()
    cycle_no = fields.Integer(string='Cycle')
    is_sold_out = fields.Boolean(string='Sold Out', help='Balance returned to zero after this move.')
    date = fields.Datetime()
    reference = fields.Char()
    picking_id = fields.Many2one('stock.picking', string='Transfer')
    origin = fields.Char(string='Source Document')
    move_type = fields.Selection(MOVE_TYPES, string='Movement Type')
    location_id = fields.Many2one('stock.location', string='From')
    location_dest_id = fields.Many2one('stock.location', string='To')
    partner_id = fields.Many2one('res.partner', string='Partner')
    lot_id = fields.Many2one('stock.lot', string='Lot/Serial')
    user_id = fields.Many2one('res.users', string='User')
    qty_in = fields.Float(string='In', digits='Product Unit of Measure')
    qty_out = fields.Float(string='Out', digits='Product Unit of Measure')
    balance = fields.Float(string='Balance', digits='Product Unit of Measure')
    cost = fields.Float(string='Cost', digits='Account')
    uom_id = fields.Many2one('uom.uom', string='UoM')


class ProductMovementSummary(models.TransientModel):
    _name = 'product.movement.summary'
    _description = 'Product Movement Summary Line'
    _order = 'sequence, id'

    wizard_id = fields.Many2one('product.movement.wizard', ondelete='cascade', index=True)
    sequence = fields.Integer()
    group = fields.Selection(SUMMARY_GROUPS, string='Stage')
    name = fields.Char(string='Stage')
    qty = fields.Float(string='Quantity', digits='Product Unit of Measure')
    cost = fields.Float(string='Cost', digits='Account')
    is_bold = fields.Boolean(string='Bold')
