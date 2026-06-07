# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class GeneralLedgerReport(models.AbstractModel):
    _name = 'report.advanced_accounting_reports.report_general_ledger'
    _description = 'General Ledger Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Pre-translated labels for QWeb template
        labels = {
            'general_ledger_report': _('General Ledger Report'),
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
            'journals': _('Journals'),
            'date': _('Date'),
            'move': _('Move'),
            'label': _('Label'),
            'partner': _('Partner'),
            'debit': _('Debit'),
            'credit': _('Credit'),
            'balance': _('Balance'),
            'rate': _('Rate'),
            'total': _('Total'),
        }

        if not docids:
            return {
                'lines': [],
                'show_secondary': False,
                'company': self.env.company,
                'date_from': '',
                'date_to': '',
                'opening_balance': 0.0,
                'ending_balance': 0.0,
                'totals': {},
                'patch_numbers': '',
                'primary_currency_symbol': '',
                'secondary_currency_symbol': '',
                'labels': labels,
            }

        wizard = self.env['general.ledger.wizard'].browse(docids[0])
        domain = wizard._build_domain()
        show_secondary = wizard.show_secondary_currency
        date_from = wizard.date_from
        date_to = wizard.date_to
        company_id = wizard.company_id.id

        # Get all lines in period
        docs = self.env['account.move.line'].search(domain, order='date, move_id, id')

        # Get opening balance (before date_from)
        opening_domain = [
            ('date', '<', date_from),
            ('company_id', '=', company_id),
            ('display_type', 'not in', ['line_section', 'line_note']),
        ]
        if wizard.target_move == 'posted':
            opening_domain.append(('parent_state', '=', 'posted'))
        if wizard.journal_ids:
            opening_domain.append(('journal_id', 'in', wizard.journal_ids.ids))
        if wizard.account_ids:
            opening_domain.append(('account_id', 'in', wizard.account_ids.ids))
        if wizard.partner_ids:
            opening_domain.append(('partner_id', 'in', wizard.partner_ids.ids))
        if wizard.feature_ids:
            opening_domain.append(('feature_ids', 'in', wizard.feature_ids.ids))
        if wizard.cost_center_ids:
            opening_domain.append(('cost_center_ids', 'in', wizard.cost_center_ids.ids))

        opening_lines = self.env['account.move.line'].read_group(
            opening_domain,
            ['balance:sum', 'secondary_balance:sum'],
            [],
            lazy=False,
        )
        opening_balance = opening_lines[0]['balance'] if opening_lines else 0.0
        opening_sec_balance = opening_lines[0]['secondary_balance'] if opening_lines else 0.0

        # Get patch numbers from moves in period
        patch_numbers = set()
        for line in docs:
            if line.move_id.patch_number_id:
                patch_numbers.add(line.move_id.patch_number_id.name)

        lines = []
        running_balance = opening_balance
        running_sec_balance = opening_sec_balance
        total_debit = total_credit = total_sec_debit = total_sec_credit = 0.0

        for line in docs:
            running_balance += line.balance
            running_sec_balance += line.secondary_balance
            total_debit += line.debit
            total_credit += line.credit
            total_sec_debit += line.secondary_debit
            total_sec_credit += line.secondary_credit

            # Account display: code + name
            account_display = ''
            if line.account_id:
                acode = line.account_id.with_company(wizard.company_id).sudo().code_store or line.account_id.code or ''
                account_display = '%s %s' % (acode, line.account_id.name or '')

            lines.append({
                'date': line.date,
                'journal': line.journal_id.name or '',
                'move': line.move_id.name or '',
                'label': line.name or '',
                'partner': line.partner_id.name or '',
                'account': account_display,
                'features': ', '.join(line.feature_ids.mapped('name')) if line.feature_ids else '',
                'cost_centers': ', '.join(line.cost_center_ids.mapped('name')) if line.cost_center_ids else '',
                'patch_number': line.move_id.patch_number_id.name or '',
                'debit': line.debit,
                'credit': line.credit,
                'balance': running_balance,
                'secondary_debit': line.secondary_debit if show_secondary else 0.0,
                'secondary_credit': line.secondary_credit if show_secondary else 0.0,
                'secondary_balance': running_sec_balance if show_secondary else 0.0,
                'rate': line.manual_rate or 0.0,
            })

        ending_balance = running_balance
        ending_sec_balance = running_sec_balance

        totals = {
            'debit': total_debit,
            'credit': total_credit,
            'balance': ending_balance,
            'sec_debit': total_sec_debit,
            'sec_credit': total_sec_credit,
            'sec_balance': ending_sec_balance,
        }

        company = wizard.company_id
        primary_symbol = company.currency_id.symbol or ''
        primary_name = company.currency_id.name or primary_symbol
        # Resolve secondary currency using auto-detection
        sec_currency = self.env['res.currency'].browse()
        sample = self.env['account.move.line'].search(
            domain + [('move_id.secondary_currency_id', '!=', False)], limit=1
        )
        if sample and sample.move_id.secondary_currency_id:
            sec_currency = sample.move_id.secondary_currency_id
        else:
            sec_currency = company._get_secondary_currency()
        sec_symbol = sec_currency.symbol if sec_currency else ''
        sec_name = sec_currency.name or sec_symbol

        # Journal names
        journal_names = ', '.join(wizard.journal_ids.mapped('name')) if wizard.journal_ids else ''
        # Account names
        account_names = ', '.join(wizard.account_ids.mapped(lambda a: '%s %s' % (a.with_company(wizard.company_id).sudo().code_store or a.code or '', a.name or ''))) if wizard.account_ids else ''

        return {
            'doc_ids': docids,
            'doc_model': 'general.ledger.wizard',
            'docs': wizard,
            'lines': lines,
            'show_secondary': show_secondary,
            'company': company,
            'date_from': date_from,
            'date_to': date_to,
            'feature_ids': wizard.feature_ids,
            'cost_center_ids': wizard.cost_center_ids,
            'opening_balance': opening_balance,
            'ending_balance': ending_balance,
            'secondary_opening_balance': opening_sec_balance if show_secondary else 0.0,
            'secondary_ending_balance': ending_sec_balance if show_secondary else 0.0,
            'totals': totals,
            'patch_numbers': ', '.join(patch_numbers) if patch_numbers else '',
            'primary_currency_symbol': primary_symbol,
            'secondary_currency_symbol': sec_symbol,
            'secondary_currency_name': sec_name,
            'journal_names': journal_names,
            'account_names': account_names,
            'labels': labels,
        }
