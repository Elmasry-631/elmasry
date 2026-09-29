# -*- coding: utf-8 -*-
"""
sale.order extension
=====================
eBooks don't need a warehouse worker to pack a box, so as soon as the
order is confirmed we reserve and validate the delivery ourselves.

Serial picking itself is NOT done manually here. Odoo's stock
reservation (`move._action_assign()`) already knows how to pick
`qty` distinct serial-tracked quants for a move according to the
warehouse's removal strategy (FIFO by default), and it does so under
row-level locking — so two concurrent orders can never be handed the
same serial. Re-implementing that with a manual query would just
duplicate (and risk breaking) logic Odoo already gets right.
"""
from markupsafe import Markup

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Placeholder for the eBook email template: lets the template (edited
    # from Odoo) show the delivered serials anywhere in the email body.
    ebook_serial_numbers_html = fields.Html(
        string="Delivered eBook Serials",
        compute='_compute_ebook_serial_numbers_html',
        sanitize=False,
        groups='stock.group_stock_user',
        help="Delivered eBook serial numbers of this order, for use in email templates.",
    )

    @api.depends('picking_ids.move_line_ids.state', 'picking_ids.move_line_ids.lot_id')
    def _compute_ebook_serial_numbers_html(self):
        for order in self:
            move_lines = order.picking_ids.filtered(
                lambda picking: picking.picking_type_code == 'outgoing'
            ).move_line_ids.filtered(
                lambda line: line.state == 'done' and line.lot_id and line.product_id.is_ebook_with_codes
            )
            if not move_lines:
                order.ebook_serial_numbers_html = False
                continue
            items = Markup().join(
                Markup('<li>%s: <strong>%s</strong></li>') % (line.product_id.display_name, line.lot_id.name)
                for line in move_lines
            )
            order.ebook_serial_numbers_html = Markup('<ul>%s</ul>') % items

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        """Hard cap eBook quantities in the cart to what's actually on the
        shelf. The "Continue selling when out of stock" flag only hides
        the *first* Add to Cart click on the product page — it does not
        stop someone raising the quantity of a line that's already in
        the cart. This hook is the one place website_sale funnels every
        cart change through (initial add AND later qty edits), so it's
        the reliable place to enforce it.
        """
        if product_id:
            product = self.env['product.product'].browse(product_id)
            if product.is_ebook_with_codes:
                available = product.qty_available
                current_line = self.order_line.filtered(
                    lambda l: l.id == line_id
                ) if line_id else self.order_line.filtered(
                    lambda l: l.product_id.id == product_id
                )
                current_qty = current_line.product_uom_qty if current_line else 0
                requested_qty = set_qty if set_qty else current_qty + (add_qty or 0)

                if requested_qty > available:
                    set_qty = available
                    add_qty = 0

        return super()._cart_update(
            product_id=product_id, line_id=line_id,
            add_qty=add_qty, set_qty=set_qty, **kwargs
        )

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if any(l.product_id.is_ebook_with_codes for l in order.order_line):
                order._auto_deliver_ebooks()
        return res

    def _auto_deliver_ebooks(self):
        self.ensure_one()
        pickings = self.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))

        for picking in pickings:
            ebook_moves = picking.move_ids.filtered(lambda m: m.product_id.is_ebook_with_codes)
            if not ebook_moves:
                continue

            picking.action_assign()

            short_moves = ebook_moves.filtered(lambda m: m.quantity < m.product_uom_qty)
            if short_moves:
                # Do NOT raise here: the order (and the payment behind it)
                # must stay confirmed — the customer already paid. Leave
                # this delivery pending, exactly like any ordinary
                # out-of-stock backorder, and record it on the chatter so
                # staff can see it and top up serials. Once someone adds
                # more serials and validates the picking (or a resend is
                # triggered), the eBook email fires automatically via the
                # _action_done hook in stock_move.py.
                names = ', '.join(short_moves.mapped('product_id.display_name'))
                self.message_post(body=_(
                    "⚠️ Not enough available Serial Numbers for: %s. "
                    "The order is confirmed and paid, but the eBook "
                    "delivery is on hold until more serials are added "
                    "to stock. Validate the delivery manually once "
                    "restocked.",
                ) % names)
                continue

            if picking.state != 'assigned':
                continue

            result = picking.button_validate()
            if isinstance(result, dict):
                wizard_model = result.get('res_model')
                if wizard_model:
                    wizard = self.env[wizard_model].with_context(
                        **result.get('context', {})
                    ).create({})
                    if wizard_model == 'stock.backorder.confirmation':
                        wizard.process_cancel_backorder()
                    else:
                        wizard.process()
