# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    secondary_currency_id = fields.Many2one(
        'res.currency',
        string='Secondary Currency',
        tracking=True,
        help='Currency used for secondary amount reporting.',
    )
    manual_rate = fields.Float(
        string='Rate',
        digits=(16, 6),
        tracking=True,
        help='Manual exchange rate applied to compute secondary amounts.',
    )
    use_manual_rate = fields.Boolean(
        string='Use Manual Rate',
        default=False,
        tracking=True,
    )
    # Secondary Currency Totals (aggregated from line_ids)
    secondary_debit_total = fields.Monetary(
        string='Secondary Debit',
        currency_field='secondary_currency_id',
        compute='_compute_secondary_totals',
        store=True,
        group_operator='sum',
    )
    secondary_credit_total = fields.Monetary(
        string='Secondary Credit',
        currency_field='secondary_currency_id',
        compute='_compute_secondary_totals',
        store=True,
        group_operator='sum',
    )
    secondary_balance_total = fields.Monetary(
        string='Secondary Balance',
        currency_field='secondary_currency_id',
        compute='_compute_secondary_totals',
        store=True,
        group_operator='sum',
    )
    # Patch Number at MOVE LEVEL (header)
    patch_number_id = fields.Many2one(
        'account.patch.number',
        string='Patch Number',
        index=True,
        check_company=True,
        domain="[('company_id', 'in', [False, company_id]), ('active', '=', True)]",
        help='Patch number assigned to this journal entry.',
    )

    @api.depends('line_ids.secondary_debit', 'line_ids.secondary_credit')
    def _compute_secondary_totals(self):
        for move in self:
            lines = move.line_ids.filtered(
                lambda l: l.display_type not in ('line_section', 'line_note')
            )
            move.secondary_debit_total = sum(lines.mapped('secondary_debit'))
            move.secondary_credit_total = sum(lines.mapped('secondary_credit'))
            move.secondary_balance_total = (
                move.secondary_debit_total - move.secondary_credit_total
            )

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        fields = super(AccountMove, self).fields_get(allfields, attributes)
        try:
            sec_currency = self.env.company._get_secondary_currency()
            if sec_currency and sec_currency != self.env.company.currency_id:
                label = (sec_currency.name or sec_currency.symbol).upper()
                for fname, fstring in [
                    ('secondary_debit_total', _('Total (%s)') % label),
                    ('secondary_credit_total', _('Credit (%s)') % label),
                    ('secondary_balance_total', _('Balance (%s)') % label),
                ]:
                    if fname in fields:
                        fields[fname]['string'] = fstring
        except Exception:
            pass
        return fields

    @api.model
    def default_get(self, fields_list):
        """Auto-populate secondary currency from company settings.
        Uses company.secondary_currency_id if set, otherwise auto-detects
        the first active non-primary currency.
        """
        res = super(AccountMove, self).default_get(fields_list)
        company = self.env.company
        sec_currency = company._get_secondary_currency()
        if sec_currency and sec_currency != company.currency_id and 'secondary_currency_id' in fields_list:
            res['secondary_currency_id'] = sec_currency.id
            res['use_manual_rate'] = False
        return res

    @api.onchange('use_manual_rate', 'manual_rate', 'line_ids')
    def _onchange_manual_rate(self):
        for line in self.line_ids:
            line._compute_secondary_amounts()
            line._compute_secondary_balance()

    @api.constrains('manual_rate', 'use_manual_rate')
    def _check_manual_rate(self):
        for move in self:
            if move.use_manual_rate and move.manual_rate <= 0:
                raise ValidationError(_('Manual exchange rate must be greater than zero when enabled.'))

    def _post(self, soft=True):
        result = super(AccountMove, self)._post(soft=soft)
        # Compute secondary amounts AFTER super to ensure
        # stored values persist even if cache is invalidated during posting
        for move in self:
            if move.use_manual_rate and move.manual_rate:
                lines = move.line_ids
                lines._compute_secondary_amounts()
                lines._compute_secondary_balance()
                # Force write to database immediately
                lines.flush_recordset()
        return result
