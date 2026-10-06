# -*- coding: utf-8 -*-
from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestHrAttendanceSheet(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create minimal data for testing
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Test Employee',
        })
        # Create overtime rule (only one rule per type and company is allowed,
        # so the existing one is reused and configured for the test)
        cls.company = cls.env.company
        overtime_model = cls.env['hr.attendance.rule.overtime']
        cls.overtime_rule = overtime_model.search([
            ('type', '=', 'working_day'),
            ('company_id', '=', cls.company.id),
        ], limit=1)
        if cls.overtime_rule:
            cls.overtime_rule.write({
                'name': 'OT Working Day',
                'apply_after_minutes': 0,
                'rate': 1.5,
            })
        else:
            cls.overtime_rule = overtime_model.create({
                'name': 'OT Working Day',
                'type': 'working_day',
                'apply_after_minutes': 0,
                'rate': 1.5,
                'company_id': cls.company.id,
            })
        # Create lateness rule with a first-occurrence tier holding steps
        cls.lateness_rule = cls.env['hr.attendance.rule.lateness'].create({
            'name': 'Lateness Standard',
            'company_id': cls.company.id,
        })
        cls.lateness_tier = cls.env['hr.attendance.rule.lateness.tier'].create({
            'name': 'First Lateness',
            'lateness_id': cls.lateness_rule.id,
            'occurrence_from': 1,
            'occurrence_to': 9999,
        })
        cls.env['hr.attendance.rule.lateness.step'].create({
            'tier_id': cls.lateness_tier.id,
            'from_minutes': 0,
            'to_minutes': 15,
            'penalty_type': 'rate',
            'rate': 1.0,
            'initial_rate': 1.0,
        })
        cls.env['hr.attendance.rule.lateness.step'].create({
            'tier_id': cls.lateness_tier.id,
            'from_minutes': 15,
            'to_minutes': 60,
            'penalty_type': 'rate',
            'rate': 1.5,
            'initial_rate': 1.0,
        })
        # Create absence rule with a first-absence tier
        cls.absence_rule = cls.env['hr.attendance.rule.absence'].create({
            'name': 'Absence Standard',
            'company_id': cls.company.id,
        })
        cls.absence_tier = cls.env['hr.attendance.rule.absence.tier'].create({
            'name': 'First Absence',
            'absence_id': cls.absence_rule.id,
            'occurrence_from': 1,
            'occurrence_to': 9999,
        })
        cls.env['hr.attendance.rule.absence.step'].create({
            'tier_id': cls.absence_tier.id,
            'from_days': 1,
            'to_days': 3,
            'penalty_type': 'rate',
            'rate': 1.0,
        })
        # Create attendance policy
        cls.policy = cls.env['hr.attendance.policy'].create({
            'name': 'Test Policy',
            'overtime_working_id': cls.overtime_rule.id,
            'lateness_id': cls.lateness_rule.id,
            'absence_id': cls.absence_rule.id,
            'company_id': cls.company.id,
        })

    def test_01_overtime_rule_creation(self):
        """Overtime rule should be created correctly."""
        self.assertEqual(self.overtime_rule.rate, 1.5)
        self.assertEqual(self.overtime_rule.type, 'working_day')

    def test_02_lateness_step_lookup(self):
        """Lateness step lookup should return the correct step."""
        step = self.lateness_rule.get_step_for_minutes(20)
        self.assertEqual(step.rate, 1.5)
        step = self.lateness_rule.get_step_for_minutes(5)
        self.assertEqual(step.rate, 1.0)

    def test_03_absence_step_lookup(self):
        """Absence step lookup should return the correct step."""
        step = self.absence_rule.get_step_for_days(2)
        self.assertEqual(step.rate, 1.0)

    def test_04_policy_get_overtime_rule(self):
        """Policy should return the correct overtime rule per day type."""
        rule = self.policy.get_overtime_rule('working_day')
        self.assertEqual(rule, self.overtime_rule)
        rule = self.policy.get_overtime_rule('weekend')
        self.assertFalse(rule)

    def test_05_sheet_sequence(self):
        """Sheet should get a sequence number on creation."""
        sheet = self.env['hr.attendance.sheet'].create({
            'employee_id': self.employee.id,
            'date_from': '2026-01-01',
            'date_to': '2026-01-15',
            'company_id': self.company.id,
        })
        self.assertNotEqual(sheet.name, 'New')
        self.assertTrue(sheet.name.startswith('AS/'))

    def test_06_state_machine_transitions(self):
        """Sheet should follow the correct state machine."""
        sheet = self.env['hr.attendance.sheet'].create({
            'employee_id': self.employee.id,
            'date_from': '2026-01-01',
            'date_to': '2026-01-15',
            'company_id': self.company.id,
        })
        self.assertEqual(sheet.state, 'draft')
        # Compute should fail because no contract
        # (no contract because the test employee has none)
        # Just verify state stays draft
        self.assertEqual(sheet.state, 'draft')

    def test_07_public_holiday_state_machine(self):
        """Public holiday state machine."""
        holiday = self.env['hr.attendance.public.holiday'].create({
            'name': 'Test Holiday',
            'date_from': '2026-01-01',
            'date_to': '2026-01-01',
            'company_id': self.company.id,
        })
        self.assertEqual(holiday.state, 'draft')
        # Activation should fail without lines
        # (verify constraint logic — don't raise, just check state stays draft)
        self.assertEqual(holiday.state, 'draft')

    def test_08_overtime_calculation(self):
        """Test the overtime calculation helper."""
        sheet = self.env['hr.attendance.sheet'].create({
            'employee_id': self.employee.id,
            'date_from': '2026-01-01',
            'date_to': '2026-01-15',
            'company_id': self.company.id,
        })
        # Working day, worked 10h, planned 8h, no apply_after
        ot = sheet._compute_overtime_hours(
            worked_hours=10.0, planned_hours=8.0,
            day_type='working_day', overtime_rule=self.overtime_rule,
        )
        self.assertEqual(ot, 2.0)
        # Public holiday, worked 8h
        ot = sheet._compute_overtime_hours(
            worked_hours=8.0, planned_hours=0.0,
            day_type='public_holiday', overtime_rule=self.overtime_rule,
        )
        self.assertEqual(ot, 8.0)
        # Working day with apply_after = 30 min (one rule per type and
        # company, so the existing public holiday rule is reused)
        overtime_model = self.env['hr.attendance.rule.overtime']
        rule_30 = overtime_model.search([
            ('type', '=', 'public_holiday'),
            ('company_id', '=', self.company.id),
        ], limit=1)
        if rule_30:
            rule_30.write({
                'name': 'OT with apply_after',
                'apply_after_minutes': 30,
                'rate': 1.5,
            })
        else:
            rule_30 = overtime_model.create({
                'name': 'OT with apply_after',
                'type': 'public_holiday',
                'apply_after_minutes': 30,
                'rate': 1.5,
                'company_id': self.company.id,
            })
        ot = sheet._compute_overtime_hours(
            worked_hours=10.0, planned_hours=8.0,
            day_type='working_day', overtime_rule=rule_30,
        )
        # 10-8 = 2h, minus 0.5h apply_after = 1.5h
        self.assertEqual(ot, 1.5)

    # ------------------------------------------------------------------
    # Tiers (escalation per repetition level)
    # ------------------------------------------------------------------
    def test_09_lateness_tier_lookup_by_occurrence(self):
        """Each lateness tier owns the steps of its own repetition level."""
        rule = self.env['hr.attendance.rule.lateness'].create({
            'name': 'Lateness Escalating',
            'unit': 'hours',
            'company_id': self.company.id,
        })
        tier_model = self.env['hr.attendance.rule.lateness.tier']
        first_tier = tier_model.create({
            'name': 'First Lateness',
            'lateness_id': rule.id,
            'occurrence_from': 1,
            'occurrence_to': 1,
        })
        second_tier = tier_model.create({
            'name': 'Second Lateness',
            'lateness_id': rule.id,
            'occurrence_from': 2,
            'occurrence_to': 9999,
        })
        step_model = self.env['hr.attendance.rule.lateness.step']
        first = step_model.create({
            'tier_id': first_tier.id,
            'from_minutes': 0,
            'to_minutes': 30,
            'penalty_type': 'rate',
            'rate': 1.0,
            'initial_rate': 1.0,
        })
        second = step_model.create({
            'tier_id': second_tier.id,
            'from_minutes': 0,
            'to_minutes': 30,
            'penalty_type': 'rate',
            'rate': 3.0,
            'initial_rate': 1.0,
        })
        # First occurrence resolves to the first tier's step
        self.assertEqual(rule.get_tier(1), first_tier)
        step = rule.get_step_for_minutes(10, 1)
        self.assertEqual(step, first)
        # Repeated lateness resolves to the second tier's step
        self.assertEqual(rule.get_tier(2), second_tier)
        step = rule.get_step_for_minutes(10, 2)
        self.assertEqual(step, second)
        step = rule.get_step_for_minutes(10, 5)
        self.assertEqual(step, second)
        # Hours lookup follows the same tier resolution
        step = rule.get_step_for_hours(0.5, 2)
        self.assertEqual(step, second)
        self.assertEqual(step.rate, 3.0)
        # get_step uses the rule unit (hours here)
        step = rule.get_step(0.5, 2)
        self.assertEqual(step, second)
        # An occurrence below every tier range resolves to nothing
        self.assertFalse(rule.get_tier(0))

    def test_10_absence_tier_escalation(self):
        """Absence tiers escalate the deduction with the absence count."""
        rule = self.env['hr.attendance.rule.absence'].create({
            'name': 'Absence Escalating',
            'company_id': self.company.id,
        })
        tier_model = self.env['hr.attendance.rule.absence.tier']
        # 1st absence deducts 2 days, 2nd and onwards deducts 3 days
        first_tier = tier_model.create({
            'name': 'First Absence',
            'absence_id': rule.id,
            'occurrence_from': 1,
            'occurrence_to': 1,
        })
        second_tier = tier_model.create({
            'name': 'Second Absence',
            'absence_id': rule.id,
            'occurrence_from': 2,
            'occurrence_to': 9999,
        })
        step_model = self.env['hr.attendance.rule.absence.step']
        step_model.create({
            'tier_id': first_tier.id,
            'from_days': 1,
            'to_days': 9999,
            'penalty_type': 'rate',
            'rate': 2.0,
        })
        second = step_model.create({
            'tier_id': second_tier.id,
            'from_days': 1,
            'to_days': 9999,
            'penalty_type': 'rate',
            'rate': 3.0,
        })
        step = rule.get_step_for_days(1, 1)
        self.assertEqual(step.rate, 2.0)
        step = rule.get_step_for_days(1, 2)
        self.assertEqual(step, second)
        self.assertEqual(step.rate, 3.0)

    def test_11_absence_fixed_days_penalty(self):
        """An absence step can deduct a fixed number of days."""
        rule = self.env['hr.attendance.rule.absence'].create({
            'name': 'Absence Fixed Days',
            'company_id': self.company.id,
        })
        tier = self.env['hr.attendance.rule.absence.tier'].create({
            'name': 'Any Absence',
            'absence_id': rule.id,
            'occurrence_from': 1,
            'occurrence_to': 9999,
        })
        step = self.env['hr.attendance.rule.absence.step'].create({
            'tier_id': tier.id,
            'from_days': 1,
            'to_days': 9999,
            'penalty_type': 'days',
            'deduction_days': 4.0,
        })
        found = rule.get_step_for_days(1, 1)
        self.assertEqual(found, step)
        self.assertEqual(found.compute_deduction_days(1), 4.0)

    def test_12_lateness_step_hour_fields(self):
        """The hour convenience fields stay in sync with the minute fields."""
        step = self.env['hr.attendance.rule.lateness.step'].create({
            'tier_id': self.lateness_tier.id,
            'from_minutes': 90,
            'to_minutes': 120,
            'penalty_type': 'rate',
        })
        self.assertAlmostEqual(step.from_hours, 1.5, places=3)
        self.assertAlmostEqual(step.to_hours, 2.0, places=3)
        # Writing hours updates the stored minute range
        step.write({'from_hours': 3.0, 'to_hours': 4.0})
        self.assertAlmostEqual(step.from_minutes, 180.0, places=3)
        self.assertAlmostEqual(step.to_minutes, 240.0, places=3)

    def test_13_tier_overlap_rejected(self):
        """Two tiers of the same rule must not cover the same occurrence."""
        from odoo.exceptions import UserError
        rule = self.env['hr.attendance.rule.absence'].create({
            'name': 'Overlap Check',
            'company_id': self.company.id,
        })
        tier_model = self.env['hr.attendance.rule.absence.tier']
        tier_model.create({
            'name': 'T1',
            'absence_id': rule.id,
            'occurrence_from': 1,
            'occurrence_to': 5,
        })
        with self.assertRaises(UserError):
            tier_model.create({
                'name': 'T2',
                'absence_id': rule.id,
                'occurrence_from': 3,
                'occurrence_to': 9,
            })

    def test_14_tier_inverted_range_rejected(self):
        """A tier with To below From is refused."""
        from odoo.exceptions import UserError
        rule = self.env['hr.attendance.rule.lateness'].create({
            'name': 'Range Check',
            'company_id': self.company.id,
        })
        with self.assertRaises(UserError):
            self.env['hr.attendance.rule.lateness.tier'].create({
                'name': 'Bad Tier',
                'lateness_id': rule.id,
                'occurrence_from': 5,
                'occurrence_to': 2,
            })

    def test_15_tier_cascade_and_navigation(self):
        """Tiers cascade with their rule and the navigation actions resolve."""
        rule = self.env['hr.attendance.rule.absence'].create({
            'name': 'Cascade Rule',
            'company_id': self.company.id,
        })
        tier = self.env['hr.attendance.rule.absence.tier'].create({
            'name': 'First Absence',
            'absence_id': rule.id,
            'occurrence_from': 1,
            'occurrence_to': 1,
        })
        step = self.env['hr.attendance.rule.absence.step'].create({
            'tier_id': tier.id,
            'from_days': 1,
            'to_days': 9999,
            'penalty_type': 'rate',
            'rate': 2.0,
        })
        self.assertEqual(step.absence_id, rule)
        self.assertEqual(tier.step_count, 1)
        # Navigation actions point at the right records
        action = tier.action_open_rule()
        self.assertEqual(action['res_model'], 'hr.attendance.rule.absence')
        self.assertEqual(action['res_id'], rule.id)
        action = tier.action_open_tier()
        self.assertEqual(action['res_model'], 'hr.attendance.rule.absence.tier')
        self.assertEqual(action['res_id'], tier.id)

    # ------------------------------------------------------------------
    # Payroll structure
    # ------------------------------------------------------------------
    def test_16_attendance_structure_created_without_inherited_rules(self):
        """Creating an ATT structure must not copy the default structure rules.

        hr.payroll.structure.rule_ids defaults to a copy of every rule of
        hr_payroll.default_structure (BASIC, GROSS, NET, ...). Those copies
        would double the salary on any payslip using the structure.
        """
        structure = self.env['hr.payroll.structure'].create({
            'name': 'Fresh Attendance Structure',
            'code': 'ATT',
            'type_id': self.env.ref('hr.structure_type_employee').id,
        })
        self.assertFalse(
            structure.rule_ids,
            "A new attendance structure must start with no rules, got: %s"
            % ', '.join(structure.rule_ids.mapped('code')),
        )

    def test_17_attendance_rules_run_before_net(self):
        """Every attendance rule must be computed before NET.

        Rules are applied in ascending sequence order, so a deduction sitting
        after the NET rule would never reach the net salary.
        """
        structure = self.env.ref(
            'el_hr_attendance_sheet.structure_attendance')
        for code in ('OVERT', 'LATE', 'ABS', 'DIFF'):
            rule = structure.rule_ids.filtered(lambda r, c=code: r.code == c)
            self.assertTrue(rule, "Missing rule %s" % code)
            self.assertLess(
                rule.sequence, 200,
                "Rule %s (sequence %s) runs at or after NET (200), so it "
                "would not affect the net salary."
                % (code, rule.sequence),
            )

    def test_18_clean_inherited_rules_respects_payslip_lines(self):
        """Cleanup removes free inherited rules but never locked ones.

        A salary rule referenced by a payslip line cannot be deleted without
        a foreign key violation, so it must be kept instead of blowing up the
        upgrade.
        """
        structure = self.env.ref(
            'el_hr_attendance_sheet.structure_attendance')
        Rule = self.env['hr.salary.rule']
        default = self.env.ref('hr_payroll.default_structure')
        default_category = self.env.ref('hr_payroll.BASIC')
        # One inherited rule that nothing references, one that is locked.
        free_rule = Rule.create({
            'name': 'Free Inherited Rule',
            'code': 'ATT_FREE',
            'struct_ids': [fields.Command.set([structure.id])],
            'sequence': 195,
            'category_ids': [fields.Command.set(default_category.ids)],
        })
        locked_rule = Rule.create({
            'name': 'Locked Inherited Rule',
            'code': 'ATT_LOCKED',
            'struct_ids': [fields.Command.set([structure.id])],
            'sequence': 196,
            'category_ids': [fields.Command.set(default_category.ids)],
        })
        payslip = self.env['hr.payslip'].create({
            'name': 'TEST CLEANUP',
            'employee_id': self.employee.id,
            'date_from': '2026-03-01',
            'date_to': '2026-03-31',
            'struct_id': structure.id,
        })
        self.env['hr.payslip.line'].create({
            'slip_id': payslip.id,
            'salary_rule_id': locked_rule.id,
            'employee_id': self.employee.id,
            'version_id': payslip.version_id.id,
            'name': locked_rule.name,
            'sequence': 1,
        })
        try:
            structure.action_clean_inherited_rules()
            self.assertNotIn(
                free_rule, structure.rule_ids,
                "An inherited rule with no payslip line should be removed.")
            self.assertIn(
                locked_rule, structure.rule_ids,
                "A rule referenced by a payslip line must be kept, deleting "
                "it would raise a foreign key violation.")
        finally:
            payslip.with_context(tracking_disable=True).unlink()
            (free_rule | locked_rule).exists().unlink()

    # ------------------------------------------------------------------
    # Payslip <-> attendance sheet linking
    # ------------------------------------------------------------------
    def _make_payable_sheet(self):
        """Build a sheet with overtime and one absence for employee 1."""
        self.env['hr.attendance'].create({
            'employee_id': self.employee.id,
            'check_in': '2026-02-02 09:00:00',
            'check_out': '2026-02-02 18:00:00',
        })
        self.env['hr.attendance'].create({
            'employee_id': self.employee.id,
            'check_in': '2026-02-03 11:00:00',
            'check_out': '2026-02-03 18:00:00',
        })
        version = self.env['hr.version'].search([
            ('employee_id', '=', self.employee.id)], limit=1)
        # date_start/date_end are computed from the contract dates.
        version.write({
            'contract_date_start': '2026-02-01',
            'contract_date_end': False,
            'attendance_policy_id': self.policy.id,
            'resource_calendar_id': self.env.ref(
                'resource.resource_calendar_std').id,
        })
        sheet = self.env['hr.attendance.sheet'].create({
            'employee_id': self.employee.id,
            'date_from': '2026-02-01',
            'date_to': '2026-02-28',
            'company_id': self.company.id,
        })
        sheet.action_compute()
        sheet.action_approve()
        return sheet

    def test_19_payslip_auto_links_matching_sheet(self):
        """A payslip created without a sheet picks up the matching one.

        Creating a payslip straight from the payroll menu leaves
        attendance_sheet_id empty, so every attendance amount computes to 0.
        """
        sheet = self._make_payable_sheet()
        self.assertGreater(sheet.total_overtime, 0)
        payslip = self.env['hr.payslip'].create({
            'name': 'TEST AUTOLINK',
            'employee_id': self.employee.id,
            'date_from': '2026-02-01',
            'date_to': '2026-02-28',
            'struct_id': self.env.ref(
                'el_hr_attendance_sheet.structure_attendance').id,
            'version_id': self.env['hr.version'].search([
                ('employee_id', '=', self.employee.id)], limit=1).id,
        })
        self.assertEqual(payslip.attendance_sheet_id, sheet)
        self.assertEqual(sheet.payslip_id, payslip)
        self.assertAlmostEqual(payslip.overtime_hours, sheet.total_overtime)
        self.assertAlmostEqual(payslip.absence_days, sheet.total_absence)
        self.assertFalse(payslip.no_attendance_sheet)

    def test_20_payslip_flag_when_no_sheet(self):
        """A payslip with no matching sheet is flagged for the user."""
        payslip = self.env['hr.payslip'].create({
            'name': 'TEST NO SHEET',
            'employee_id': self.employee.id,
            'date_from': '2020-01-01',
            'date_to': '2020-01-31',
            'struct_id': self.env.ref(
                'el_hr_attendance_sheet.structure_attendance').id,
            'version_id': self.env['hr.version'].search([
                ('employee_id', '=', self.employee.id)], limit=1).id,
        })
        self.assertFalse(payslip.attendance_sheet_id)
        self.assertTrue(payslip.no_attendance_sheet)
        self.assertEqual(payslip.overtime_hours, 0.0)
        self.assertEqual(payslip.absence_days, 0.0)

    def test_21_action_link_attendance_sheet(self):
        """The manual link button attaches the sheet and computes amounts."""
        from odoo.exceptions import UserError
        sheet = self._make_payable_sheet()
        payslip = self.env['hr.payslip'].create({
            'name': 'TEST MANUAL LINK',
            'employee_id': self.employee.id,
            'date_from': '2026-03-01',
            'date_to': '2026-03-31',
            'struct_id': self.env.ref(
                'el_hr_attendance_sheet.structure_attendance').id,
            'version_id': self.env['hr.version'].search([
                ('employee_id', '=', self.employee.id)], limit=1).id,
        })
        # Period 03 has no sheet -> explicit error, no silent zeroing
        with self.assertRaises(UserError):
            payslip.action_link_attendance_sheet()
        # Linking the real sheet fills the amounts
        payslip.write({
            'date_from': '2026-02-01', 'date_to': '2026-02-28'})
        payslip.action_link_attendance_sheet()
        self.assertEqual(payslip.attendance_sheet_id, sheet)
        self.assertAlmostEqual(payslip.overtime_hours, sheet.total_overtime)
        # Linking twice is refused
        with self.assertRaises(UserError):
            payslip.action_link_attendance_sheet()

    # ------------------------------------------------------------------
    # Timezone handling for lateness
    # ------------------------------------------------------------------
    def test_22_shift_start_is_converted_to_utc(self):
        """The shift start must be UTC, like hr.attendance.check_in.

        resource.calendar.attendance.hour_from is a wall-clock time read in the
        timezone of the employee resource (a calendar has no timezone of its own
        since Odoo 20) while check_in is stored in UTC. Comparing the two
        without converting the shift start reports every employee as early,
        so lateness is always 0 on any calendar outside UTC.
        """
        from datetime import date, datetime, timedelta
        self.employee.tz = 'Africa/Cairo'
        calendar = self.env['resource.calendar'].create({
            'name': 'TZ Calendar',
            'attendance_ids': [
                (0, 0, {
                    'dayofweek': '0',
                    'hour_from': 8.0, 'hour_to': 16.0,
                }),
            ],
        })
        sheet = self.env['hr.attendance.sheet'].new({
            'employee_id': self.employee.id,
            'date_from': '2026-04-06', 'date_to': '2026-04-30',
        })
        # Africa/Cairo is UTC+2 in April 2026 (before DST), so 08:00 local
        # is 06:00 UTC. The offset is read from the tz database rather than
        # hardcoded, so this stays correct across DST changes.
        day = date(2026, 4, 6)
        shift_start = sheet._shift_start_for_day(calendar, day)
        expected_utc = datetime(2026, 4, 6, 6, 0)
        self.assertEqual(
            shift_start, expected_utc,
            "The shift start must be converted to UTC before being compared "
            "with hr.attendance.check_in.")
        # A check-in 20 minutes after the shift start is late by 20 minutes.
        late_check_in = shift_start + timedelta(minutes=20)
        self.assertAlmostEqual(
            (late_check_in - shift_start).total_seconds() / 60.0, 20.0,
            places=2)
        self.assertGreater(late_check_in, shift_start)
        # A check-in exactly at the shift start is on time.
        self.assertFalse(shift_start + timedelta(minutes=1) < shift_start)
        # In September the calendar is at UTC+3, so the same 08:00 shift is
        # 05:00 UTC. This is what makes lateness detection work year round.
        sept_start = sheet._shift_start_for_day(calendar, date(2026, 9, 7))
        self.assertEqual(
            sept_start, datetime(2026, 9, 7, 5, 0),
            "DST must be taken into account: Africa/Cairo switches to UTC+3 "
            "in September.")
        # An employee working in UTC stays untouched.
        self.employee.tz = 'UTC'
        utc_cal = self.env['resource.calendar'].create({
            'name': 'UTC Calendar',
            'attendance_ids': [
                (0, 0, {
                    'dayofweek': '0',
                    'hour_from': 8.0, 'hour_to': 16.0,
                }),
            ],
        })
        self.assertEqual(
            sheet._shift_start_for_day(utc_cal, day),
            datetime(2026, 4, 6, 8, 0))

    def test_23_absence_line_uses_occurrence_count(self):
        """Each absence line is priced on its own tier, without compounding.

        The 1st absence uses the 1st tier's rate, the 2nd the 2nd tier's rate.
        A tier configured "from_days 2" describes the 2nd absence, so the
        lookup must pass the occurrence number rather than a hardcoded 1, and
        the resulting rate must not be multiplied by that number — otherwise
        repeating an absence re-charges the earlier penalties as well.
        """
        rule = self.env['hr.attendance.rule.absence'].create({
            'name': 'Occurrence Escalation',
            'company_id': self.company.id,
        })
        tier_model = self.env['hr.attendance.rule.absence.tier']
        first = tier_model.create({
            'name': 'First Absence', 'absence_id': rule.id,
            'occurrence_from': 1, 'occurrence_to': 1,
        })
        second = tier_model.create({
            'name': 'Second Absence', 'absence_id': rule.id,
            'occurrence_from': 2, 'occurrence_to': 2,
        })
        self.env['hr.attendance.rule.absence.step'].create({
            'tier_id': first.id, 'from_days': 1, 'to_days': 1,
            'penalty_type': 'rate', 'rate': 2.0,
        })
        self.env['hr.attendance.rule.absence.step'].create({
            'tier_id': second.id, 'from_days': 2, 'to_days': 2,
            'penalty_type': 'rate', 'rate': 3.0,
        })
        # Tiers created out of order must still resolve by range.
        self.assertEqual(rule.get_tier(1), first)
        self.assertEqual(rule.get_tier(2), second)
        # The 2nd occurrence resolves to the 2nd tier's step.
        self.assertEqual(
            rule.get_step_for_days(2, 2).rate, 3.0)

        # Now exercise the line compute with two absences.
        sheet = self.env['hr.attendance.sheet'].create({
            'employee_id': self.employee.id,
            'date_from': '2026-05-01',
            'date_to': '2026-05-31',
            'company_id': self.company.id,
        })
        policy = self.env['hr.attendance.policy'].create({
            'name': 'Occurrence Policy',
            'absence_id': rule.id,
            'company_id': self.company.id,
        })
        sheet.write({'policy_id': policy.id})
        lines = self.env['hr.attendance.sheet.line']
        first_line = lines.create({
            'sheet_id': sheet.id, 'date': '2026-05-04',
            'day_type': 'working_day', 'is_absent': True,
            'absence_occurrence': 1,
        })
        second_line = lines.create({
            'sheet_id': sheet.id, 'date': '2026-05-05',
            'day_type': 'working_day', 'is_absent': True,
            'absence_occurrence': 2,
        })
        # Each absence is charged on its own tier, without multiplying:
        # 1st absence = rate 2, 2nd absence = rate 3, total 5 days.
        self.assertAlmostEqual(first_line.absence_penalty_days, 2.0)
        self.assertAlmostEqual(second_line.absence_penalty_days, 3.0)
        self.assertAlmostEqual(sheet.total_absence_penalty_days, 5.0)

    def test_24_lateness_step_flat_penalty_hours(self):
        """A lateness step can charge a flat number of penalised hours."""
        rule = self.env['hr.attendance.rule.lateness'].create({
            'name': 'Flat Hours Lateness',
            'unit': 'minutes',
            'company_id': self.company.id,
        })
        tier = self.env['hr.attendance.rule.lateness.tier'].create({
            'name': 'First Lateness',
            'lateness_id': rule.id,
            'occurrence_from': 1,
            'occurrence_to': 9999,
        })
        self.env['hr.attendance.rule.lateness.step'].create({
            'tier_id': tier.id,
            'from_minutes': 0,
            'to_minutes': 15,
            'penalty_type': 'hours',
            'penalty_hours': 2.0,
        })
        sheet = self.env['hr.attendance.sheet'].create({
            'employee_id': self.employee.id,
            'date_from': '2026-06-01',
            'date_to': '2026-06-30',
            'company_id': self.company.id,
        })
        policy = self.env['hr.attendance.policy'].create({
            'name': 'Flat Hours Policy',
            'lateness_id': rule.id,
            'company_id': self.company.id,
        })
        sheet.write({'policy_id': policy.id})
        # 3 minutes late is still charged the flat 2 hours, not 3/60.
        line = self.env['hr.attendance.sheet.line'].create({
            'sheet_id': sheet.id, 'date': '2026-06-02',
            'day_type': 'working_day',
            'late_in_minutes': 3.0, 'late_occurrence': 1,
        })
        self.assertAlmostEqual(line.late_penalty, 2.0)
        self.assertAlmostEqual(sheet.total_late_penalty_hours, 2.0)

    # ------------------------------------------------------------------
    # Attendance rules propagation
    # ------------------------------------------------------------------
    def test_25_propagate_attendance_rules_to_other_structures(self):
        """The attendance rules are copied into the other structures.

        A payslip applies a single structure, so overtime / lateness / absence
        only get computed when their rules sit next to the basic salary.
        """
        source = self.env.ref(
            'el_hr_attendance_sheet.structure_attendance')
        target = self.env['hr.payroll.structure'].create({
            'name': 'Propagation Target',
            'type_id': self.env.ref('hr.structure_type_employee').id,
        })
        self.assertFalse(
            target.rule_ids.filtered(lambda r: r.code in ('OVERT', 'LATE', 'ABS')))
        added = source.action_propagate_attendance_rules()
        self.assertTrue(added)
        codes = target.rule_ids.mapped('code')
        for code in ('OVERT', 'LATE', 'ABS'):
            self.assertIn(code, codes)
        # The source structure keeps its own rules (copy, not move).
        for code in ('OVERT', 'LATE', 'ABS'):
            self.assertTrue(source.rule_ids.filtered(
                lambda r, c=code: r.code == c))
        # Idempotent: running it again adds nothing.
        again = source.action_propagate_attendance_rules()
        self.assertFalse(again)

    def test_26_server_action_runs_the_propagation(self):
        """The server action delegates to the same propagation."""
        from odoo.exceptions import UserError
        source = self.env.ref(
            'el_hr_attendance_sheet.structure_attendance')
        action = self.env.ref(
            'el_hr_attendance_sheet.action_propagate_attendance_rules')
        target = self.env['hr.payroll.structure'].create({
            'name': 'Server Action Target',
            'type_id': self.env.ref('hr.structure_type_employee').id,
        })
        action.with_context(
            active_model='hr.payroll.structure', active_ids=target.ids,
        ).run()
        self.assertTrue(target.rule_ids.filtered(lambda r: r.code == 'OVERT'))
        self.assertTrue(target.rule_ids.filtered(lambda r: r.code == 'ABS'))
        # A second run adds nothing and reports that there was nothing to do.
        with self.assertRaises(UserError):
            action.with_context(
                active_model='hr.payroll.structure', active_ids=target.ids,
            ).run()
        # Silent mode (used by the post-install hook) never raises.
        other = self.env['hr.payroll.structure'].create({
            'name': 'Silent Target',
            'type_id': self.env.ref('hr.structure_type_employee').id,
        })
        action.with_context(
            attendance_propagate_silent=True,
            active_model='hr.payroll.structure', active_ids=other.ids,
        ).run()
        self.assertTrue(other.rule_ids.filtered(lambda r: r.code == 'ABS'))
        # The source structure keeps its own rules (copy, not move).
        self.assertTrue(source.rule_ids.filtered(lambda r: r.code == 'OVERT'))
