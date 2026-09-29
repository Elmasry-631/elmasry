# -*- coding: utf-8 -*-
"""
stock.move extension
======================
`stock.picking.state` is a stored *computed* field — Odoo sets it by
recomputing from the moves' states during the ORM's internal flush,
not through an explicit `write({'state': 'done'})` call. That means a
`write()` override on stock.picking watching for `vals['state'] ==
'done'` will never actually fire.

`_action_done()` on stock.move is the one place every "mark as done"
path funnels through — our own auto-validate flow, the immediate
transfer wizard, the backorder wizard, or a human validating the
picking manually — so it's the reliable hook.
"""
from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_done(self, cancel_backorder=False):
        moves = super()._action_done(cancel_backorder=cancel_backorder)

        pickings = moves.mapped('picking_id').filtered(
            lambda p: p.sale_id and not p.ebook_email_sent
        )
        for picking in pickings:
            has_ebook = picking.move_ids.filtered(
                lambda m: m.product_id.is_ebook_with_codes and m.state == 'done'
            )
            if has_ebook:
                picking._send_ebook_serial_email()

        return moves
