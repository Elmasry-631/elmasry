from odoo import api, fields, models


class ResPartner(models.Model):
    """Extend res.partner with a Payment Gateway link.

    When a ``payment_gateway_id`` is selected on a partner, the gateway's
    default Receivable and Payable accounts are automatically copied into
    the partner's ``property_account_receivable_id`` and
    ``property_account_payable_id`` fields (which already exist on
    ``res.partner`` via the ``account`` module).

    The two account fields are kept READ-ONLY on the partner form so the
    user cannot desynchronize them from the gateway — the canonical
    configuration lives on ``sale.payment.gateway``.

    Auto-fill behavior
    ------------------
    * On partner create with a gateway → accounts are filled from gateway.
    * On partner write changing the gateway → accounts are re-filled
      from the new gateway. If the new gateway has no account configured,
      the previous value is left in place (we never silently NULL-out
      an existing account).
    * On gateway write changing its accounts → all linked partners are
      updated to mirror the new accounts (handled in
      ``sale.payment.gateway.write``).
    """

    _inherit = 'res.partner'

    # ------------------------------------------------------------------
    # NEW FIELD
    # ------------------------------------------------------------------
    payment_gateway_id = fields.Many2one(
        'sale.payment.gateway',
        string='Payment Gateway',
        help='Selecting a payment gateway auto-fills the Receivable and '
             'Payable accounts on this partner from the gateway defaults.',
        tracking=True,
    )

    # ------------------------------------------------------------------
    # ON-CHANGE — live auto-fill when the user picks a gateway
    # ------------------------------------------------------------------
    @api.onchange('payment_gateway_id')
    def _onchange_payment_gateway_id(self):
        """When the user selects a payment gateway, auto-fill the
        Receivable and Payable accounts from the gateway defaults.

        The change is NOT applied when the gateway has no account set,
        so the user can clear the gateway without losing the previously
        filled accounts.
        """
        gateway = self.payment_gateway_id
        if not gateway:
            return
        if gateway.property_account_receivable_id:
            self.property_account_receivable_id = \
                gateway.property_account_receivable_id
        if gateway.property_account_payable_id:
            self.property_account_payable_id = \
                gateway.property_account_payable_id

    # ------------------------------------------------------------------
    # CREATE / WRITE — enforce the auto-fill server-side so API callers
    # and batch imports also get the behavior, not just the UI.
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """Before creating partners, fill the account-property fields
        from the chosen payment gateway (if any).
        """
        for vals in vals_list:
            self._sync_gateway_accounts(vals)
        partners = super().create(vals_list)
        return partners

    def write(self, vals):
        """If ``payment_gateway_id`` is being changed, refresh the
        account-property fields from the new gateway before writing.
        """
        if 'payment_gateway_id' in vals:
            # If only the gateway is being written, we need to read the
            # current partner state to know whether to override the
            # accounts. We do this per-partner because different partners
            # may receive different gateways in the same write batch.
            gateway_id = vals['payment_gateway_id']
            gateway = self.env['sale.payment.gateway'].browse(gateway_id) \
                if gateway_id else self.env['sale.payment.gateway']
            new_vals = dict(vals)
            if gateway:
                if gateway.property_account_receivable_id and \
                        'property_account_receivable_id' not in vals:
                    new_vals['property_account_receivable_id'] = \
                        gateway.property_account_receivable_id.id
                if gateway.property_account_payable_id and \
                        'property_account_payable_id' not in vals:
                    new_vals['property_account_payable_id'] = \
                        gateway.property_account_payable_id.id
            return super().write(new_vals)
        return super().write(vals)

    # ------------------------------------------------------------------
    # HELPER
    # ------------------------------------------------------------------
    def _sync_gateway_accounts(self, vals):
        """If ``vals`` contains a ``payment_gateway_id``, fill the
        account-property fields from the gateway defaults — but ONLY
        if the caller has NOT already supplied an explicit value for
        those fields (explicit values win).

        Mutates ``vals`` in place.
        """
        gateway_id = vals.get('payment_gateway_id')
        if not gateway_id:
            return
        gateway = self.env['sale.payment.gateway'].browse(gateway_id)
        if not gateway.property_account_receivable_id and \
                'property_account_receivable_id' not in vals:
            vals['property_account_receivable_id'] = \
                gateway.property_account_receivable_id.id
        if not gateway.property_account_payable_id and \
                'property_account_payable_id' not in vals:
            vals['property_account_payable_id'] = \
                gateway.property_account_payable_id.id
