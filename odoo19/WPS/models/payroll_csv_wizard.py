from odoo import models
import csv
import io
import base64
from datetime import datetime

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_export_sif(self):
        output = io.StringIO()
        writer = csv.writer(output)

        now = datetime.now()
        creation_date = now.strftime("%Y%m%d")
        creation_time = now.strftime("%H%M")

        all_lines = self.mapped('line_ids')
        line_names = list(dict.fromkeys(line.name for line in all_lines))

        total_salary = sum(self.mapped('net_wage'))

        writer.writerow([
            "Employer EID",
            "File Creation Date",
            "File Creation Time",
            "Payer EID",
            "Payer QID",
            "Payer Bank Short Name",
            "Payer IBAN",
            "Salary Year and Month",
            "Total Salaries",
            "Total Records",
            "SIF Version"
        ])

        writer.writerow([
            "17159530",
            creation_date,
            creation_time,
            "17159530",
            "",
            "QIB",
            "QA90QISB000000000151287460019",  # IBAN
            self[0].date_to.strftime("%Y%m"),
            total_salary,
            len(self),
            "1"
        ])

        writer.writerow([])

        fixed_columns = [
            "Record ID",
            "Employee QID",
            "Employee Visa ID",
            "Employee Name",
            "Employee Bank Short Name",
            "Employee Account",
            "Salary Frequency",
            "Number of Working Days"
        ]
        writer.writerow(fixed_columns + line_names)

        record_id = 1

        for slip in self:
            bank_account = slip.employee_id.bank_account_ids[:1]

            employee_bank_name = bank_account.bank_id.name if bank_account else ''
            employee_account_number = bank_account.acc_number if bank_account else ''

            line_dict = {line.name: line.total for line in slip.line_ids}

            row = [
                record_id,
                slip.employee_id.barcode or '',
                '',
                slip.employee_id.name,
                employee_bank_name,
                employee_account_number,
                "M",
                30
            ]

            for name in line_names:
                row.append(line_dict.get(name, 0))

            writer.writerow(row)
            record_id += 1

        csv_data = output.getvalue()
        file = base64.b64encode(csv_data.encode())
        attachment = self.env['ir.attachment'].create({
            'name': f'SIF_File_{creation_date}.csv',
            'type': 'binary',
            'datas': file,
            'mimetype': 'text/csv'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }