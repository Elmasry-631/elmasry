import base64
import csv
import io
from collections import OrderedDict

import xlsxwriter
from markupsafe import Markup, escape

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round

# Columns of the bank salary file ("ملف رواتب البنك"), in this exact order.
HEADERS = [
    'البنك', 'رقم الحساب', 'إجمالي الراتب', 'ملاحظات', 'اسم الموظف', 'رقم الهوية أو الإقامة',
    'عنوان الموظف', 'الراتب الأساسي', 'بدل سكن', 'بدلات أخرى', 'خصومات',
]
COLUMN_WIDTHS = {0: 5.75, 1: 25.5, 4: 26.75, 5: 14.5, 6: 11.0, 7: 11.75}
# Columns of the CSV bank file, as in the CSV file the bank already receives.
CSV_HEADERS = [
    'Bank', 'Account', 'Salary(total)', 'Notice(month)', 'Name', 'ID number',
    'address', 'wage', 'house', 'Others', 'discount',
]
# English month names, whatever the language and locale of the server.
MONTH_NAMES = (
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
)


class WpsExportWizard(models.TransientModel):
    _name = 'wps.export.wizard'
    _description = 'WPS Payroll Bank File Export'

    month = fields.Date(
        string='Month',
        required=True,
        default=fields.Date.context_today,
        help="Pick any date within the month you want to export. All validated or "
             "paid payslips of the current company starting in that month are exported.",
    )
    bank_code = fields.Char(
        string='Bank Code', required=True, default='NCBK',
        help="Value of the first column (البنك), as in the bank template.")
    payslip_count = fields.Integer(compute='_compute_preview')
    employee_count = fields.Integer(compute='_compute_preview')
    total_net = fields.Float(string='Total Net', digits='Payroll', compute='_compute_preview')
    issues = fields.Html(compute='_compute_preview', sanitize=False)
    has_blocking_issue = fields.Boolean(compute='_compute_preview')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')
    file_data = fields.Binary(string='File', readonly=True, attachment=False)
    file_name = fields.Char(readonly=True)

    # ------------------------------------------------------------------
    # Data
    # ------------------------------------------------------------------
    def _period(self):
        self.ensure_one()
        date_from = self.month.replace(day=1)
        if date_from.month == 12:
            date_to = date_from.replace(year=date_from.year + 1, month=1, day=1)
        else:
            date_to = date_from.replace(month=date_from.month + 1, day=1)
        return date_from, date_to

    def _get_payslips(self):
        date_from, date_to = self._period()
        return self.env['hr.payslip'].search([
            ('date_from', '>=', date_from),
            ('date_from', '<', date_to),
            ('state', 'in', ['validated', 'paid']),
            ('company_id', '=', self.env.company.id),
        ], order='employee_id, date_from, id')

    def _get_employee_address(self, employee):
        parts = [employee.private_street, employee.private_city, employee.private_state_id.name]
        return ', '.join(p for p in parts if p)

    def _get_bank_account(self, employee):
        account = employee.primary_bank_account_id or employee.bank_account_ids[:1]
        return account.acc_number or ''

    def _get_bank_name(self, employee):
        account = employee.primary_bank_account_id or employee.bank_account_ids[:1]
        return account.bank_id.name or self.bank_code or ''

    def _collect_rows(self):
        """One row per employee (payslips of the month added together), plus
        the list of problems: (message, blocking)."""
        self.ensure_one()
        rows = OrderedDict()
        issues = []
        payslips = self._get_payslips()
        if not payslips:
            date_from, _date_to = self._period()
            issues.append(("No validated or paid payslip starts in %s." % date_from.strftime('%m/%Y'), True))
        for slip in payslips:
            amounts = slip._wps_amounts()
            row = rows.setdefault(slip.employee_id, {
                'basic': 0.0, 'house': 0.0, 'others': 0.0, 'deductions': 0.0, 'net': 0.0, 'slips': [],
            })
            for key in ('basic', 'house', 'others', 'deductions', 'net'):
                row[key] += amounts[key]
            row['slips'].append(slip.name)
        for employee, row in rows.items():
            name = employee.name
            if not self._get_bank_account(employee):
                issues.append(("%s: no bank account number." % name, True))
            if not employee.identification_id:
                issues.append(("%s: no identity / Iqama number." % name, True))
            if float_compare(row['net'], 0.0, precision_digits=2) <= 0:
                issues.append(("%s: net salary is %.2f (nothing to transfer)." % (name, row['net']), True))
            computed = row['basic'] + row['house'] + row['others'] - row['deductions']
            if float_compare(computed, row['net'], precision_digits=2):
                issues.append((
                    "%s: basic + housing + other allowances - deductions = %.2f but the net salary is %.2f "
                    "(the payslip has lines outside the allowance / deduction categories)."
                    % (name, computed, row['net']), True))
            if not self._get_employee_address(employee):
                issues.append(("%s: no private address (the address column will be empty)." % name, False))
        return rows, issues

    @api.depends('month', 'bank_code')
    def _compute_preview(self):
        for wizard in self:
            if not wizard.month:
                wizard.update({'payslip_count': 0, 'employee_count': 0, 'total_net': 0.0, 'issues': False,
                               'has_blocking_issue': True})
                continue
            rows, issues = wizard._collect_rows()
            wizard.payslip_count = sum(len(row['slips']) for row in rows.values())
            wizard.employee_count = len(rows)
            wizard.total_net = sum(row['net'] for row in rows.values())
            wizard.has_blocking_issue = any(blocking for _msg, blocking in issues)
            if issues:
                items = Markup('').join(
                    Markup('<li class="%s">%s%s</li>') % (
                        'text-danger' if blocking else 'text-warning',
                        'Blocking: ' if blocking else 'Warning: ', escape(msg))
                    for msg, blocking in issues)
                wizard.issues = Markup('<ul class="mb-0">%s</ul>') % items
            else:
                wizard.issues = Markup('<span class="text-success">No problem found.</span>')

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------
    def _build_xlsx(self, rows):
        self.ensure_one()
        date_from, _date_to = self._period()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Sheet1')
        head = workbook.add_format({'bold': True, 'font_name': 'Geeza Pro', 'font_size': 10})
        bank = workbook.add_format({'bold': True, 'font_name': 'Helvetica Neue', 'font_size': 10})
        text = workbook.add_format({'font_name': 'Helvetica Neue', 'font_size': 10})
        month = workbook.add_format({'font_name': 'Helvetica Neue', 'font_size': 10, 'num_format': 'mmm-yy'})
        for col, width in COLUMN_WIDTHS.items():
            sheet.set_column(col, col, width)
        sheet.write_row(0, 0, HEADERS, head)
        month_date = fields.Datetime.to_datetime(date_from)
        for index, (employee, row) in enumerate(rows.items(), start=1):
            excel_row = index + 1
            net = float_round(row['basic'] + row['house'] + row['others'] - row['deductions'], 2)
            sheet.write_string(index, 0, self.bank_code or '', bank)
            sheet.write_string(index, 1, self._get_bank_account(employee), text)
            sheet.write_formula(index, 2, '=H%d+I%d+J%d-K%d' % ((excel_row,) * 4), text, net)
            sheet.write_datetime(index, 3, month_date, month)
            sheet.write_string(index, 4, employee.name or '', text)
            sheet.write_string(index, 5, employee.identification_id or '', text)
            sheet.write_string(index, 6, self._get_employee_address(employee), text)
            for col, key in ((7, 'basic'), (8, 'house'), (9, 'others'), (10, 'deductions')):
                sheet.write_number(index, col, float_round(row[key], 2), text)
        workbook.close()
        return output.getvalue()

    def _build_csv(self, rows):
        """Same rows as the Excel file, in the CSV layout the bank already
        receives. UTF-8 with a BOM, so Arabic names open correctly in Excel."""
        self.ensure_one()
        date_from, _date_to = self._period()
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(CSV_HEADERS)
        for employee, row in rows.items():
            basic, house, others, deductions = (
                float_round(row[key], 2) for key in ('basic', 'house', 'others', 'deductions'))
            writer.writerow([
                self._get_bank_name(employee),
                self._get_bank_account(employee),
                '%.2f' % float_round(basic + house + others - deductions, 2),
                MONTH_NAMES[date_from.month - 1],
                employee.name or '',
                employee.identification_id or '',
                self._get_employee_address(employee),
            ] + ['%.2f' % amount for amount in (basic, house, others, deductions)])
        return buffer.getvalue().encode('utf-8-sig')

    def _export_rows(self):
        """Rows of the bank file; refused while a blocking problem remains."""
        rows, issues = self._collect_rows()
        blocking = [msg for msg, is_blocking in issues if is_blocking]
        if blocking:
            raise UserError("The bank file cannot be generated:\n- " + "\n- ".join(blocking))
        return rows

    def action_export(self):
        """Build the bank salary file (same layout as the bank template) and
        offer it for download."""
        self.ensure_one()
        rows = self._export_rows()
        date_from, _date_to = self._period()
        return self._offer_file(self._build_xlsx(rows), 'Bank_Salaries_%s.xlsx' % date_from.strftime('%Y_%m'))

    def action_export_csv(self):
        """Build the bank salary file as CSV (columns of the CSV the bank
        already receives) and offer it for download."""
        self.ensure_one()
        rows = self._export_rows()
        date_from, _date_to = self._period()
        return self._offer_file(
            self._build_csv(rows), 'Salary_%s_%d.csv' % (MONTH_NAMES[date_from.month - 1], date_from.year))

    def _offer_file(self, data, file_name):
        self.write({
            'file_data': base64.b64encode(data),
            'file_name': file_name,
            'state': 'done',
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'name': 'WPS Export',
        }
