# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class TrialBalanceReport(models.AbstractModel):
    _name = 'report.advanced_accounting_reports.report_trial_balance'
    _description = 'Trial Balance Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Pre-translated labels for QWeb template
        labels = {
            'trial_balance_report': _('Trial Balance Report'),
            'from_to': _('From: %s To: %s'),
            'from_text': _('From'),
            'to_text': _('To'),
            'opening_balance': _('Opening Balance'),
            'ending_balance': _('Ending Balance'),
            'account': _('Account'),
            'all_accounts': _('All Accounts'),
            'features': _('Features'),
            'cost_centers': _('Cost Centers'),
            'patch_number': _('Patch Number'),
            'date': _('Date'),
            'code': _('Code'),
            'debit': _('Debit'),
            'credit': _('Credit'),
            'balance': _('Balance'),
            'total': _('Total'),
            'period': _('Period'),
            'opening_bal': _('Opening Bal'),
            'ending_bal': _('Ending Bal'),
        }

        # Get wizard for PDF export
        wizard = self.env['trial.balance.wizard'].browse(docids) if docids else False

        if wizard:
            date_from = wizard.date_from
            date_to = wizard.date_to
            company_id = wizard.company_id.id
            show_secondary = wizard.show_secondary_currency
            target_move = wizard.target_move
            journal_ids = wizard.journal_ids.ids
            account_ids = wizard.account_ids.ids or False
            feature_ids = wizard.feature_ids.ids or False
            cost_center_ids = wizard.cost_center_ids.ids or False
        else:
            ctx = self.env.context
            date_from = ctx.get('date_from')
            date_to = ctx.get('date_to')
            company_id = ctx.get('company_id', self.env.company.id)
            show_secondary = ctx.get('show_secondary_currency', True)
            target_move = ctx.get('target_move', 'posted')
            journal_ids = ctx.get('journal_ids', [])
            account_ids = ctx.get('account_ids', False)
            feature_ids = ctx.get('feature_ids', False)
            cost_center_ids = ctx.get('cost_center_ids', False)

        company = self.env['res.company'].browse(company_id)

        def _add_dimension_domain(dom):
            if feature_ids:
                dom.append(('feature_ids', 'in', feature_ids))
            if cost_center_ids:
                dom.append(('cost_center_ids', 'in', cost_center_ids))
            return dom

        # Base domain for period lines
        domain = [
            ('date', '>=', date_from),
            ('date', '<=', date_to),
            ('company_id', '=', company_id),
            ('display_type', 'not in', ['line_section', 'line_note']),
        ]
        if target_move == 'posted':
            domain.append(('parent_state', '=', 'posted'))
        if journal_ids:
            domain.append(('journal_id', 'in', journal_ids))
        if account_ids:
            domain.append(('account_id', 'in', account_ids))
        _add_dimension_domain(domain)

        # Get period totals grouped by account
        period_lines = self.env['account.move.line'].read_group(
            domain,
            ['debit:sum', 'credit:sum', 'balance:sum',
             'secondary_debit:sum', 'secondary_credit:sum', 'secondary_balance:sum'],
            ['account_id'],
            orderby='account_id',
            lazy=False,
        )

        # Build period dict from read_group results
        period_dict = {}
        for line in period_lines:
            acc_id = line['account_id'][0] if line['account_id'] else False
            if acc_id:
                period_dict[acc_id] = {
                    'debit': line['debit'] or 0.0,
                    'credit': line['credit'] or 0.0,
                    'balance': line['balance'] or 0.0,
                    'sec_debit': line['secondary_debit'] or 0.0,
                    'sec_credit': line['secondary_credit'] or 0.0,
                    'sec_balance': line['secondary_balance'] or 0.0,
                }

        # Search all accounts
        accounts = self.env['account.account'].search([])
        account_dict = {a.id: a for a in accounts}

        # Build opening balance domain (before date_from)
        opening_domain = [
            ('date', '<', date_from),
            ('company_id', '=', company_id),
            ('display_type', 'not in', ['line_section', 'line_note']),
        ]
        if target_move == 'posted':
            opening_domain.append(('parent_state', '=', 'posted'))
        if journal_ids:
            opening_domain.append(('journal_id', 'in', journal_ids))
        if account_ids:
            opening_domain.append(('account_id', 'in', account_ids))
        _add_dimension_domain(opening_domain)

        opening_lines = self.env['account.move.line'].read_group(
            opening_domain,
            ['debit:sum', 'credit:sum', 'balance:sum',
             'secondary_debit:sum', 'secondary_credit:sum', 'secondary_balance:sum'],
            ['account_id'],
            orderby='account_id',
            lazy=False,
        )
        opening_dict = {}
        for line in opening_lines:
            acc_id = line['account_id'][0] if line['account_id'] else False
            if acc_id:
                opening_dict[acc_id] = {
                    'debit': line['debit'] or 0.0,
                    'credit': line['credit'] or 0.0,
                    'balance': line['balance'] or 0.0,
                    'sec_debit': line['secondary_debit'] or 0.0,
                    'sec_credit': line['secondary_credit'] or 0.0,
                    'sec_balance': line['secondary_balance'] or 0.0,
                }

        # Combine ALL accounts from both period and opening data
        all_account_ids = set(period_dict.keys()) | set(opening_dict.keys())

        # Get patch numbers from moves in period
        patch_numbers = set()
        rate_domain = [
            ('date', '>=', date_from),
            ('date', '<=', date_to),
            ('company_id', '=', company_id),
            ('move_id.patch_number_id', '!=', False),
        ]
        if target_move == 'posted':
            rate_domain.append(('parent_state', '=', 'posted'))
        if journal_ids:
            rate_domain.append(('journal_id', 'in', journal_ids))
        patch_lines = self.env['account.move.line'].search(rate_domain, limit=100)
        for pl in patch_lines:
            if pl.move_id.patch_number_id:
                patch_numbers.add(pl.move_id.patch_number_id.name)

        report_lines = []
        total_op_debit = 0.0
        total_op_credit = 0.0
        total_op_balance = 0.0
        total_debit = total_credit = total_balance = 0.0
        total_end_debit = 0.0
        total_end_credit = 0.0
        total_end_balance = 0.0
        total_sec_op_debit = 0.0
        total_sec_op_credit = 0.0
        total_sec_op_balance = 0.0
        total_sec_debit = total_sec_credit = total_sec_balance = 0.0
        total_sec_end_debit = 0.0
        total_sec_end_credit = 0.0
        total_sec_end_balance = 0.0

        # Default empty values
        _empty = {
            'debit': 0.0, 'credit': 0.0, 'balance': 0.0,
            'sec_debit': 0.0, 'sec_credit': 0.0, 'sec_balance': 0.0,
        }

        # Iterate over ALL accounts that have either opening or period activity
        for acc_id in sorted(all_account_ids):
            account = account_dict.get(acc_id)
            if not account:
                continue

            op = opening_dict.get(acc_id, _empty)
            per = period_dict.get(acc_id, _empty)

            debit = per['debit']
            credit = per['credit']
            bal = per['balance']
            sec_debit = per['sec_debit']
            sec_credit = per['sec_credit']
            sec_bal = per['sec_balance']

            end_balance = op['balance'] + bal
            end_sec_balance = op['sec_balance'] + sec_bal

            report_lines.append({
                'code': account.with_company(company).sudo().code_store or account.code or '',
                'name': account.name or '',
                'opening_balance': op['balance'],
                'opening_debit': op['debit'],
                'opening_credit': op['credit'],
                'debit': debit,
                'credit': credit,
                'balance': bal,
                'ending_balance': end_balance,
                'ending_debit': op['debit'] + debit,
                'ending_credit': op['credit'] + credit,
                'secondary_debit': sec_debit if show_secondary else 0.0,
                'secondary_credit': sec_credit if show_secondary else 0.0,
                'secondary_balance': sec_bal if show_secondary else 0.0,
                'secondary_opening_balance': op['sec_balance'] if show_secondary else 0.0,
                'secondary_opening_debit': op['sec_debit'] if show_secondary else 0.0,
                'secondary_opening_credit': op['sec_credit'] if show_secondary else 0.0,
                'secondary_ending_balance': end_sec_balance if show_secondary else 0.0,
                'secondary_ending_debit': (op['sec_debit'] + sec_debit) if show_secondary else 0.0,
                'secondary_ending_credit': (op['sec_credit'] + sec_credit) if show_secondary else 0.0,
            })

            # Totals
            total_op_debit += op['debit']
            total_op_credit += op['credit']
            total_op_balance += op['balance']
            total_debit += debit
            total_credit += credit
            total_balance += bal
            total_end_debit += op['debit'] + debit
            total_end_credit += op['credit'] + credit
            total_end_balance += end_balance
            total_sec_op_debit += op['sec_debit']
            total_sec_op_credit += op['sec_credit']
            total_sec_op_balance += op['sec_balance']
            total_sec_debit += sec_debit
            total_sec_credit += sec_credit
            total_sec_balance += sec_bal
            total_sec_end_debit += op['sec_debit'] + sec_debit
            total_sec_end_credit += op['sec_credit'] + sec_credit
            total_sec_end_balance += end_sec_balance

        totals = {
            'op_balance': total_op_balance,
            'op_debit': total_op_debit,
            'op_credit': total_op_credit,
            'debit': total_debit,
            'credit': total_credit,
            'balance': total_balance,
            'end_balance': total_end_balance,
            'end_debit': total_end_debit,
            'end_credit': total_end_credit,
            'sec_op_balance': total_sec_op_balance,
            'sec_op_debit': total_sec_op_debit,
            'sec_op_credit': total_sec_op_credit,
            'sec_debit': total_sec_debit,
            'sec_credit': total_sec_credit,
            'sec_balance': total_sec_balance,
            'sec_end_balance': total_sec_end_balance,
            'sec_end_debit': total_sec_end_debit,
            'sec_end_credit': total_sec_end_credit,
        }

        primary_symbol = company.currency_id.symbol or ''
        sec_currency = company._get_secondary_currency()
        sec_symbol = sec_currency.symbol if sec_currency else ''
        sec_name = sec_currency.name or sec_symbol

        return {
            'doc_ids': docids,
            'doc_model': 'trial.balance.wizard',
            'docs': wizard,
            'lines': report_lines,
            'show_secondary': show_secondary,
            'date_from': date_from,
            'date_to': date_to,
            'company': company,
            'feature_ids': wizard.feature_ids if wizard else False,
            'cost_center_ids': wizard.cost_center_ids if wizard else False,
            'totals': totals,
            'patch_numbers': ', '.join(patch_numbers) if patch_numbers else '',
            'primary_currency_symbol': primary_symbol,
            'secondary_currency_symbol': sec_symbol,
            'secondary_currency_name': sec_name,
            'labels': labels,
        }
