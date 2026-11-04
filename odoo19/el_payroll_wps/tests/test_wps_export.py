# -*- coding: utf-8 -*-
import base64
import codecs
import csv
import io
from datetime import date, datetime

import openpyxl

from odoo import Command
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged

from odoo.addons.el_payroll_wps.wizard.wps_export_wizard import CSV_HEADERS, HEADERS


@tagged('post_install', '-at_install')
class TestWpsExport(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ref = cls.env.ref
        rule = lambda code, category, amount, seq: Command.create({  # noqa: E731
            'name': code, 'code': code, 'sequence': seq, 'category_id': ref(category).id,
            'condition_select': 'none', 'amount_select': 'fix', 'amount_fix': amount,
        })
        cls.structure = cls.env['hr.payroll.structure'].create({
            'name': 'WPS Test Structure',
            'type_id': ref('hr.structure_type_employee').id,
            'rule_ids': [
                Command.clear(),
                rule('BASIC', 'hr_payroll.BASIC', 5000.0, 1),
                rule('HOUALLOW', 'hr_payroll.ALW', 1000.0, 10),
                rule('TRANSP', 'hr_payroll.ALW', 300.0, 11),
                rule('PENALTY', 'hr_payroll.DED', -200.0, 50),
                Command.create({
                    'name': 'Net', 'code': 'NET', 'sequence': 100, 'category_id': ref('hr_payroll.NET').id,
                    'condition_select': 'none', 'amount_select': 'code',
                    'amount_python_compute': "result = categories['BASIC'] + categories['ALW'] + categories['DED']",
                }),
            ],
        })
        if 'journal_id' in cls.structure._fields:
            cls.structure.journal_id = False  # no accounting entry needed here
        cls.bank = cls.env['res.bank'].create({'name': 'WPS Test Bank', 'bic': 'NCBKSAJE'})
        cls.employee = cls._make_employee('WPS Employee One', 'WPS-ID-1', 'SA00WPS0000000000000001')
        cls.employee.write({'private_street': 'King Fahd Road', 'private_city': 'Riyadh'})

    @classmethod
    def _make_employee(cls, name, identification, account=None):
        employee = cls.env['hr.employee'].create({'name': name, 'identification_id': identification})
        employee.write({'wage': 5000.0, 'structure_type_id': cls.env.ref('hr.structure_type_employee').id,
                        'contract_date_start': date(2025, 1, 1)})
        if account:
            bank_account = cls.env['res.partner.bank'].create({
                'acc_number': account, 'bank_id': cls.bank.id, 'partner_id': employee.work_contact_id.id,
            })
            employee.bank_account_ids = [Command.set(bank_account.ids)]
        return employee

    def _validated_slip(self, employee, date_from=date(2026, 1, 1), date_to=date(2026, 1, 31)):
        slip = self.env['hr.payslip'].create({
            'name': 'WPS slip', 'employee_id': employee.id, 'version_id': employee.version_id.id,
            'struct_id': self.structure.id, 'date_from': date_from, 'date_to': date_to,
        })
        slip.compute_sheet()
        if 'approval_state' in slip._fields:  # one-level payroll approval, when installed
            slip.sudo().action_submit_approval()
            slip.sudo().action_approve_payslip()
        slip.action_payslip_done()
        self.assertEqual(slip.state, 'validated')
        return slip

    def _wizard(self, month=date(2026, 1, 15)):
        return self.env['wps.export.wizard'].create({'month': month})

    def _export(self, wizard):
        wizard.action_export()
        content = base64.b64decode(wizard.file_data)
        return (openpyxl.load_workbook(io.BytesIO(content)).active,
                openpyxl.load_workbook(io.BytesIO(content), data_only=True).active)

    # -----------------------------------------------------------------
    def test_others_field_is_the_other_allowances(self):
        slip = self._validated_slip(self.employee)
        self.assertEqual(slip.x_others, 300.0, "housing and deductions are not 'others'")

    def test_bank_file_has_the_template_layout_and_correct_amounts(self):
        slip = self._validated_slip(self.employee)
        wizard = self._wizard()
        self.assertFalse(wizard.has_blocking_issue, wizard.issues)
        self.assertEqual((wizard.payslip_count, wizard.employee_count), (1, 1))
        sheet, values = self._export(wizard)
        self.assertEqual([c.value for c in sheet[1]], HEADERS)
        row = [c.value for c in sheet[2]]
        self.assertEqual(row[0], 'NCBK')
        self.assertEqual(row[1], 'SA00WPS0000000000000001')
        self.assertEqual(row[2], '=H2+I2+J2-K2')
        self.assertEqual(values['C2'].value, slip.net_wage)
        self.assertEqual(row[3], datetime(2026, 1, 1))
        self.assertEqual(sheet['D2'].number_format, 'mmm-yy')
        self.assertEqual(row[4:7], ['WPS Employee One', 'WPS-ID-1', 'King Fahd Road, Riyadh'])
        self.assertEqual(row[7:11], [5000, 1000, 300, 200])
        self.assertEqual(5000 + 1000 + 300 - 200, slip.net_wage)
        self.assertEqual(wizard.file_name, 'Bank_Salaries_2026_01.xlsx')

    def test_missing_bank_account_or_id_blocks_the_export(self):
        self._validated_slip(self.employee)
        other = self._make_employee('WPS Employee Two', False)
        self._validated_slip(other)
        wizard = self._wizard()
        self.assertTrue(wizard.has_blocking_issue)
        self.assertIn('WPS Employee Two: no bank account number', wizard.issues)
        self.assertIn('WPS Employee Two: no identity / Iqama number', wizard.issues)
        with self.assertRaises(UserError):
            wizard.action_export()

    def test_payslips_of_an_employee_in_the_month_are_added_together(self):
        first = self._validated_slip(self.employee, date(2026, 1, 1), date(2026, 1, 15))
        second = self._validated_slip(self.employee, date(2026, 1, 16), date(2026, 1, 31))
        sheet, values = self._export(self._wizard())
        self.assertEqual(sheet.max_row, 2, "one row per employee")
        self.assertEqual(values['C2'].value, first.net_wage + second.net_wage)

    def test_draft_payslips_and_other_months_are_not_exported(self):
        self.env['hr.payslip'].create({
            'name': 'Draft', 'employee_id': self.employee.id, 'version_id': self.employee.version_id.id,
            'struct_id': self.structure.id, 'date_from': date(2026, 1, 1), 'date_to': date(2026, 1, 31),
        }).compute_sheet()
        self._validated_slip(self.employee, date(2026, 2, 1), date(2026, 2, 28))
        wizard = self._wizard()
        self.assertEqual(wizard.payslip_count, 0)
        self.assertTrue(wizard.has_blocking_issue)
        with self.assertRaises(UserError):
            wizard.action_export()

    def test_csv_bank_file_has_the_bank_columns_and_correct_amounts(self):
        slip = self._validated_slip(self.employee)
        wizard = self._wizard()
        wizard.action_export_csv()
        self.assertEqual(wizard.file_name, 'Salary_January_2026.csv')
        content = base64.b64decode(wizard.file_data)
        self.assertTrue(content.startswith(codecs.BOM_UTF8), "UTF-8 with BOM, for Arabic names in Excel")
        rows = list(csv.reader(io.StringIO(content.decode('utf-8-sig'))))
        self.assertEqual(rows[0], CSV_HEADERS)
        self.assertEqual(rows[1], [
            'WPS Test Bank', 'SA00WPS0000000000000001', '6100.00', 'January', 'WPS Employee One',
            'WPS-ID-1', 'King Fahd Road, Riyadh', '5000.00', '1000.00', '300.00', '200.00',
        ])
        self.assertEqual(float(rows[1][2]), slip.net_wage)
        self.assertEqual(len(rows), 2, "one row per employee")

    def test_csv_export_is_blocked_like_the_excel_one(self):
        self._validated_slip(self.employee)
        self._validated_slip(self._make_employee('WPS Employee Two', False))
        wizard = self._wizard()
        with self.assertRaises(UserError):
            wizard.action_export_csv()
        self.assertFalse(wizard.file_data)
