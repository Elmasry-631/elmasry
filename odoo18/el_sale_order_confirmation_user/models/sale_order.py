# -*- coding: utf-8 -*-
from odoo import fields, models

# Internal context key used to allow this module's own code to write
# confirmed_by_id. Any write() call that does not carry this flag will have
# confirmed_by_id silently stripped from its vals, so the field can never be
# set through the normal UI / API / RPC write path.
INTERNAL_WRITE_KEY = '_so_confirmed_by_internal_write'


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_by_id = fields.Many2one(
        'res.users',
        string='Confirmed By',
        readonly=True,
        copy=False,
        index=True,
        help="User who actually triggered the confirmation of this order "
             "(clicked Confirm, ran a batch confirmation, or triggered an "
             "automated/programmatic confirmation). This is NOT the "
             "Salesperson, the record creator, or the last writer. "
             "Left empty for orders that were already confirmed before this "
             "module was installed, since the original confirming user "
             "cannot be reliably determined from existing Odoo data.",
    )

    def action_confirm(self):
        """Extend the standard confirmation entry point to stamp
        confirmed_by_id with the user actually performing the confirmation.

        Overriding the *public* action_confirm() (rather than the private
        _action_confirm()) lets us compare state before/after super(), so we
        only stamp orders that are genuinely transitioning into 'sale'
        right now. This covers every confirmation path, because they all
        funnel through this same method:
          - Normal UI "Confirm" button
          - Batch confirmation (multiple orders selected in the list view)
          - Programmatic confirmation (order.action_confirm() from code)
          - Automated confirmation (e.g. automated actions, integrations,
            online payment/signature flows) that call action_confirm()
        In all these cases self.env.user is the acting user in that
        execution context.
        """
        orders_to_stamp = self.filtered(lambda so: so.state != 'sale')
        result = super().action_confirm()
        if orders_to_stamp:
            orders_to_stamp.with_context(**{INTERNAL_WRITE_KEY: True}).write({
                'confirmed_by_id': self.env.user.id,
            })
        return result

    def write(self, vals):
        """Prevent confirmed_by_id from being modified through a normal
        write() call (UI, API, RPC, import, etc.). It can only be set from
        action_confirm() above, which passes the internal context flag.
        """
        if 'confirmed_by_id' in vals and not self.env.context.get(INTERNAL_WRITE_KEY):
            vals = dict(vals)
            vals.pop('confirmed_by_id')
        return super().write(vals)
