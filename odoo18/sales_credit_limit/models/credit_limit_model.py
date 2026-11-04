from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # --- Credit Limit Fields ---
    active_limit = fields.Boolean("Active Credit Limit", default=False)
    warning_stage = fields.Float(
        string='Warning Amount',
        help="A warning message will appear once the selected customer crosses the warning amount. "
             "Set its value to 0.00 to disable this feature"
    )
    blocking_stage = fields.Float(
        string='Blocking Amount',
        help="Cannot make sales once the selected customer crosses the blocking amount. "
             "Set its value to 0.00 to disable this feature"
    )

    # --- Computed Fields ---
    due_amount = fields.Float(string="Total Due", compute="_compute_due_amount", store=True)

    # --- Helper Booleans for Visibility (Odoo 18 t-if) ---
    warning_stage_visible = fields.Boolean(compute='_compute_limit_visibility')
    blocking_stage_visible = fields.Boolean(compute='_compute_limit_visibility')

    @api.depends('active_limit')
    def _compute_limit_visibility(self):
        for rec in self:
            rec.warning_stage_visible = rec.active_limit
            rec.blocking_stage_visible = rec.active_limit

    @api.depends('debit', 'credit')
    def _compute_due_amount(self):
        for rec in self:
            if not rec.id:
                continue
            rec.due_amount = rec.credit - rec.debit

    # --- Constraints ---
    @api.constrains('warning_stage', 'blocking_stage')
    def _check_warning_blocking(self):
        for rec in self:
            if rec.active_limit and rec.blocking_stage > 0:
                if rec.warning_stage >= rec.blocking_stage:
                    raise UserError(_("Warning amount should be less than Blocking amount"))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # --- Fields for Alerts ---
    has_due = fields.Boolean()
    is_warning = fields.Boolean()
    due_amount = fields.Float(related='partner_id.due_amount', string="Customer Due")

    # --- Override confirm to check blocking limit ---
    def action_confirm(self):
        for order in self:
            partner = order.partner_id
            if partner.active_limit and partner.blocking_stage != 0:
                if order.due_amount >= partner.blocking_stage:
                    raise UserError(_(
                        "This customer is in Blocking Stage and has %.2f to pay."
                    ) % order.due_amount)
        return super(SaleOrder, self).action_confirm()

    # --- Onchange to update alert flags dynamically ---
    @api.onchange('partner_id')
    def _onchange_partner_due_warning(self):
        for order in self:
            partner = order.partner_id
            # Check due amount
            order.has_due = partner.due_amount > 0
            # Check warning stage
            if partner.active_limit and partner.warning_stage != 0:
                order.is_warning = order.due_amount >= partner.warning_stage
            else:
                order.is_warning = False
