from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    actual_qty_allow_over = fields.Boolean(
        string="Allow Actual Quantity Above Ordered Quantity",
        config_parameter="el_purchase_actual_qty.allow_actual_over_ordered",
    )
    variance_warning_percent = fields.Float(
        string="Variance Warning %",
        default=5.0,
        config_parameter="el_purchase_actual_qty.variance_warning_percent",
    )
    variance_critical_percent = fields.Float(
        string="Variance Critical %",
        default=10.0,
        config_parameter="el_purchase_actual_qty.variance_critical_percent",
    )
    actual_qty_required = fields.Boolean(
        string="Require Actual Quantity",
        default=True,
        config_parameter="el_purchase_actual_qty.actual_qty_required",
    )
