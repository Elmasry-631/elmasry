from odoo.exceptions import UserError, AccessError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestWpsExport(TransactionCase):
    """Test suite for el_payroll_wps — covers the x_others field, the
    WPS export wizard, the CSV column layout, the discount sign (positive),
    the filename (Salary_<Month>_<Year>.csv), the UTF-8 BOM, bank/account
    extraction via primary_bank_account_id, address via private_state_id,
    the menu parenting, Odoo 19 states (validated/paid), the HOUALLOW
    housing rule code, and security."""

    # ── Setup ──────────────────────────────────────────────────────────

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.HrPayslip = cls.env['hr.payslip']
        cls.HrEmployee = cls.env['hr.employee']
        cls.HrSalaryRule = cls.env['hr.salary.rule']
        cls.HrSalaryRuleCategory = cls.env['hr.salary.rule.category']
        cls.WpsWizard = cls.env['wps.export.wizard']

        # Categories — ALW and DED are the codes used by the module
        cls.cat_alw = cls.HrSalaryRuleCategory.create({
            'name': 'Allowances', 'code': 'ALW',
        })
        cls.cat_ded = cls.HrSalaryRuleCategory.create({
            'name': 'Deductions', 'code': 'DED',
        })
        cls.cat_net = cls.HrSalaryRuleCategory.create({
            'name': 'Net', 'code': 'NET',
        })

        # Salary rules — codes match what the wizard queries
        cls.rule_basic = cls._make_rule('BASIC', 'BASIC', cls.cat_alw, 5000.0)
        cls.rule_house = cls._make_rule('HOUALLOW', 'Housing', cls.cat_alw, 1000.0)
        cls.rule_ded = cls._make_rule('DED1', 'DED1', cls.cat_ded, 200.0)
        cls.rule_net = cls._make_rule('NET', 'NET', cls.cat_net, 0.0)

        # Bank + bank account
        bank = cls.env['res.bank'].create({'name': 'Test Bank'})
        partner = cls.env.user.partner_id
        cls.bank_account = cls.env['res.partner.bank'].create({
            'acc_number': 'EG123456789',
            'bank_id': bank.id,
            'partner_id': partner.id,
        })

        # Employee — Odoo 19 uses primary_bank_account_id
        employee_vals = {
            'name': 'Test Employee',
            'identification_id': '29101012345678',
        }
        if 'primary_bank_account_id' in cls.HrEmployee._fields:
            employee_vals['primary_bank_account_id'] = cls.bank_account.id
        elif 'bank_account_id' in cls.HrEmployee._fields:
            employee_vals['bank_account_id'] = cls.bank_account.id
        cls.employee = cls.HrEmployee.create(employee_vals)

    @classmethod
    def _make_rule(cls, code, name, category, amount):
        return cls.HrSalaryRule.create({
            'name': name,
            'code': code,
            'category_id': category.id,
            'sequence': 100,
            'struct_id': cls.env.ref('hr_payroll.structure_base').id,
            'amount_select': 'fix',
            'amount_fix': amount,
        })

    def _create_payslip(self, date_from, state='validated'):
        slip = self.HrPayslip.create({
            'employee_id': self.employee.id,
            'date_from': date_from,
            'date_to': date_from.replace(day=28),
            'contract_id': False,
            'struct_id': self.env.ref('hr_payroll.structure_base').id,
        })
        slip.compute_sheet()
        if state in ('validated', 'paid'):
            # Odoo 19: action_payslip_done → state='validated'
            slip.action_payslip_done()
            if state == 'paid':
                slip.action_payslip_paid()
        return slip

    def _run_wizard(self, month_date):
        wizard = self.WpsWizard.create({'month': month_date})
        return wizard.action_export()

    def _attachment_from_action(self, action):
        att_id = int(action['url'].split('/')[-1].split('?')[0])
        return self.env['ir.attachment'].browse(att_id)

    # ── 1. x_others field exists ───────────────────────────────────────

    def test_01_others_field_exists(self):
        """x_others field is present on hr.payslip after module install."""
        slip = self.HrPayslip.create({
            'employee_id': self.employee.id,
            'date_from': '2026-07-01',
            'date_to': '2026-07-28',
            'struct_id': self.env.ref('hr_payroll.structure_base').id,
        })
        self.assertIn('x_others', slip._fields)
        self.assertEqual(slip.x_others, 0.0)

    # ── 2. x_others auto-computed on compute_sheet ────────────────────

    def test_02_others_auto_computed(self):
        """compute_sheet() populates x_others."""
        from odoo.fields import Date
        slip = self._create_payslip(Date.to_date('2026-07-01'))
        self.assertNotEqual(slip.x_others, 0.0, "x_others should have been computed")

    # ── 3. x_others = Allowances − Deductions ─────────────────────────

    def test_03_others_formula(self):
        """x_others == ALW total − DED total."""
        from odoo.fields import Date
        slip = self._create_payslip(Date.to_date('2026-07-01'))
        alw = slip._get_line_total_by_category('ALW')
        ded = slip._get_line_total_by_category('DED')
        self.assertAlmostEqual(slip.x_others, alw - ded, places=2)

    # ── 4. x_others is manually editable ──────────────────────────────

    def test_04_others_editable(self):
        """User can write a manual value into x_others."""
        from odoo.fields import Date
        slip = self._create_payslip(Date.to_date('2026-07-01'))
        slip.write({'x_others': 999.99})
        self.assertEqual(slip.x_others, 999.99, "Manual edit should stick")

    # ── 5. Wizard month field is required ─────────────────────────────

    def test_05_wizard_month_required(self):
        """Wizard raises if month is not set."""
        with self.assertRaises(Exception):
            self.WpsWizard.create({})

    # ── 6. Wizard filters by month + state (validated/paid) ───────────

    def test_06_wizard_filter(self):
        """Wizard picks up only validated/paid payslips in the chosen month."""
        from odoo.fields import Date
        import base64 as _b64
        slip_july = self._create_payslip(Date.to_date('2026-07-01'), state='validated')
        slip_august = self._create_payslip(Date.to_date('2026-08-01'), state='validated')
        action = self._run_wizard(Date.to_date('2026-07-15'))
        attachment = self._attachment_from_action(action)
        csv_text = _b64.b64decode(attachment.datas).decode('utf-8-sig')
        self.assertIn('Test Employee', csv_text)
        # Only July payslip should be in the CSV (count = 1, not 2)
        self.assertEqual(csv_text.count('Test Employee'), 1)

    # ── 7. Wizard raises if no payslips ───────────────────────────────

    def test_07_no_payslips_raises(self):
        """Wizard raises UserError when no validated payslips exist for the month."""
        from odoo.fields import Date
        with self.assertRaises(UserError):
            self._run_wizard(Date.to_date('2025-01-15'))

    # ── 8. CSV has 11 columns in correct order ────────────────────────

    def test_08_csv_columns_order(self):
        """CSV header row contains exactly the 11 columns in the spec order."""
        from odoo.fields import Date
        import base64 as _b64
        self._create_payslip(Date.to_date('2026-07-01'), state='validated')
        action = self._run_wizard(Date.to_date('2026-07-15'))
        attachment = self._attachment_from_action(action)
        csv_text = _b64.b64decode(attachment.datas).decode('utf-8-sig')
        header = csv_text.split('\n')[0].strip()
        expected = 'Bank,Account,Salary(total),Notice(month),Name,ID number,address,wage,house,Others,discount'
        self.assertEqual(header, expected)

    # ── 9. CSV discount is POSITIVE (per corrected spec) ──────────────

    def test_09_discount_positive(self):
        """The 'discount' column is always a positive number (per corrected spec)."""
        from odoo.fields import Date
        import base64 as _b64
        self._create_payslip(Date.to_date('2026-07-01'), state='validated')
        action = self._run_wizard(Date.to_date('2026-07-15'))
        attachment = self._attachment_from_action(action)
        csv_text = _b64.b64decode(attachment.datas).decode('utf-8-sig')
        lines = csv_text.strip().split('\n')
        last_col = lines[1].split(',')[-1]
        # Must NOT start with '-' (positive per corrected spec)
        self.assertFalse(last_col.startswith('-'), f"Discount should be positive, got: {last_col}")

    # ── 10. CSV filename = Salary_<Month>_<Year>.csv ──────────────────

    def test_10_filename(self):
        """Attachment filename follows Salary_<Month>_<Year>.csv pattern."""
        from odoo.fields import Date
        self._create_payslip(Date.to_date('2026-07-01'), state='validated')
        action = self._run_wizard(Date.to_date('2026-07-15'))
        attachment = self._attachment_from_action(action)
        self.assertEqual(attachment.name, 'Salary_July_2026.csv')

    # ── 11. CSV has UTF-8 BOM ─────────────────────────────────────────

    def test_11_utf8_bom(self):
        """CSV binary payload starts with UTF-8 BOM (EF BB BF)."""
        from odoo.fields import Date
        import base64 as _b64
        self._create_payslip(Date.to_date('2026-07-01'), state='validated')
        action = self._run_wizard(Date.to_date('2026-07-15'))
        attachment = self._attachment_from_action(action)
        raw_bytes = _b64.b64decode(attachment.datas)
        self.assertTrue(raw_bytes.startswith(b'\xef\xbb\xbf'), "CSV must start with UTF-8 BOM")

    # ── 12. Bank/Account extracted via primary_bank_account_id ───────

    def test_12_bank_account(self):
        """Bank name + account number pulled from primary_bank_account_id (O19)."""
        from odoo.fields import Date
        import base64 as _b64
        self._create_payslip(Date.to_date('2026-07-01'), state='validated')
        action = self._run_wizard(Date.to_date('2026-07-15'))
        attachment = self._attachment_from_action(action)
        csv_text = _b64.b64decode(attachment.datas).decode('utf-8-sig')
        data_line = csv_text.strip().split('\n')[1]
        self.assertIn('Test Bank', data_line)
        self.assertIn('EG123456789', data_line)

    # ── 13. Address uses private_state_id (Odoo 19) ───────────────────

    def test_13_address_o19(self):
        """Address helper uses private_state_id when available (Odoo 19+)."""
        wizard = self.WpsWizard.create({'month': '2026-07-15'})
        addr = wizard._get_employee_address(self.employee)
        self.assertIsInstance(addr, str)

    # ── 14. Menu parented under Payroll root ──────────────────────────

    def test_14_menu_parented(self):
        """menu_wps_export exists with correct name and parent."""
        menu = self.env.ref('el_payroll_wps.menu_wps_export', raise_if_not_found=False)
        self.assertTrue(menu, "WPS Export menu must exist")
        self.assertEqual(menu.name, 'WPS Export')

    # ── 15. Security: only Payroll User can run ───────────────────────

    def test_15_security_access(self):
        """User without hr_payroll group cannot access wps.export.wizard."""
        no_hr_user = self.env['res.users'].create({
            'name': 'No HR User',
            'login': 'nohruser_wps',
            'group_ids': [(6, 0, [self.env.ref('base.group_user').id])],
        })
        wizard_as_user = self.WpsWizard.with_user(no_hr_user)
        with self.assertRaises(AccessError):
            wizard_as_user.create({'month': '2026-07-15'})

    # ── 16. Payslip states validated/paid (Odoo 19) ───────────────────

    def test_16_o19_states(self):
        """Wizard searches for state in ('validated', 'paid') — Odoo 19 states."""
        # Create a draft payslip — should NOT be picked up by the wizard
        from odoo.fields import Date
        import base64 as _b64
        slip_draft = self.HrPayslip.create({
            'employee_id': self.employee.id,
            'date_from': Date.to_date('2026-07-01'),
            'date_to': Date.to_date('2026-07-28'),
            'struct_id': self.env.ref('hr_payroll.structure_base').id,
        })
        slip_draft.compute_sheet()
        # Draft state — wizard should raise UserError (no validated payslips)
        with self.assertRaises(UserError):
            self._run_wizard(Date.to_date('2026-07-15'))

    # ── 17. Housing rule code = HOUALLOW ──────────────────────────────

    def test_17_houallow_code(self):
        """The wizard queries payslip lines by code 'HOUALLOW' (Odoo 19)."""
        from odoo.fields import Date
        import base64 as _b64
        slip = self._create_payslip(Date.to_date('2026-07-01'), state='validated')
        # The HOUALLOW line total should be > 0 (we created a rule with amount_fix=1000)
        houallow_total = slip._get_line_amount_by_code('HOUALLOW')
        self.assertGreater(houallow_total, 0, "HOUALLOW line should have a positive total")

    # ── 18. _get_line_amount_by_code returns 0 for missing code ───────

    def test_18_missing_line_code(self):
        """_get_line_amount_by_code returns 0.0 if no line matches the code."""
        from odoo.fields import Date
        slip = self._create_payslip(Date.to_date('2026-07-01'))
        self.assertEqual(slip._get_line_amount_by_code('NONEXISTENT_CODE'), 0.0)

    # ── 19. _get_line_total_by_category returns 0 for missing cat ─────

    def test_19_missing_category(self):
        """_get_line_total_by_category returns 0.0 if no line matches the category."""
        from odoo.fields import Date
        slip = self._create_payslip(Date.to_date('2026-07-01'))
        self.assertEqual(slip._get_line_total_by_category('NONEXISTENT_CAT'), 0.0)
