# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    inter_company_transfer_id = fields.Many2one(
        'stock.inter.company.transfer',
        string='InterCompany Transaction',
        readonly=True,
        copy=False,
    )
    inter_company_purchase_order_id = fields.Many2one(
        'purchase.order',
        string='InterCompany Purchase Order',
        related='inter_company_transfer_id.purchase_order_id',
        readonly=True,
    )

    def action_confirm(self):
        """Trigger an inter-company transaction after standard sale confirmation."""
        result = super().action_confirm()
        if not self.env.context.get('skip_inter_company_transfer'):
            self._create_inter_company_transaction()
        return result

    def _create_inter_company_transaction(self):
        """Create inter-company transactions for eligible confirmed sales."""
        Config = self.env['inter.company.config'].sudo()
        Transfer = self.env['stock.inter.company.transfer']
        for order in self:
            if order.inter_company_transfer_id or order.state not in ('sale', 'done'):
                continue
            config = Config._find_for_sale(order.company_id, order.partner_id)
            if config:
                Transfer.create_from_sale_order(order, config)

    def action_view_inter_company_transfer(self):
        """Open the related inter-company transaction."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.inter.company.transfer',
            'view_mode': 'form',
            'res_id': self.inter_company_transfer_id.id,
        }

    def action_view_inter_company_purchase_order(self):
        """Open the purchase order linked through the inter-company transaction."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': self.inter_company_purchase_order_id.id,
        }
