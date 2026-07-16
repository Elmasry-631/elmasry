"""Stock Movement Report — business logic.

Performance design (per spec):
    1. Single batch fetch of stock.move.line records within the date range
       and filtered by warehouse/location/product/category.
    2. Separate batch fetch for opening balance (date < from_date).
    3. Prefetch product.standard_price and product.uom_id via read()
       to avoid N+1 queries.
    4. Build an in-memory dict {product_id: [move_line_data, ...]} and
       compute running balances with pure Python — no ORM calls in the
       movement loop.

Source-of-truth tables (per spec):
    * stock.move.line     — actual quantities moved (in/out)
    * product.product     — standard_price (Community Edition cost source)
"""

from __future__ import annotations

from collections import defaultdict

from odoo import _, api, models, fields
from odoo.exceptions import UserError


class StockMovementReport(models.AbstractModel):
    """Abstract model that produces the report data structure.

    The QWeb template iterates over the dict returned by
    ``get_report_data()``. We use an AbstractModel (not TransientModel)
    because the report is rendered from a wizard — no records persist.
    """

    _name = 'stock.movement.report'
    _description = 'Stock Movement Report (abstract data provider)'

    # ─── Public entry point ──────────────────────────────────────────

    def get_report_data(
        self,
        date_from,
        date_to,
        warehouse_id=False,
        location_id=False,
        product_id=False,
        categ_id=False,
    ):
        """Return the report payload as a dict.

        :raises UserError: if date_from > date_to.
        """
        # ─── 1. Validate inputs ──────────────────────────────────────
        if date_from > date_to:
            raise UserError(_(
                "From Date (%(frm)s) cannot be after To Date (%(to)s).",
                frm=date_from, to=date_to,
            ))

        company = self.env.company

        # ─── 2. Build the domain (single source for both opening + period) ─
        base_domain = self._build_base_domain(
            company, warehouse_id, location_id, product_id, categ_id
        )

        # ─── 3. Identify products that have ANY movement in the period ─
        period_domain = base_domain + [
            ('date', '>=', date_from),
            ('date', '<=', date_to),
            ('state', '=', 'done'),
        ]
        product_ids_in_period = self.env['stock.move.line'].read_group(
            period_domain,
            ['product_id'],
            ['product_id'],
        )
        product_ids = [g['product_id'][0] for g in product_ids_in_period if g['product_id']]
        if not product_ids:
            return self._empty_payload(date_from, date_to, warehouse_id, location_id, company)

        products = self.env['product.product'].browse(product_ids).exists()

        # ─── 4. Batch-prefetch product data (cost, uom, category, name, code) ─
        product_data = self._prefetch_product_data(products)

        # ─── 5. Fetch opening balances (date < date_from) — batch ─────
        opening_domain = base_domain + [
            ('date', '<', date_from),
            ('state', '=', 'done'),
        ]
        opening_by_product = self._compute_opening_balances(opening_domain, product_data)

        # ─── 6. Fetch all period move lines — single batch read ───────
        move_line_fields = [
            'id', 'date', 'reference', 'product_id', 'product_uom_id',
            'qty_done', 'location_id', 'location_dest_id',
            'move_id', 'picking_id',
        ]
        move_lines = self.env['stock.move.line'].search_read(
            period_domain,
            move_line_fields,
            order='date asc, id asc',
        )
        # Group by product_id (in memory — no more queries)
        lines_by_product = defaultdict(list)
        for ml in move_lines:
            lines_by_product[ml['product_id'][0]].append(ml)

        # ─── 7. Batch-prefetch partner + location names (avoid N+1 in loop) ─
        picking_ids = {ml['picking_id'][0] for ml in move_lines if ml['picking_id']}
        partner_map = {}
        if picking_ids:
            pickings = self.env['stock.picking'].browse(picking_ids)
            partner_map = {p.id: p.partner_id.display_name for p in pickings}
        location_ids = {ml['location_id'][0] for ml in move_lines} | \
                       {ml['location_dest_id'][0] for ml in move_lines}
        locations = self._prefetch_names(self.env['stock.location'].browse(location_ids))

        # ─── 8. Compute running balances per product (in memory) ──────
        scope_location_ids = self._scope_location_ids(
            warehouse_id.id if warehouse_id else False,
            location_id.id if location_id else False,
        )

        products_payload = []
        for product in products:
            pdata = product_data[product.id]
            opening = opening_by_product.get(product.id, {'qty': 0.0, 'value': 0.0})
            opening_qty = opening['qty']
            unit_cost = pdata['cost']

            opening_payload = {
                'qty': opening_qty,
                'unit_cost': unit_cost,
                'value': opening_qty * unit_cost,
            }

            lines_payload = []
            running_qty = opening_qty
            total_in = 0.0
            total_out = 0.0

            for ml in lines_by_product.get(product.id, []):
                qty_done = ml['qty_done'] or 0.0
                # Determine direction based on scope
                src_in_scope = (not scope_location_ids) or \
                               (ml['location_id'][0] in scope_location_ids)
                dst_in_scope = (not scope_location_ids) or \
                               (ml['location_dest_id'][0] in scope_location_ids)
                # Default: treat as outgoing when no scope (whole company)
                incoming = dst_in_scope and not src_in_scope

                if incoming:
                    in_qty = qty_done
                    out_qty = 0.0
                    total_in += qty_done
                else:
                    in_qty = 0.0
                    out_qty = qty_done
                    total_out += qty_done

                running_qty += in_qty - out_qty

                lines_payload.append({
                    'date': ml['date'],
                    'reference': ml['reference'] or '',
                    'partner': partner_map.get(ml['picking_id'][0] if ml['picking_id'] else 0, ''),
                    'source': locations.get(ml['location_id'][0], ''),
                    'destination': locations.get(ml['location_dest_id'][0], ''),
                    'in_qty': in_qty,
                    'in_unit': pdata['uom_name'],
                    'in_price': unit_cost if in_qty else 0.0,
                    'in_total': in_qty * unit_cost,
                    'out_qty': out_qty,
                    'out_unit': pdata['uom_name'],
                    'out_price': unit_cost if out_qty else 0.0,
                    'out_total': out_qty * unit_cost,
                    'bal_qty': running_qty,
                    'bal_unit': pdata['uom_name'],
                    'bal_price': unit_cost,
                    'bal_total': running_qty * unit_cost,
                })

            closing_qty = opening_qty + total_in - total_out
            products_payload.append({
                'product': product,
                'product_name': pdata['name'],
                'product_code': pdata['code'],
                'category': pdata['category'],
                'uom': pdata['uom_name'],
                'opening': opening_payload,
                'lines': lines_payload,
                'summary': {
                    'opening_qty': opening_qty,
                    'total_in': total_in,
                    'total_out': total_out,
                    'closing_qty': closing_qty,
                    'unit_cost': unit_cost,
                    'inventory_value': closing_qty * unit_cost,
                },
            })

        return {
            'date_from': date_from,
            'date_to': date_to,
            'warehouse': warehouse_id,
            'location': location_id,
            'company': company,
            'products': products_payload,
        }

    # ─── Helpers ─────────────────────────────────────────────────────

    def _build_base_domain(self, company, warehouse_id, location_id, product_id, categ_id):
        """Build the shared domain used for both opening and period queries."""
        domain = [('company_id', '=', company.id)]
        if location_id:
            domain += ['|',
                       ('location_id', 'child_of', location_id.id),
                       ('location_dest_id', 'child_of', location_id.id)]
        elif warehouse_id:
            wh = warehouse_id
            location_ids = [wh.lot_stock_id.id]
            picking_types = self.env['stock.picking.type'].search(
                [('warehouse_id', '=', wh.id)]
            )
            for pt in picking_types:
                if pt.default_location_src_id:
                    location_ids.append(pt.default_location_src_id.id)
                if pt.default_location_dest_id:
                    location_ids.append(pt.default_location_dest_id.id)
            domain += ['|',
                       ('location_id', 'in', list(set(location_ids))),
                       ('location_dest_id', 'in', list(set(location_ids)))]
        if product_id:
            domain += [('product_id', '=', product_id.id)]
        elif categ_id:
            domain += [('product_id.categ_id', 'child_of', categ_id.id)]
        return domain

    def _prefetch_product_data(self, products):
        """Single query to load all product fields the report needs."""
        result = {}
        if not products:
            return result
        fields_to_read = ['id', 'name', 'default_code', 'standard_price',
                          'uom_id', 'categ_id']
        for prod in products.read(fields_to_read):
            uom_name = prod['uom_id'][1] if prod['uom_id'] else ''
            categ_name = prod['categ_id'][1] if prod['categ_id'] else ''
            result[prod['id']] = {
                'name': prod['name'],
                'code': prod['default_code'] or '',
                'cost': prod['standard_price'] or 0.0,
                'uom_id': prod['uom_id'][0] if prod['uom_id'] else False,
                'uom_name': uom_name,
                'category': categ_name,
            }
        return result

    def _compute_opening_balances(self, opening_domain, product_data):
        """Aggregate qty_done per product for all moves before date_from."""
        result = defaultdict(lambda: {'qty': 0.0, 'value': 0.0})
        move_lines = self.env['stock.move.line'].search_read(
            opening_domain,
            ['product_id', 'qty_done', 'location_id', 'location_dest_id'],
        )
        scope_location_ids = self.env.context.get('_scope_location_ids')
        for ml in move_lines:
            pid = ml['product_id'][0] if ml['product_id'] else None
            if pid is None or pid not in product_data:
                continue
            qty = ml['qty_done'] or 0.0
            if scope_location_ids is None:
                # No scope restriction — internal moves cancel, treat
                # moves between internal and customer/supplier as out/in
                continue  # Conservative: ignore when no scope
            src_in_scope = ml['location_id'][0] in scope_location_ids
            dst_in_scope = ml['location_dest_id'][0] in scope_location_ids
            if dst_in_scope and not src_in_scope:
                result[pid]['qty'] += qty  # incoming
            elif src_in_scope and not dst_in_scope:
                result[pid]['qty'] -= qty  # outgoing
            # else: internal move within scope — no net change
        for pid, data in result.items():
            data['value'] = data['qty'] * product_data[pid]['cost']
        return dict(result)

    def _scope_location_ids(self, warehouse_id, location_id):
        """Return the set of location IDs considered "in scope".

        Returns ``None`` if no scope restriction (whole company).
        """
        if location_id:
            return set(self.env['stock.location'].search(
                [('id', 'child_of', location_id)]
            ).ids)
        if warehouse_id:
            wh = self.env['stock.warehouse'].browse(warehouse_id)
            return set(self.env['stock.location'].search(
                [('id', 'child_of', wh.lot_stock_id.id)]
            ).ids)
        return None

    def _prefetch_names(self, records):
        """Return ``{id: name}`` dict for a recordset — single SQL query."""
        if not records:
            return {}
        return {r.id: r.display_name for r in records}

    def _empty_payload(self, date_from, date_to, warehouse_id, location_id, company):
        return {
            'date_from': date_from,
            'date_to': date_to,
            'warehouse': warehouse_id,
            'location': location_id,
            'company': company,
            'products': [],
        }


class StockMovementReportWizard(models.TransientModel):
    """Transient wizard that collects report filters and prints the PDF."""

    _name = 'stock.movement.report.wizard'
    _description = 'Stock Movement Report Wizard'

    date_from = fields.Date(string='From Date', required=True,
                            help='Start of the reporting period.')
    date_to = fields.Date(string='To Date', required=True,
                          help='End of the reporting period (inclusive).')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse',
                                   help='Optional: restrict to one warehouse.')
    location_id = fields.Many2one('stock.location', string='Location',
                                   help='Optional: restrict to one location subtree.')
    product_id = fields.Many2one('product.product', string='Product',
                                  help='Optional: restrict to one product.')
    categ_id = fields.Many2one('product.category', string='Product Category',
                                help='Optional: restrict to a product category subtree.')

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        """Validate that date_from is not after date_to."""
        for wiz in self:
            if wiz.date_from and wiz.date_to and wiz.date_from > wiz.date_to:
                raise UserError(_(
                    "From Date (%(frm)s) cannot be after To Date (%(to)s).",
                    frm=wiz.date_from, to=wiz.date_to,
                ))

    def action_print_pdf(self):
        """Trigger the QWeb PDF report with the wizard's filters."""
        self.ensure_one()
        data = {
            'date_from': fields.Date.to_date(self.date_from).isoformat() if self.date_from else False,
            'date_to': fields.Date.to_date(self.date_to).isoformat() if self.date_to else False,
            'warehouse_id': self.warehouse_id.id if self.warehouse_id else False,
            'location_id': self.location_id.id if self.location_id else False,
            'product_id': self.product_id.id if self.product_id else False,
            'categ_id': self.categ_id.id if self.categ_id else False,
        }
        return self.env.ref(
            'ie_stock_movement_report.action_report_stock_movement'
        ).report_action(self, data=data)


# Need fields import at module level (used by wizard.action_print_pdf)
from odoo import fields  # noqa: E402
