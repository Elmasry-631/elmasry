import base64
import csv
import io

from odoo import models, fields
from odoo.exceptions import UserError


class WpsExportWizard(models.TransientModel):
    _name = 'wps.export.wizard'
    _description = 'WPS Payroll CSV Export'

    month = fields.Date(
        string='Month',
        required=True,
        default=fields.Date.context_today,
        help="Pick any date within the month you want to export. "
             "All payslips whose period falls in that month will be exported.",
    )

    def _get_employee_address(self, employee):
        """Odoo 19: employee.private_state_id is provided by hr.version
        via _inherits. Returns the state/province name, or '' if unset."""
        if employee.private_state_id:
            return employee.private_state_id.name or ''
        return ''

    def _get_bank_account(self, employee):
        """Return (bank_name, account_number) for the employee, or empty
        strings if the employee has no bank account on file.

        Odoo 19: prefers `primary_bank_account_id` (the new field) and
        falls back to `bank_account_id` for any 19.x version where the
        rename has not landed yet."""
        bank_name = ''
        account_number = ''
        bank_account = False
        if 'primary_bank_account_id' in employee._fields and employee.primary_bank_account_id:
            bank_account = employee.primary_bank_account_id
        elif 'bank_account_id' in employee._fields and employee.bank_account_id:
            bank_account = employee.bank_account_id
        if bank_account:
            bank_name = bank_account.bank_id.name or ''
            account_number = bank_account.acc_number or ''
        return bank_name, account_number

    def action_export(self):
        """Search every validated/paid payslip whose date_from falls inside
        the chosen month, build a CSV with the WPS column layout, store it as
        an attachment, and return a download URL action."""
        self.ensure_one()
        date_from = self.month.replace(day=1)
        if date_from.month == 12:
            date_to = date_from.replace(year=date_from.year + 1, month=1, day=1)
        else:
            date_to = date_from.replace(month=date_from.month + 1, day=1)

        payslips = self.env['hr.payslip'].search([
            ('date_from', '>=', date_from),
            ('date_from', '<', date_to),
            ('state', 'in', ['validated', 'paid']),
        ])
        if not payslips:
            raise UserError(
                "No validated payslips were found for %s." % date_from.strftime('%B %Y')
            )

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow([
            'Bank', 'Account', 'Salary(total)', 'Notice(month)', 'Name',
            'ID number', 'address', 'wage', 'house', 'Others', 'discount',
        ])

        for slip in payslips:
            employee = slip.employee_id
            bank_name, account_number = self._get_bank_account(employee)
            net_total = slip._get_line_amount_by_code('NET')
            wage = slip._get_line_amount_by_code('BASIC')
            house = slip._get_line_amount_by_code('HOUALLOW')
            deductions_total = abs(slip._get_line_total_by_category('DED'))

            writer.writerow([
                bank_name,
                account_number,
                net_total,
                date_from.strftime('%B'),
                employee.name or '',
                employee.identification_id or '',
                self._get_employee_address(employee),
                wage,
                house,
                slip.x_others,
                deductions_total,
            ])

        csv_data = buffer.getvalue().encode('utf-8-sig')  # BOM for Excel/Arabic-safe opening
        filename = 'Salary_%s.csv' % date_from.strftime('%B_%Y')

        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(csv_data),
            'mimetype': 'text/csv',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }
