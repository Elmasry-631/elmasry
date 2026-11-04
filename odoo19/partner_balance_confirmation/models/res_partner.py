# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_open_balance_confirmation(self):
        """Open the balance confirmation wizard for this partner.

        Returns an act_window action that opens a new wizard record pre-filled
        with the partner_id.
        """
        self.ensure_one()
        # Get the current user's timezone-aware date
        today = fields.Date.context_today(self)
        return {
            'name': _('Balance Confirmation'),
            'type': 'ir.actions.act_window',
            'res_model': 'balance.confirmation.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_partner_id': self.id,
                'default_confirmation_date': today,
                'default_template_type': 'amdad',
                'default_printed_by': self.env.user.id,
            },
        }

    @api.model
    def _get_partner_balance_at_date(self, partner_id, target_date, account_types=None):
        """Compute the partner's receivable balance (debit - credit) up to target_date.

        :param partner_id: res.partner id
        :param target_date: date string or object
        :param account_types: list of account types to include (default: asset_receivable)
        :return: (balance_float, currency_id)
        """
        if account_types is None:
            account_types = ['asset_receivable']

        if not partner_id:
            return 0.0, self.env.company.currency_id

        partner = self.browse(partner_id)
        company = self.env.company
        currency = company.currency_id

        # Build the domain for account.move.line
        domain = [
            ('partner_id', '=', partner_id),
            ('date', '<=', target_date),
            ('parent_state', '=', 'posted'),
            ('account_id.account_type', 'in', account_types),
            ('company_id', '=', company.id),
        ]

        # Use read_group to sum debit and credit
        query_result = self.env['account.move.line'].read_group(
            domain,
            ['debit', 'credit', 'amount_currency'],
            [],
        )
        if query_result:
            total_debit = query_result[0].get('debit', 0.0) or 0.0
            total_credit = query_result[0].get('credit', 0.0) or 0.0
            balance = total_debit - total_credit
        else:
            balance = 0.0

        return balance, currency
