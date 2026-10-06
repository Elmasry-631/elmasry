from odoo import models, fields


class SalePaymentGateway(models.Model):
    _name = 'sale.payment.gateway'
    _description = 'Sale Payment Gateway'

    name = fields.Char(string="Payment Gateway", required=True)
    active = fields.Boolean(default=True)

    # ------------------------------------------------------------------
    # Default accounting accounts linked to this payment gateway.
    # These are mirrored onto res.partner's property_account_receivable_id
    # and property_account_payable_id when a gateway is selected on a
    # partner. The partner-side fields are READ-ONLY — the canonical
    # configuration lives here.
    # ------------------------------------------------------------------
    property_account_receivable_id = fields.Many2one(
        'account.account',
        string="Receivable Account",
        company_dependent=True,
        domain="[('account_type', '=', 'asset_receivable')]",
        help="Default receivable account used for customers linked to "
             "this payment gateway. This value is mirrored on res.partner "
             "as a read-only field.",
    )
    property_account_payable_id = fields.Many2one(
        'account.account',
        string="Payable Account",
        company_dependent=True,
        domain="[('account_type', '=', 'liability_payable')]",
        help="Default payable account used for vendors linked to "
             "this payment gateway. This value is mirrored on res.partner "
             "as a read-only field.",
    )

    # ------------------------------------------------------------------
    # PROPAGATION — when the gateway's accounts change, push the new
    # values to every partner that is currently linked to this gateway.
    # ------------------------------------------------------------------
    def write(self, vals):
        res = super().write(vals)
        if 'property_account_receivable_id' in vals or \
                'property_account_payable_id' in vals:
            # Build the write-once value dict (same for all linked partners
            # because `vals` is the same for the whole batch).
            write_vals = {}
            if 'property_account_receivable_id' in vals and \
                    vals['property_account_receivable_id']:
                write_vals['property_account_receivable_id'] = \
                    vals['property_account_receivable_id']
            if 'property_account_payable_id' in vals and \
                    vals['property_account_payable_id']:
                write_vals['property_account_payable_id'] = \
                    vals['property_account_payable_id']
            if write_vals:
                # Single search for ALL gateways in the batch — no N+1.
                # Use sudo() to bypass record rules — partners may belong
                # to companies / groups the current user cannot write to.
                partners = self.env['res.partner'].sudo().search([
                    ('payment_gateway_id', 'in', self.ids),
                ])
                # skip_sync_from_gateway context flag avoids any future
                # re-entrancy if a partner.write ever calls gateway.write.
                partners.with_context(
                    skip_sync_from_gateway=True
                ).sudo().write(write_vals)
        return res
