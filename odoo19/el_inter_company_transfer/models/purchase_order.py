# -*- coding: utf-8 -*-

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    inter_company_transfer_id = fields.Many2one(
        'stock.inter.company.transfer',
        string='InterCompany Transaction',
        readonly=True,
        copy=False,
    )
    inter_company_sale_order_id = fields.Many2one(
        'sale.order',
        string='InterCompany Sales Order',
        related='inter_company_transfer_id.sale_order_id',
        readonly=True,
    )

    def button_confirm(self):
        """Trigger an inter-company transaction after standard purchase confirmation."""
        result = super().button_confirm()
        if not self.env.context.get('skip_inter_company_transfer'):
            self._create_inter_company_transaction()
        return result

    def _create_inter_company_transaction(self):
        """Create inter-company transactions for eligible confirmed purchases."""
        Config = self.env['inter.company.config'].sudo()
        Transfer = self.env['stock.inter.company.transfer']
        for order in self:
            if order.inter_company_transfer_id or order.state not in ('purchase', 'done'):
                continue
            config = Config._find_for_purchase(order.company_id, order.partner_id)
            if config:
                Transfer.create_from_purchase_order(order, config)

    def action_view_inter_company_transfer(self):
        """Open the related inter-company transaction."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.inter.company.transfer',
            'view_mode': 'form',
            'res_id': self.inter_company_transfer_id.id,
        }

    def action_view_inter_company_sale_order(self):
        """Open the sale order linked through the inter-company transaction."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.inter_company_sale_order_id.id,
        }
