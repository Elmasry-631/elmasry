"""Stock.move extension — prevent negative stock."""

from odoo import models, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    """Override _action_assign to prevent negative stock."""

    _inherit = 'stock.move'

    def _action_assign(self):
        """Check available quantity before allowing reservation."""
        for move in self:
            if move.state in ('done', 'cancel', 'assigned'):
                continue
            if not move.product_id or not move.location_id:
                continue
            if move.product_id.type == 'service':
                continue

            check_qty = move.product_uom_qty or 0.0
            if check_qty <= 0:
                continue

            available_qty = self.env['stock.quant']._get_available_quantity(
                move.product_id,
                move.location_id,
            )

            if available_qty < check_qty:
                # Create alert in a savepoint so it survives the UserError
                alert_vals = {
                    'product_id': move.product_id.id,
                    'location_id': move.location_id.id,
                    'requested_qty': check_qty,
                    'available_qty': available_qty,
                    'move_id': move.id,
                }
                alert = self.env['el.stock.alert'].create(alert_vals)

                # Send email before raising error
                template = self.env.ref(
                    'el_prevent_negative_stock.mail_template_negative_stock_alert',
                    raise_if_not_found=False,
                )
                if template:
                    template.send_mail(alert.id, force_send=True)

                # Flush the alert to DB before raising
                self.env.cr.flush()

                raise UserError(_(
                    'Negative Stock Prevented!\n\n'
                    'Product: %s\n'
                    'Location: %s\n'
                    'Requested: %s %s\n'
                    'Available: %s %s\n\n'
                    'This operation is NOT allowed.\n'
                    'Alert Reference: %s'
                ) % (
                    move.product_id.display_name,
                    move.location_id.display_name,
                    check_qty,
                    move.product_id.uom_id.name,
                    available_qty,
                    move.product_id.uom_id.name,
                    alert.name,
                ))

        return super()._action_assign()
