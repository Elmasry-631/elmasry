# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import _, fields, models
from odoo.tools import float_is_zero

from ..models.product_movement_line import LINE_GROUP, MOVE_TYPES, SUMMARY_GROUPS


class ProductMovementWizard(models.TransientModel):
    _name = 'product.movement.wizard'
    _description = 'Product Movement Lifecycle Wizard'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    lot_id = fields.Many2one(
        'stock.lot', string='Lot/Serial',
        domain="[('product_id', '=', product_id)]",
        help='Leave empty to trace the product as a whole.')
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')
    line_ids = fields.One2many('product.movement.line', 'wizard_id', string='Movements')
    summary_ids = fields.One2many('product.movement.summary', 'wizard_id', string='Movement Summary')

    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id',
                                  string='Currency')

    sales_revenue = fields.Float(string='Sales Revenue', digits='Account')
    sales_cogs = fields.Float(string='Cost of Goods Sold', digits='Account')
    margin = fields.Float(string='Margin', digits='Account')
    margin_pct = fields.Float(string='Margin %')

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------
    @staticmethod
    def _get_move_type(move_line):
        src, dst = move_line.location_id, move_line.location_dest_id
        if dst.scrap_location:
            return 'scrap'
        mapping = {
            ('supplier', 'internal'): 'receipt',
            ('internal', 'supplier'): 'vendor_return',
            ('internal', 'customer'): 'delivery',
            ('customer', 'internal'): 'customer_return',
            ('internal', 'internal'): 'internal',
            ('internal', 'production'): 'mo_consume',
            ('production', 'internal'): 'mo_produce',
            ('inventory', 'internal'): 'adjust_in',
            ('internal', 'inventory'): 'adjust_out',
            ('transit', 'internal'): 'transit_in',
            ('internal', 'transit'): 'transit_out',
        }
        return mapping.get((src.usage, dst.usage), 'other')

    def _get_move_line_domain(self):
        self.ensure_one()
        domain = [
            ('state', '=', 'done'),
            ('product_id', '=', self.product_id.id),
        ]
        if self.lot_id:
            domain.append(('lot_id', '=', self.lot_id.id))
        return domain

    # ------------------------------------------------------------------
    # Costing helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _move_line_cost(line):
        """ Cost booked for a done move line, taken from the valuation layers
            of its move and apportioned by quantity. Zero when the product is
            not valued in real time. """
        move = line.move_id
        total_qty = sum(l.quantity_product_uom for l in move.move_line_ids)
        if not total_qty:
            return 0.0
        layers = move.stock_valuation_layer_ids
        amount = sum(abs(l.value) for l in layers)
        if layers and layers[0].currency_id != line.env.company.currency_id:
            company = line.env.company
            amount = sum(
                abs(l.currency_id._convert(l.value, company.currency_id, company, l.create_date))
                for l in layers)
        return amount * (line.quantity_product_uom / total_qty)

    @staticmethod
    def _move_line_revenue(line, company):
        """ Net selling price of a delivered quantity, from the sale order line
            that generated the move (order currency converted to company). """
        move = line.move_id
        sale_line = move.sale_line_id if 'sale_line_id' in move._fields else None
        if not sale_line:
            return 0.0
        order_qty = sale_line.product_uom_qty or line.quantity_product_uom
        if not order_qty:
            return 0.0
        unit_rev = sale_line.price_subtotal / order_qty
        if sale_line.currency_id != company.currency_id:
            unit_rev = sale_line.currency_id._convert(
                unit_rev, company.currency_id, company, sale_line.date_order)
        return unit_rev * line.quantity_product_uom

    # ------------------------------------------------------------------
    # Core computation
    # ------------------------------------------------------------------
    def _generate_lines(self):
        """Build the detail lines and the accounting-style summary:
           opening balance, purchases, manufacturing, sales, returns, scrap,
           other, closing -- each with quantity and cost, plus sales revenue
           and margin."""
        self.ensure_one()
        self.line_ids.unlink()
        self.summary_ids.unlink()

        move_lines = self.env['stock.move.line'].search(
            self._get_move_line_domain(), order='date, id')
        rounding = self.product_id.uom_id.rounding
        company = self.company_id or self.env.company

        gqty = defaultdict(float)
        gcost = defaultdict(float)
        opening_qty = 0.0
        sales_rev = 0.0
        sales_cogs = 0.0

        balance = 0.0
        cycle = 1
        had_stock = False
        rows = []
        for seq, ml in enumerate(move_lines, start=1):
            src, dst = ml.location_id, ml.location_dest_id
            qty = ml.quantity_product_uom
            qty_in = qty if (dst.usage == 'internal' and src.usage != 'internal') else 0.0
            qty_out = qty if (src.usage == 'internal' and dst.usage != 'internal') else 0.0
            net = qty_in - qty_out
            move_type = self._get_move_type(ml)
            mdate = ml.date.date()

            if self.date_from and mdate < self.date_from:
                # accrues into the opening balance, no detail row
                balance += net
                opening_qty += net
                continue
            if self.date_to and mdate > self.date_to:
                # outside the period: ignored completely
                continue

            cost = self._move_line_cost(ml)
            cost_signed = cost if qty_in else (-cost if qty_out else 0.0)
            group = LINE_GROUP.get(move_type)
            if group:
                gqty[group] += net
                gcost[group] += cost_signed
                if group == 'sales':
                    sales_rev += self._move_line_revenue(ml, company)
                    sales_cogs += cost

            balance += net
            sold_out = False
            if balance > 0 and not float_is_zero(balance, precision_rounding=rounding):
                had_stock = True
            elif had_stock and (balance < 0 or float_is_zero(balance, precision_rounding=rounding)):
                sold_out = True

            rows.append({
                'wizard_id': self.id,
                'sequence': seq,
                'cycle_no': cycle,
                'is_sold_out': sold_out,
                'date': ml.date,
                'reference': ml.reference,
                'picking_id': ml.picking_id.id,
                'origin': ml.move_id.origin or ml.picking_id.origin,
                'move_type': move_type,
                'location_id': src.id,
                'location_dest_id': dst.id,
                'partner_id': ml.picking_id.partner_id.id,
                'lot_id': ml.lot_id.id,
                'user_id': ml.write_uid.id,
                'qty_in': qty_in,
                'qty_out': qty_out,
                'balance': balance,
                'cost': cost_signed,
                'uom_id': self.product_id.uom_id.id,
            })
            if sold_out:
                cycle += 1
                had_stock = False

        # opening value approximated at the product's standard cost
        gqty['opening'] = opening_qty
        gcost['opening'] = opening_qty * self.product_id.standard_price
        gqty['closing'] = opening_qty + sum(
            v for k, v in gqty.items() if k not in ('opening', 'closing'))
        gcost['closing'] = gcost['opening'] + sum(
            v for k, v in gcost.items() if k not in ('opening', 'closing'))

        self.env['product.movement.summary'].create([
            {
                'wizard_id': self.id,
                'sequence': seq,
                'group': grp,
                'name': label,
                'qty': gqty.get(grp, 0.0),
                'cost': gcost.get(grp, 0.0),
                'is_bold': grp in ('opening', 'closing'),
            }
            for seq, (grp, label) in enumerate(SUMMARY_GROUPS, start=1)
        ])

        self.line_ids = [(6, 0, self.env['product.movement.line'].create(rows).ids)]
        self.sales_revenue = sales_rev
        self.sales_cogs = sales_cogs
        self.margin = sales_rev - sales_cogs
        self.margin_pct = (self.margin / sales_rev * 100) if sales_rev else 0.0
        return len(rows)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def action_show(self):
        self.ensure_one()
        self._generate_lines()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Product Movement: %s', self.product_id.display_name),
            'res_model': 'product.movement.wizard',
            'view_mode': 'form',
            'views': [(self.env.ref(
                'product_movement_report.product_movement_wizard_result_form').id, 'form')],
            'res_id': self.id,
            'target': 'current',
        }

    def action_print(self):
        self.ensure_one()
        self._generate_lines()
        return self.env.ref(
            'product_movement_report.action_report_product_movement').report_action(self)

    def get_move_type_label(self, key):
        return dict(MOVE_TYPES).get(key, key)
