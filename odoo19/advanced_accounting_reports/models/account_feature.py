# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_round, float_is_zero


class AccountFeature(models.Model):
    _name = 'account.feature'
    _description = 'Feature'
    _order = 'code, name'
    _parent_store = True
    _check_company_auto = True

    name = fields.Char(string='Feature', required=True, translate=True)
    code = fields.Char(string='Reference', index=True)
    parent_id = fields.Many2one(
        'account.feature',
        string='Parent Feature',
        index=True,
        ondelete='cascade',
        check_company=True,
    )
    parent_path = fields.Char(index=True, unaccent=False)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)
    notes = fields.Text(string='Notes', translate=True)
    child_ids = fields.One2many('account.feature', 'parent_id', string='Sub Features')

    # Company Currency totals
    debit = fields.Monetary(string='Debit', compute='_compute_debit_credit_balance')
    credit = fields.Monetary(string='Credit', compute='_compute_debit_credit_balance')
    balance = fields.Monetary(string='Balance', compute='_compute_debit_credit_balance')
    currency_id = fields.Many2one('res.currency', compute='_compute_debit_credit_balance')

    # Secondary Currency totals
    secondary_debit = fields.Monetary(string='Secondary Debit', compute='_compute_debit_credit_balance', currency_field='secondary_currency_id')
    secondary_credit = fields.Monetary(string='Secondary Credit', compute='_compute_debit_credit_balance', currency_field='secondary_currency_id')
    secondary_balance = fields.Monetary(string='Secondary Balance', compute='_compute_debit_credit_balance', currency_field='secondary_currency_id')
    secondary_currency_id = fields.Many2one('res.currency', compute='_compute_debit_credit_balance')

    # Average Exchange Rate
    avg_rate = fields.Float(string='Avg. Rate', compute='_compute_debit_credit_balance', digits=(16, 6))

    _sql_constraints = [
        ('code_company_uniq', 'unique(code, company_id)',
         'The code must be unique per company!'),
    ]

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive features.'))

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        fields = super(AccountFeature, self).fields_get(allfields, attributes)
        try:
            company = self.env.company
            sec_currency = company._get_secondary_currency()
            if sec_currency and sec_currency != company.currency_id:
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

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.code:
                name = '[%s] %s' % (record.code, name)
            result.append((record.id, name))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name + '%'), ('name', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    @api.depends('company_id')
    def _compute_debit_credit_balance(self):
        MoveLine = self.env['account.move.line']
        for feature in self:
            company = feature.company_id or self.env.company
            currency = company.currency_id
            feature.debit = 0.0
            feature.credit = 0.0
            feature.balance = 0.0
            feature.currency_id = currency
            feature.secondary_debit = 0.0
            feature.secondary_credit = 0.0
            feature.secondary_balance = 0.0
            feature.secondary_currency_id = False
            feature.avg_rate = 0.0

            try:
                sec_currency = False
                if company.secondary_currency_id:
                    sec_currency = company.secondary_currency_id
                else:
                    sec_currency = self.env['res.currency'].search([
                        ('active', '=', True), ('id', '!=', company.currency_id.id),
                    ], limit=1) or False
                feature.secondary_currency_id = sec_currency
            except Exception:
                pass

            try:
                base = [
                    ('company_id', '=', company.id),
                    ('display_type', 'not in', ['line_section', 'line_note']),
                    ('parent_state', '=', 'posted'),
                    ('feature_ids', '=', feature.id),
                ]

                # Primary currency
                r = MoveLine.read_group(base, ['debit:sum', 'credit:sum'], [], lazy=False)
                dr = (r[0]['debit'] or 0.0) if r else 0.0
                cr = (r[0]['credit'] or 0.0) if r else 0.0
                feature.debit = dr
                feature.credit = cr
                feature.balance = dr - cr

                # Secondary currency
                s = MoveLine.read_group(base, ['secondary_debit:sum', 'secondary_credit:sum'], [], lazy=False)
                sdr = (s[0].get('secondary_debit') or 0.0) if s else 0.0
                scr = (s[0].get('secondary_credit') or 0.0) if s else 0.0
                feature.secondary_debit = sdr
                feature.secondary_credit = scr
                feature.secondary_balance = sdr - scr

                # Avg rate
                rounding = currency.rounding or 0.01
                if not float_is_zero(dr, precision_rounding=rounding) or not float_is_zero(cr, precision_rounding=rounding):
                    tp = dr + cr
                    ts = sdr + scr
                    if not float_is_zero(tp, precision_rounding=rounding):
                        feature.avg_rate = float_round(ts / tp, precision_digits=6)
            except Exception:
                pass
