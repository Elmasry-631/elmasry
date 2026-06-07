# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools import float_round


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # === Features: Many2many (multi-select on journal line) ===
    feature_ids = fields.Many2many(
        'account.feature',
        'account_move_line_feature_rel',
        'move_line_id',
        'feature_id',
        string='Features',
        check_company=True,
        domain="[('company_id', 'in', [False, company_id]), ('active', '=', True)]",
    )

    # === Cost Centers: Many2many (multi-select on journal line) ===
    cost_center_ids = fields.Many2many(
        'account.cost.center',
        'account_move_line_cost_center_rel',
        'move_line_id',
        'cost_center_id',
        string='Cost Centers',
        check_company=True,
        domain="[('company_id', 'in', [False, company_id]), ('active', '=', True)]",
    )

    # === Secondary Currency ===
    secondary_debit = fields.Monetary(
        string='Debit',
        currency_field='secondary_currency_id',
        compute='_compute_secondary_amounts',
        store=True,
        readonly=False,
        group_operator='sum',
    )
    secondary_credit = fields.Monetary(
        string='Credit',
        currency_field='secondary_currency_id',
        compute='_compute_secondary_amounts',
        store=True,
        readonly=False,
        group_operator='sum',
    )
    secondary_balance = fields.Monetary(
        string='Balance',
        currency_field='secondary_currency_id',
        compute='_compute_secondary_balance',
        store=True,
        group_operator='sum',
    )
    secondary_currency_id = fields.Many2one(
        related='move_id.secondary_currency_id',
        string='Secondary Currency',
        store=True,
        readonly=True,
    )
    manual_rate = fields.Float(
        string='Rate',
        related='move_id.manual_rate',
        store=True,
        readonly=True,
        digits=(16, 6),
    )
    patch_number_id = fields.Many2one(
        related='move_id.patch_number_id',
        string='Patch Number',
        store=True,
        readonly=True,
    )
    secondary_currency_name = fields.Char(
        string='Secondary Currency Name',
        compute='_compute_secondary_currency_symbol',
    )

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        fields = super(AccountMoveLine, self).fields_get(allfields, attributes)
        try:
            sec_currency = self.env.company._get_secondary_currency()
            if sec_currency and sec_currency != self.env.company.currency_id:
                label = (sec_currency.name or sec_currency.symbol).upper()
                for fname, fstring in [
                    ('secondary_debit', _('Debit (%s)') % label),
                    ('secondary_credit', _('Credit (%s)') % label),
                    ('secondary_balance', _('Balance (%s)') % label),
                ]:
                    if fname in fields:
                        fields[fname]['string'] = fstring
        except Exception:
            pass
        return fields

    @api.depends('secondary_currency_id')
    def _compute_secondary_currency_symbol(self):
        for line in self:
            if line.secondary_currency_id:
                line.secondary_currency_name = line.secondary_currency_id.name or line.secondary_currency_id.symbol
            else:
                line.secondary_currency_name = ''

    @api.depends('debit', 'credit', 'move_id.manual_rate', 'move_id.use_manual_rate')
    def _compute_secondary_amounts(self):
        for line in self:
            move = line.move_id
            if move.use_manual_rate and move.manual_rate and move.secondary_currency_id:
                rate = move.manual_rate
                sec_debit = float_round(line.debit * rate, precision_rounding=move.secondary_currency_id.rounding)
                sec_credit = float_round(line.credit * rate, precision_rounding=move.secondary_currency_id.rounding)
                line.secondary_debit = sec_debit
                line.secondary_credit = sec_credit
            else:
                line.secondary_debit = 0.0
                line.secondary_credit = 0.0

    @api.depends('secondary_debit', 'secondary_credit')
    def _compute_secondary_balance(self):
        for line in self:
            line.secondary_balance = (line.secondary_debit or 0.0) - (line.secondary_credit or 0.0)
