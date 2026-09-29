# -*- coding: utf-8 -*-

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    inter_company_transfer_id = fields.Many2one(
        'stock.inter.company.transfer',
        string='InterCompany Transaction',
        readonly=True,
        copy=False,
    )

    def action_view_inter_company_transfer(self):
        """Open the related inter-company transaction."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.inter.company.transfer',
            'view_mode': 'form',
            'res_id': self.inter_company_transfer_id.id,
        }
