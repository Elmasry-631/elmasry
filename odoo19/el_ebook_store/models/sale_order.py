from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """When sale order is confirmed:
        1. Find an available code for the e-book
        2. Assign it to the customer
        3. Expire it immediately (one-time use — can never be reused)
        4. Create a permanent library entry for the customer
        5. Send email with the code
        """
        res = super().action_confirm()
        for order in self:
            for line in order.order_line:
                product = line.product_id.product_tmpl_id
                if not product.is_ebook:
                    continue
                # Assign one code per quantity ordered
                for _ in range(int(line.product_uom_qty)):
                    code = self.env['ebook.code'].search([
                        ('product_tmpl_id', '=', product.id),
                        ('state', '=', 'available'),
                    ], limit=1)
                    if code:
                        # Assign to customer
                        code.action_assign_and_expire(order.partner_id.id, order.id)
                        # Expire immediately — this code is DONE, never reused
                        # Create permanent library entry — customer can access forever
                        self.env['ebook.library'].create({
                            'partner_id': order.partner_id.id,
                            'product_tmpl_id': product.id,
                            'code_id': code.id,
                            'order_id': order.id,
                            'state': 'accessible',
                        })
                        # Send email with the code
                        template = self.env.ref(
                            'el_ebook_store.mail_template_ebook_code_delivery',
                            raise_if_not_found=False
                        )
                        if template:
                            template.send_mail(order.id, force_send=False)
        return res
