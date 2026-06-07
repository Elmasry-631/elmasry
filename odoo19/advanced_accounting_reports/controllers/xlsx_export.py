# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request, content_disposition
import io
import xlsxwriter


class XlsxExportController(http.Controller):

    def _get_header_format(self, workbook):
        return workbook.add_format({
            'bold': True, 'bg_color': '#D9D9D9', 'font_color': 'black',
            'align': 'center', 'valign': 'vcenter', 'border': 1,
            'text_wrap': True,
        })

    def _get_title_format(self, workbook):
        return workbook.add_format({
            'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter',
        })

    def _get_number_format(self, workbook):
        return workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'align': 'right'})

    def _get_text_format(self, workbook):
        return workbook.add_format({'border': 1})

    def _get_total_format(self, workbook):
        return workbook.add_format({
            'bold': True, 'bg_color': '#E7E6E6', 'num_format': '#,##0.00', 'border': 1, 'align': 'right',
        })

    def _get_info_format(self, workbook):
        return workbook.add_format({
            'bold': True, 'bg_color': '#f0f0f0', 'border': 1,
        })

    def _get_info_value_format(self, workbook):
        return workbook.add_format({
            'border': 1, 'valign': 'vcenter',
        })

    def _resolve_secondary_currency(self, domain):
        """Get the actual secondary currency from the journal entry lines in the period."""
        sec_currency = request.env['res.currency'].browse()
        # Try from move.secondary_currency_id
        sample = request.env['account.move.line'].search(
            domain + [('move_id.secondary_currency_id', '!=', False)], limit=1
        )
        if sample and sample.move_id.secondary_currency_id:
            sec_currency = sample.move_id.secondary_currency_id
        else:
            # Fallback to company auto-detection
            company = request.env.company
            sec_currency = company._get_secondary_currency()
        return sec_currency

    # =========================================================================
    # GENERAL LEDGER EXCEL EXPORT
    # =========================================================================
    @http.route('/advanced_accounting/export/general_ledger_xlsx', type='http', auth='user')
    def export_general_ledger_xlsx(self, wizard_id, **kw):
        try:
            wizard = request.env['general.ledger.wizard'].browse(int(wizard_id))
            if not wizard.exists():
                return request.not_found()

            domain = wizard._build_domain()
            company = wizard.company_id
            lang = request.env.user.lang or 'en_US'
            is_rtl = lang and lang.startswith('ar')
            show_secondary = wizard.show_secondary_currency

            # Determine currency symbols
            company_currency = company.currency_id
            primary_symbol = company_currency.symbol or ''
            primary_name = company_currency.name or primary_symbol
            sec_currency = self._resolve_secondary_currency(domain)
            sec_symbol = sec_currency.symbol if sec_currency else ''
            sec_name = sec_currency.name or sec_symbol

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet(_('General Ledger'))
            if is_rtl:
                sheet.right_to_left()

            tf = self._get_title_format(workbook)
            nf = self._get_number_format(workbook)
            xf = self._get_text_format(workbook)
            tof = self._get_total_format(workbook)
            infof = self._get_info_format(workbook)
            infovf = self._get_info_value_format(workbook)

            # Calculate column count
            base_cols = 11  # Date, Move, Label, Partner, Account, Features, Cost Centers, Patch, Dr, Cr, Balance
            sec_cols = 3 if show_secondary else 0
            rate_col = 1 if show_secondary else 0
            total_cols = base_cols + sec_cols + rate_col
            last_col = total_cols - 1

            # Title rows - NO duplicate company name
            sheet.merge_range(0, 0, 0, last_col, company.name, tf)
            sheet.merge_range(1, 0, 1, last_col, _('General Ledger Report'), tf)
            sheet.merge_range(2, 0, 2, last_col, _('From: %s To: %s') % (wizard.date_from, wizard.date_to), tf)

            # ---- Info rows ----
            # Row 3: Opening Balance (Primary) | Ending Balance (Primary)
            row_info = 3
            sheet.write(row_info, 0, _('Opening Balance') + ' (' + primary_symbol + ')', infof)
            # Get actual opening balance value (will be written after calculation below)
            mid_col = int(last_col / 2)
            sheet.write(row_info, mid_col, _('Ending Balance') + ' (' + primary_symbol + ')', infof)

            # Row 4: Secondary Opening Balance | Secondary Ending Balance (only if secondary)
            if show_secondary and sec_symbol:
                row_info = 4
                sheet.write(row_info, 0, _('Opening Balance') + ' (' + sec_name + ')', infof)
                sheet.write(row_info, mid_col, _('Ending Balance') + ' (' + sec_name + ')', infof)
                row_info = 5
            else:
                row_info = 4

            # Row: Account info
            account_names = ', '.join(wizard.account_ids.mapped(lambda a: '%s %s' % (a.with_company(company).sudo().code_store or a.code or '', a.name or ''))) if wizard.account_ids else _('All Accounts')
            sheet.write(row_info, 0, _('Account'), infof)
            sheet.merge_range(row_info, 1, row_info, last_col, account_names, infovf)
            row_info += 1

            # Row: Journals
            journal_names = ', '.join(wizard.journal_ids.mapped('name')) if wizard.journal_ids else ''
            sheet.write(row_info, 0, _('Journals'), infof)
            sheet.merge_range(row_info, 1, row_info, last_col, journal_names, infovf)
            row_info += 1

            # ---- Get Opening Balance ----
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
            if wizard.partner_ids:
                opening_domain.append(('partner_id', 'in', wizard.partner_ids.ids))
            if wizard.feature_ids:
                opening_domain.append(('feature_ids', 'in', wizard.feature_ids.ids))
            if wizard.cost_center_ids:
                opening_domain.append(('cost_center_ids', 'in', wizard.cost_center_ids.ids))

            opening_data = request.env['account.move.line'].read_group(
                opening_domain,
                ['balance:sum', 'secondary_balance:sum'],
                [],
                lazy=False,
            )
            opening_balance = opening_data[0]['balance'] if opening_data else 0.0
            opening_sec_balance = opening_data[0]['secondary_balance'] if opening_data else 0.0

            # Write Opening Balance values (primary)
            sheet.write(3, 1, round(opening_balance, 2), nf)
            # Write Opening/Ending secondary balance values
            if show_secondary and sec_symbol:
                sheet.write(4, 1, round(opening_sec_balance, 2), nf)

            # ---- Headers ----
            header_row = row_info
            col = 0
            sheet.write(header_row, col, _('Date'), infof); col += 1
            sheet.write(header_row, col, _('Move'), infof); col += 1
            sheet.write(header_row, col, _('Label'), infof); col += 1
            sheet.write(header_row, col, _('Partner'), infof); col += 1
            sheet.write(header_row, col, _('Account'), infof); col += 1
            sheet.write(header_row, col, _('Features'), infof); col += 1
            sheet.write(header_row, col, _('Cost Centers'), infof); col += 1
            sheet.write(header_row, col, _('Patch Number'), infof); col += 1
            sheet.write(header_row, col, _('Debit') + ' (' + primary_symbol + ')', infof); col += 1
            sheet.write(header_row, col, _('Credit') + ' (' + primary_symbol + ')', infof); col += 1
            sheet.write(header_row, col, _('Balance') + ' (' + primary_symbol + ')', infof); col += 1
            if show_secondary:
                sheet.write(header_row, col, _('Debit') + ' (' + sec_name + ')', infof); col += 1
                sheet.write(header_row, col, _('Credit') + ' (' + sec_name + ')', infof); col += 1
                sheet.write(header_row, col, _('Balance') + ' (' + sec_name + ')', infof); col += 1
                sheet.write(header_row, col, _('Rate'), infof); col += 1

            # ---- Data rows ----
            lines = request.env['account.move.line'].search(domain, order='date, move_id, id')
            row = header_row + 1
            running_balance = opening_balance
            running_sec_balance = opening_sec_balance
            total_debit = total_credit = total_sec_debit = total_sec_credit = 0.0

            for line in lines:
                running_balance += line.balance
                running_sec_balance += line.secondary_balance
                total_debit += line.debit
                total_credit += line.credit
                total_sec_debit += line.secondary_debit
                total_sec_credit += line.secondary_credit

                col = 0
                sheet.write(row, col, str(line.date), xf); col += 1
                sheet.write(row, col, line.move_id.name or '', xf); col += 1
                sheet.write(row, col, line.name or '', xf); col += 1
                sheet.write(row, col, line.partner_id.name or '', xf); col += 1
                acode = (line.account_id.with_company(company).sudo().code_store or line.account_id.code or '') if line.account_id else ''
                sheet.write(row, col, '%s %s' % (acode, line.account_id.name or '') if line.account_id else '', xf); col += 1
                sheet.write(row, col, ', '.join(line.feature_ids.mapped('name')) if line.feature_ids else '', xf); col += 1
                sheet.write(row, col, ', '.join(line.cost_center_ids.mapped('name')) if line.cost_center_ids else '', xf); col += 1
                sheet.write(row, col, line.move_id.patch_number_id.name or '', xf); col += 1
                sheet.write(row, col, line.debit, nf); col += 1
                sheet.write(row, col, line.credit, nf); col += 1
                sheet.write(row, col, running_balance, nf); col += 1
                if show_secondary:
                    sheet.write(row, col, line.secondary_debit, nf); col += 1
                    sheet.write(row, col, line.secondary_credit, nf); col += 1
                    sheet.write(row, col, running_sec_balance, nf); col += 1
                    rate = line.manual_rate if line.manual_rate else 0.0
                    sheet.write(row, col, rate if rate else '', nf); col += 1
                row += 1

            # Write Ending Balance values
            ending_balance = running_balance
            ending_sec_balance = running_sec_balance
            sheet.write(3, mid_col + 1, round(ending_balance, 2), nf)
            if show_secondary and sec_symbol:
                sheet.write(4, mid_col + 1, round(ending_sec_balance, 2), nf)

            # ---- Total row ----
            col = 0
            sheet.write(row, col, _('Total'), tof); col += 1
            sheet.write(row, col, '', tof); col += 1  # Move
            sheet.write(row, col, '', tof); col += 1  # Label
            sheet.write(row, col, '', tof); col += 1  # Partner
            sheet.write(row, col, '', tof); col += 1  # Account
            sheet.write(row, col, '', tof); col += 1  # Features
            sheet.write(row, col, '', tof); col += 1  # Cost Centers
            sheet.write(row, col, '', tof); col += 1  # Patch Number
            sheet.write(row, col, total_debit, tof); col += 1
            sheet.write(row, col, total_credit, tof); col += 1
            sheet.write(row, col, ending_balance, tof); col += 1
            if show_secondary:
                sheet.write(row, col, total_sec_debit, tof); col += 1
                sheet.write(row, col, total_sec_credit, tof); col += 1
                sheet.write(row, col, ending_sec_balance, tof); col += 1
                sheet.write(row, col, '', tof); col += 1  # No total for Rate

            # Set column widths
            sheet.set_column(0, 0, 14)   # Date
            sheet.set_column(1, 1, 18)   # Move
            sheet.set_column(2, 2, 25)   # Label
            sheet.set_column(3, 3, 20)   # Partner
            sheet.set_column(4, 4, 25)   # Account
            sheet.set_column(5, 7, 16)   # Features/Cost Centers/Patch
            sheet.set_column(8, 10, 16)  # Dr/Cr/Bal
            if show_secondary:
                sheet.set_column(11, 13, 16)  # Sec Dr/Cr/Bal
                sheet.set_column(14, 14, 14)  # Rate

            workbook.close()
            output.seek(0)
            filename = 'General_Ledger_%s_%s.xlsx' % (wizard.date_from, wizard.date_to)
            return request.make_response(
                output.read(),
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    ('Content-Disposition', content_disposition(filename)),
                ]
            )
        except Exception as e:
            import traceback
            error_msg = str(e) + "\n" + traceback.format_exc()
            return request.make_response(
                error_msg.encode('utf-8'),
                headers=[('Content-Type', 'text/plain')],
                status=500
            )

    # =========================================================================
    # TRIAL BALANCE EXCEL EXPORT
    # =========================================================================
    @http.route('/advanced_accounting/export/trial_balance_xlsx', type='http', auth='user')
    def export_trial_balance_xlsx(self, wizard_id, **kw):
        try:
            wizard = request.env['trial.balance.wizard'].browse(int(wizard_id))
            if not wizard.exists():
                return request.not_found()

            show_secondary = wizard.show_secondary_currency
            company = wizard.company_id
            lang = request.env.user.lang or 'en_US'
            is_rtl = lang and lang.startswith('ar')
            date_from = wizard.date_from
            date_to = wizard.date_to
            company_id = wizard.company_id.id
            target_move = wizard.target_move

            # Determine currency symbols
            company_currency = company.currency_id
            primary_symbol = company_currency.symbol or ''
            primary_name = company_currency.name or primary_symbol
            sec_currency = company._get_secondary_currency()
            sec_symbol = sec_currency.symbol if sec_currency else ''
            sec_name = sec_currency.name or sec_symbol

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet(_('Trial Balance'))
            if is_rtl:
                sheet.right_to_left()

            tf = self._get_title_format(workbook)
            nf = self._get_number_format(workbook)
            xf = self._get_text_format(workbook)
            tof = self._get_total_format(workbook)
            infof = self._get_info_format(workbook)
            infovf = self._get_info_value_format(workbook)

            # Column layout - PRIMARY CURRENCY ONLY (no secondary, no rate):
            # Account Number, Account Name, Opening Dr/Cr/Bal, Period Dr/Cr, Ending Dr/Cr/Bal = 10 cols
            total_cols = 10
            last_col = total_cols - 1

            # Title rows
            sheet.merge_range(0, 0, 0, last_col, company.name, tf)
            sheet.merge_range(1, 0, 1, last_col, _('Trial Balance Report'), tf)
            sheet.merge_range(2, 0, 2, last_col, _('From: %s To: %s') % (date_from, date_to), tf)

            # Get report data (always pass show_secondary=False for TB export)
            ctx = {
                'date_from': date_from,
                'date_to': date_to,
                'journal_ids': wizard.journal_ids.ids,
                'account_ids': wizard.account_ids.ids or False,
                'feature_ids': wizard.feature_ids.ids or False,
                'cost_center_ids': wizard.cost_center_ids.ids or False,
                'target_move': target_move,
                'company_id': company_id,
                'show_secondary_currency': False,
            }
            report = request.env['report.advanced_accounting_reports.report_trial_balance']
            report_data = report.with_context(**ctx)._get_report_values([], data={})
            lines = report_data['lines']
            total_vals = report_data.get('totals', {})

            # ---- 2-Row Headers ----
            # Row 3: Group headers (Opening Bal, Current Period, Ending Bal)
            group_row = 3
            col = 2  # Start after Account Number & Account Name

            # Opening Bal ($)
            sheet.merge_range(group_row, col, group_row, col + 2, _('Opening Bal') + ' (' + primary_symbol + ')', infof)
            col += 3
            # Current Period ($)
            sheet.merge_range(group_row, col, group_row, col + 1, _('Current Period') + ' (' + primary_symbol + ')', infof)
            col += 2
            # Ending Bal ($)
            sheet.merge_range(group_row, col, group_row, col + 2, _('Ending Bal') + ' (' + primary_symbol + ')', infof)

            # Row 4: Detail headers
            header_row = 4
            col = 0
            sheet.write(header_row, col, _('Account Number'), infof); col += 1
            sheet.write(header_row, col, _('Account Name'), infof); col += 1
            # Opening Bal
            sheet.write(header_row, col, _('Dr') + ' (' + primary_symbol + ')', infof); col += 1
            sheet.write(header_row, col, _('Cr') + ' (' + primary_symbol + ')', infof); col += 1
            sheet.write(header_row, col, _('Bal') + ' (' + primary_symbol + ')', infof); col += 1
            # Current Period
            sheet.write(header_row, col, _('Dr') + ' (' + primary_symbol + ')', infof); col += 1
            sheet.write(header_row, col, _('Cr') + ' (' + primary_symbol + ')', infof); col += 1
            # Ending Bal
            sheet.write(header_row, col, _('Dr') + ' (' + primary_symbol + ')', infof); col += 1
            sheet.write(header_row, col, _('Cr') + ' (' + primary_symbol + ')', infof); col += 1
            sheet.write(header_row, col, _('Bal') + ' (' + primary_symbol + ')', infof)

            # ---- Data rows ----
            row = header_row + 1

            for line in lines:
                col = 0
                sheet.write(row, col, line['code'], xf); col += 1
                sheet.write(row, col, line['name'], xf); col += 1
                # Opening Bal
                sheet.write(row, col, line.get('opening_debit', 0.0), nf); col += 1
                sheet.write(row, col, line.get('opening_credit', 0.0), nf); col += 1
                sheet.write(row, col, line['opening_balance'], nf); col += 1
                # Current Period
                sheet.write(row, col, line['debit'], nf); col += 1
                sheet.write(row, col, line['credit'], nf); col += 1
                # Ending Bal
                sheet.write(row, col, line.get('ending_debit', 0.0), nf); col += 1
                sheet.write(row, col, line.get('ending_credit', 0.0), nf); col += 1
                sheet.write(row, col, line['ending_balance'], nf)
                row += 1

            # ---- Total row ----
            col = 0
            sheet.write(row, col, '', tof); col += 1  # Account Number
            sheet.write(row, col, _('Total'), tof); col += 1  # Account Name
            # Opening Bal totals
            sheet.write(row, col, total_vals.get('op_debit', 0.0), tof); col += 1
            sheet.write(row, col, total_vals.get('op_credit', 0.0), tof); col += 1
            sheet.write(row, col, total_vals.get('op_balance', 0.0), tof); col += 1
            # Current Period totals
            sheet.write(row, col, total_vals.get('debit', 0.0), tof); col += 1
            sheet.write(row, col, total_vals.get('credit', 0.0), tof); col += 1
            # Ending Bal totals
            sheet.write(row, col, total_vals.get('end_debit', 0.0), tof); col += 1
            sheet.write(row, col, total_vals.get('end_credit', 0.0), tof); col += 1
            sheet.write(row, col, total_vals.get('end_balance', 0.0), tof)

            # Set column widths
            sheet.set_column(0, 0, 14)   # Account Number
            sheet.set_column(1, 1, 30)   # Account Name
            for c in range(2, total_cols):
                sheet.set_column(c, c, 16)

            workbook.close()
            output.seek(0)
            filename = 'Trial_Balance_%s_%s.xlsx' % (date_from, date_to)
            return request.make_response(
                output.read(),
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    ('Content-Disposition', content_disposition(filename)),
                ]
            )
        except Exception as e:
            import traceback
            error_msg = str(e) + "\n" + traceback.format_exc()
            return request.make_response(
                error_msg.encode('utf-8'),
                headers=[('Content-Type', 'text/plain')],
                status=500
            )
