# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    secondary_currency_id = fields.Many2one(
        'res.currency',
        string='Default Secondary Currency',
        help='Default secondary currency for reporting purposes.',
    )

    def _get_secondary_currency(self):
        """Get the company's secondary currency.
        Returns company.secondary_currency_id if set,
        otherwise auto-detects the first active non-primary currency.
        """
        self.ensure_one()
        if self.secondary_currency_id:
            return self.secondary_currency_id
        # Auto-detect: first active currency that is not the primary
        other_currencies = self.env['res.currency'].search([
            ('active', '=', True),
            ('id', '!=', self.currency_id.id),
        ], limit=1, order='name')
        return other_currencies or self.env['res.currency']
