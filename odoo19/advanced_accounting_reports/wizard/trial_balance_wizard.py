# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TrialBalanceWizard(models.TransientModel):
    _name = 'trial.balance.wizard'
    _description = 'Trial Balance Report Wizard'

    date_from = fields.Date(string='Start Date', required=True, default=lambda self: fields.Date.today().replace(day=1))
    date_to = fields.Date(string='End Date', required=True, default=lambda self: fields.Date.today())
    journal_ids = fields.Many2many(
        'account.journal',
        string='Journals',
        required=True,
        default=lambda self: self.env['account.journal'].search([('company_id', '=', self.env.company.id)]),
    )
    account_ids = fields.Many2many('account.account', string='Accounts')
    feature_ids = fields.Many2many('account.feature', string='Features')
    cost_center_ids = fields.Many2many('account.cost.center', string='Cost Centers')
    target_move = fields.Selection([
        ('posted', 'Posted Entries Only'),
        ('all', 'All Entries'),
    ], string='Target Moves', required=True, default='posted')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
    )
    show_secondary_currency = fields.Boolean(string='Show Secondary Currency', default=True)

    # Computed opening/ending balances
    opening_balance = fields.Monetary(string='Opening Balance', compute='_compute_balances', store=False)
    ending_balance = fields.Monetary(string='Ending Balance', compute='_compute_balances', store=False)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            self.journal_ids = self.env['account.journal'].search([('company_id', '=', self.company_id.id)])

    def _add_dimension_domain(self, domain):
        """Add feature/cost center filters to domain."""
        if self.feature_ids:
            domain.append(('feature_ids', 'in', self.feature_ids.ids))
        if self.cost_center_ids:
            domain.append(('cost_center_ids', 'in', self.cost_center_ids.ids))
        return domain

    @api.depends('date_from', 'date_to', 'journal_ids', 'account_ids', 'feature_ids', 'cost_center_ids', 'target_move', 'company_id')
    def _compute_balances(self):
        for wizard in self:
            if not wizard.date_from or not wizard.company_id:
                wizard.opening_balance = 0.0
                wizard.ending_balance = 0.0
                continue

            # Opening balance
            opening_domain = [
                ('date', '<', wizard.date_from),
                ('company_id', '=', wizard.company_id.id),
                ('display_type', 'not in', ['line_section', 'line_note']),
            ]
            if wizard.target_move == 'posted':
                opening_domain.append(('parent_state', '=', 'posted'))
            if wizard.journal_ids:
                opening_domain.append(('journal_id', 'in', wizard.journal_ids.ids))
            if wizard.account_ids:
                opening_domain.append(('account_id', 'in', wizard.account_ids.ids))
            wizard._add_dimension_domain(opening_domain)

            opening = self.env['account.move.line'].read_group(opening_domain, ['balance:sum'], [], lazy=False)
            op_bal = opening[0]['balance'] if opening else 0.0

            # Period balance
            period_domain = [
                ('date', '>=', wizard.date_from),
                ('date', '<=', wizard.date_to),
                ('company_id', '=', wizard.company_id.id),
                ('display_type', 'not in', ['line_section', 'line_note']),
            ]
            if wizard.target_move == 'posted':
                period_domain.append(('parent_state', '=', 'posted'))
            if wizard.journal_ids:
                period_domain.append(('journal_id', 'in', wizard.journal_ids.ids))
            if wizard.account_ids:
                period_domain.append(('account_id', 'in', wizard.account_ids.ids))
            wizard._add_dimension_domain(period_domain)

            period = self.env['account.move.line'].read_group(period_domain, ['balance:sum'], [], lazy=False)
            per_bal = period[0]['balance'] if period else 0.0

            wizard.opening_balance = op_bal
            wizard.ending_balance = op_bal + per_bal

    def action_view_report(self):
        self.ensure_one()
        if self.date_from > self.date_to:
            raise UserError(_('Start Date must be before End Date.'))

        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('journal_id', 'in', self.journal_ids.ids),
            ('company_id', '=', self.company_id.id),
            ('display_type', 'not in', ['line_section', 'line_note']),
        ]
        if self.target_move == 'posted':
            domain.append(('parent_state', '=', 'posted'))
        if self.account_ids:
            domain.append(('account_id', 'in', self.account_ids.ids))
        self._add_dimension_domain(domain)

        return {
            'type': 'ir.actions.act_window',
            'name': _('Trial Balance'),
            'res_model': 'account.move.line',
            'view_mode': 'list,pivot,graph',
            'domain': domain,
            'context': dict(self.env.context, **{
                'date_from': self.date_from,
                'date_to': self.date_to,
                'show_secondary_currency': self.show_secondary_currency,
                'search_default_groupby_account': True,
            }),
            'search_view_id': self.env.ref('advanced_accounting_reports.view_trial_balance_report_search').id,
            'views': [
                (self.env.ref('advanced_accounting_reports.view_trial_balance_report_list').id, 'list'),
            ],
        }

    def action_export_excel(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/advanced_accounting/export/trial_balance_xlsx?wizard_id=%s' % self.id,
            'target': 'self',
        }

    def action_export_pdf(self):
        self.ensure_one()
        return self.env.ref('advanced_accounting_reports.action_report_trial_balance_pdf').report_action(self)
