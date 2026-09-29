from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    actual_qty = fields.Float(
        string="Actual Quantity",
        digits="Product Unit",
        copy=True,
        help="Physical quantity received into stock. The original ordered quantity and commercial value remain unchanged.",
    )
    effective_price_unit = fields.Float(
        string="Effective Unit Cost",
        compute="_compute_effective_price_unit",
        digits="Product Price",
        help="Original line value redistributed over the actual quantity.",
    )
    variance_qty = fields.Float(
        string="Quantity Variance",
        compute="_compute_variance",
        digits="Product Unit",
    )
    variance_percent = fields.Float(
        string="Variance %",
        compute="_compute_variance",
        digits=(16, 2),
    )

    @api.depends("product_qty", "actual_qty", "price_unit")
    def _compute_effective_price_unit(self):
        for line in self:
            rounding = line.product_uom.rounding if line.product_uom else 0.01
            if line.display_type or float_is_zero(line.actual_qty, precision_rounding=rounding):
                line.effective_price_unit = 0.0
            else:
                line.effective_price_unit = (
                    line.price_unit * line.product_qty / line.actual_qty
                )

    @api.depends("product_qty", "actual_qty")
    def _compute_variance(self):
        for line in self:
            line.variance_qty = line.product_qty - line.actual_qty
            line.variance_percent = (
                line.variance_qty / line.product_qty * 100.0
                if line.product_qty else 0.0
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if (
                not vals.get("display_type")
                and "actual_qty" not in vals
                and vals.get("product_qty") is not None
            ):
                vals["actual_qty"] = vals["product_qty"]
        return super().create(vals_list)

    @api.onchange("product_id", "product_qty")
    def _onchange_actual_qty_default(self):
        for line in self:
            if not line.display_type and not line.actual_qty and line.product_qty:
                line.actual_qty = line.product_qty

    @api.constrains("actual_qty")
    def _check_actual_qty(self):
        allow_over = self.env["ir.config_parameter"].sudo().get_param(
            "el_purchase_actual_qty.allow_actual_over_ordered", "False"
        ) == "True"
        for line in self:
            if line.display_type:
                continue
            if line.actual_qty < 0:
                raise ValidationError(_("Actual Quantity cannot be negative."))
            if (
                not allow_over
                and line.product_qty
                and line.actual_qty > line.product_qty
            ):
                raise ValidationError(
                    _("Actual Quantity cannot exceed Ordered Quantity.")
                )

    def write(self, vals):
        if "actual_qty" in vals:
            precision = self.env["decimal.precision"].precision_get("Product Unit")
            for line in self:
                if (
                    line.order_id.state not in ("draft", "sent", "cancel")
                    and float_compare(
                        line.actual_qty,
                        vals["actual_qty"],
                        precision_digits=precision,
                    ) != 0
                ):
                    raise ValidationError(
                        _("Actual Quantity cannot be changed after the Purchase Order is confirmed.")
                    )
        return super().write(vals)

    @api.depends(
        "invoice_lines.move_id.state",
        "invoice_lines.quantity",
        "qty_received",
        "product_uom_qty",
        "order_id.state",
        "actual_qty",
        "product_id.purchase_method",
    )
    def _compute_qty_invoiced(self):
        super()._compute_qty_invoiced()
        for line in self:
            if line.display_type or line.order_id.state != "purchase":
                continue
            if line.product_id.purchase_method == "purchase":
                line.qty_to_invoice = line.actual_qty - line.qty_invoiced

    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line(move=move)
        self.ensure_one()
        if self.display_type or not self.actual_qty:
            return res
        # Keep the full original line value while invoicing the physical quantity.
        billable_qty = max(self.actual_qty - self.qty_invoiced, 0.0)
        res["quantity"] = billable_qty
        res["price_unit"] = (
            res.get("price_unit", 0.0) * self.product_qty / self.actual_qty
        )
        return res

    def _prepare_stock_moves(self, picking):
        moves_vals = super()._prepare_stock_moves(picking)
        self.ensure_one()
        if self.display_type or not self.product_id or not moves_vals:
            return moves_vals

        rounding = self.product_uom.rounding
        if float_is_zero(self.actual_qty, precision_rounding=rounding):
            for vals in moves_vals:
                vals["product_uom_qty"] = 0.0
            return moves_vals

        original_total = sum(vals.get("product_uom_qty", 0.0) for vals in moves_vals)
        if float_is_zero(original_total, precision_rounding=rounding):
            moves_vals[0]["product_uom_qty"] = self.actual_qty
        else:
            remaining = self.actual_qty
            for index, vals in enumerate(moves_vals):
                if index == len(moves_vals) - 1:
                    new_qty = remaining
                else:
                    new_qty = self.actual_qty * vals.get("product_uom_qty", 0.0) / original_total
                    remaining -= new_qty
                vals["product_uom_qty"] = new_qty

        for vals in moves_vals:
            vals["price_unit"] = self.effective_price_unit
        return moves_vals
