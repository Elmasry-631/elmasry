"""Sale.order extension — prevent confirming sales with insufficient stock."""

from odoo import models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    """Override action_confirm to check stock before allowing sale."""

    _inherit = 'sale.order'

    def action_confirm(self):
        """Check available stock for each product before confirming the sale.

        For every storable product in the order, check if the available
        quantity at the source location (warehouse stock) is sufficient.
        If not → create alert + send email + raise UserError.

        NO exceptions — even managers cannot bypass.
        """
        for order in self:
            # Get the source location (warehouse stock location)
            warehouse = order.warehouse_id
            if not warehouse:
                continue
            source_location = warehouse.lot_stock_id

            for line in order.order_line:
                product = line.product_id
                if not product:
                    continue
                # Skip services and combos — only check storable (consu/goods)
                if product.type not in ('consu',):
                    continue

                requested_qty = line.product_uom_qty
                if requested_qty <= 0:
                    continue

                # Get available quantity at warehouse stock location
                available_qty = self.env['stock.quant']._get_available_quantity(
                    product,
                    source_location,
                )

                if available_qty < requested_qty:
                    # ─── Create alert record ───
                    alert_vals = {
                        'product_id': product.id,
                        'location_id': source_location.id,
                        'requested_qty': requested_qty,
                        'available_qty': available_qty,
                    }
                    alert = self.env['el.stock.alert'].create(alert_vals)

                    # ─── Send email notification ───
                    template = self.env.ref(
                        'el_prevent_negative_stock.mail_template_negative_stock_alert',
                        raise_if_not_found=False,
                    )
                    if template:
                        template.send_mail(alert.id, force_send=True)

                    # ─── Raise error (block the sale) ───
                    raise UserError(_(
                        '🚫 Sale Blocked — Insufficient Stock!\n\n'
                        'Sales Order: %s\n'
                        'Product: %s\n'
                        'Warehouse: %s\n'
                        'Requested: %s %s\n'
                        'Available: %s %s\n\n'
                        'This sale cannot be confirmed because there is not '
                        'enough stock available.\n\n'
                        'Alert Reference: %s'
                    ) % (
                        order.name,
                        product.display_name,
                        warehouse.name,
                        requested_qty,
                        product.uom_id.name,
                        available_qty,
                        product.uom_id.name,
                        alert.name,
                    ))

        return super().action_confirm()
