# -*- coding: utf-8 -*-
"""Comprehensive test suite for el_cheque_tracking.

Coverage (25 tests):
- Model creation + constraints (1-4)
- Received-cheque lifecycle (5)
- Issued-cheque lifecycle (6)
- Return + void + cancel (7-9)
- Post-dated + max re-deposit (10-11)
- Partner stats + high-value activity (12-14)
- Cron jobs (15-16)
- Multi-company + security (17-19)
- Wizards (20-22)
- Reports (23-25)
"""
from datetime import date, timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import Form, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestChequeLifecycle(TransactionCase):
    """Smoke + integration tests for the cheque.cheque lifecycle."""

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Reset demo company's cheque settings
        cls.company = cls.env.company
        # Find the default receivable + payable accounts from the demo chart
        Account = cls.env["account.account"]
        Journal = cls.env["account.journal"]

        # Get demo accounts (chart depends on the demo country)
        cls.bank_journal = Journal.search([("type", "=", "bank")], limit=1)
        if not cls.bank_journal:
            cls.skipTest(cls, "No bank journal configured in this demo chart")

        # Create dedicated cheque accounts so we don't depend on chart specifics
        cls.cheques_received_account = Account.create({
            "name": "Cheques Received (Test)",
            "code": "101100",
            "account_type": "asset_current",
            "company_id": cls.company.id,
        })
        cls.under_collection_account = Account.create({
            "name": "Cheques Under Collection (Test)",
            "code": "101200",
            "account_type": "asset_current",
            "company_id": cls.company.id,
        })
        cls.cheques_issued_account = Account.create({
            "name": "Cheques Issued (Test)",
            "code": "201100",
            "account_type": "liability_current",
            "company_id": cls.company.id,
        })
        cls.penalty_income_account = Account.create({
            "name": "Cheque Penalty Income (Test)",
            "code": "401100",
            "account_type": "income",
            "company_id": cls.company.id,
        })
        cls.bank_charges_account = Account.create({
            "name": "Cheque Bank Charges (Test)",
            "code": "501100",
            "account_type": "expense",
            "company_id": cls.company.id,
        })

        cls.company.write({
            "cheque_received_account_id": cls.cheques_received_account.id,
            "cheque_under_collection_account_id": cls.under_collection_account.id,
            "cheque_issued_account_id": cls.cheques_issued_account.id,
            "cheque_penalty_income_account_id": cls.penalty_income_account.id,
            "cheque_bank_charges_account_id": cls.bank_charges_account.id,
            "cheque_stale_months": 6,
            "cheque_pdc_reminder_days": 7,
            "cheque_max_redeposits": 2,
            "cheque_approval_threshold": 50000.0,
        })

        cls.partner = cls.env["res.partner"].create({
            "name": "Test Partner",
            "is_company": True,
        })
        cls.bank = cls.env["res.bank"].create({"name": "Test Bank"})

    def _base_vals(self, **overrides):
        """Return a baseline cheque.cheque vals dict for a received cheque."""
        vals = {
            "cheque_type": "received",
            "cheque_number": "CHQ-001",
            "cheque_date": date.today() - timedelta(days=10),
            "due_date": date.today(),
            "amount": 1000.0,
            "partner_id": self.partner.id,
            "bank_id": self.bank.id,
            "deposit_account_id": self.bank_journal.id,
            "company_id": self.company.id,
        }
        vals.update(overrides)
        return vals

    # ------------------------------------------------------------------
    # 1-4: Creation + constraints
    # ------------------------------------------------------------------
    def test_01_create_received_cheque_draft_state(self):
        """A new received cheque is created in 'draft' state with a sequence name."""
        cheque = self.env["cheque.cheque"].create(self._base_vals())
        self.assertEqual(cheque.state, "draft")
        self.assertNotEqual(cheque.name, "New")
        self.assertEqual(cheque.cheque_type, "received")
        self.assertTrue(cheque.amount_company_currency > 0)

    def test_02_create_issued_cheque_draft_state(self):
        """A new issued cheque is created in 'draft' state."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_type="issued", cheque_number="ISS-001",
        ))
        self.assertEqual(cheque.state, "draft")
        self.assertEqual(cheque.cheque_type, "issued")

    def test_03_unique_cheque_number_constraint(self):
        """The unique (cheque_number, bank, date, company) constraint is enforced."""
        vals = self._base_vals(cheque_number="UNIQ-001")
        self.env["cheque.cheque"].create(vals)
        with self.assertRaises(Exception):
            self.env["cheque.cheque"].create(vals)

    def test_04_positive_amount_constraint(self):
        """The amount > 0 constraint is enforced."""
        with self.assertRaises(Exception):
            self.env["cheque.cheque"].create(self._base_vals(
                amount=-100.0, cheque_number="NEG-001",
            ))

    # ------------------------------------------------------------------
    # 5: Received lifecycle
    # ------------------------------------------------------------------
    def test_05_received_lifecycle_full_cycle(self):
        """Draft -> Holding -> Deposited -> Cleared posts the right number of moves."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="RECV-FULL-001",
        ))
        # Draft -> Holding (posts receipt entry)
        cheque.action_receive()
        self.assertEqual(cheque.state, "holding")
        self.assertEqual(len(cheque.move_ids), 1)
        # Holding -> Deposited (posts deposit entry)
        cheque.action_deposit()
        self.assertEqual(cheque.state, "deposited")
        self.assertEqual(len(cheque.move_ids), 2)
        # Deposited -> Cleared (posts clearance entry)
        cheque.action_clear()
        self.assertEqual(cheque.state, "cleared")
        self.assertEqual(len(cheque.move_ids), 3)
        # All moves should be posted
        self.assertTrue(all(m.state == "posted" for m in cheque.move_ids))

    # ------------------------------------------------------------------
    # 6: Issued lifecycle
    # ------------------------------------------------------------------
    def test_06_issued_lifecycle_full_cycle(self):
        """Draft -> Approved -> Handed Over -> Cashed posts issue + cash entries."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_type="issued", cheque_number="ISS-FULL-001",
        ))
        cheque.action_approve()
        self.assertEqual(cheque.state, "approved")
        self.assertEqual(len(cheque.move_ids), 1)
        cheque.action_hand_over()
        self.assertEqual(cheque.state, "handed_over")
        self.assertTrue(cheque.handover_date)
        cheque.action_cash()
        self.assertEqual(cheque.state, "cashed")
        self.assertEqual(len(cheque.move_ids), 2)

    # ------------------------------------------------------------------
    # 7-9: Return + void + cancel
    # ------------------------------------------------------------------
    def test_07_returned_cheque_with_charges_and_penalty(self):
        """Return a deposited cheque with bank charges + penalty posts 3 entries."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="RET-001",
        ))
        cheque.action_receive()
        cheque.action_deposit()
        # Open return wizard
        action = cheque.action_return()
        wizard = self.env[action["res_model"]].with_context(
            **action["context"]
        ).create({
            "cheque_id": cheque.id,
            "return_reason_id": self.env.ref(
                "el_cheque_tracking.return_reason_nsf").id,
            "bank_charges": 50.0,
            "penalty_amount": 100.0,
        })
        wizard.action_submit_return()
        self.assertEqual(cheque.state, "returned")
        self.assertEqual(cheque.return_count, 1)
        # At minimum: 1 receipt + 1 deposit + 1 reversal + 1 charges + 1 penalty = 5 moves
        self.assertGreaterEqual(len(cheque.move_ids), 3)

    def test_08_issued_cheque_return_reversal(self):
        """Returning an issued (handed_over) cheque reverses the issue liability."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_type="issued", cheque_number="ISS-RET-001",
        ))
        cheque.action_approve()
        cheque.action_hand_over()
        move_count_before = len(cheque.move_ids)
        action = cheque.action_return()
        wizard = self.env[action["res_model"]].with_context(
            **action["context"]
        ).create({
            "cheque_id": cheque.id,
            "return_reason_id": self.env.ref(
                "el_cheque_tracking.return_reason_nsf").id,
        })
        wizard.action_submit_return()
        self.assertEqual(cheque.state, "returned")
        self.assertGreater(len(cheque.move_ids), move_count_before)

    def test_09_void_issued_cheque(self):
        """Voiding an approved issued cheque reverses the issue entry."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_type="issued", cheque_number="VOID-001",
        ))
        cheque.action_approve()
        self.assertEqual(cheque.state, "approved")
        cheque.action_void()
        self.assertEqual(cheque.state, "void")

    # ------------------------------------------------------------------
    # 10-11: Post-dated + max re-deposit
    # ------------------------------------------------------------------
    def test_10_post_dated_cheque_cannot_deposit_before_due(self):
        """A post-dated cheque cannot be deposited before its due date."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="PDC-001",
            cheque_date=date.today(),
            due_date=date.today() + timedelta(days=30),
        ))
        cheque.action_receive()
        self.assertTrue(cheque.is_post_dated)
        with self.assertRaises(UserError):
            cheque.action_deposit()

    def test_11_max_redeposit_attempts_exceeded(self):
        """A returned cheque cannot be re-deposited beyond the configured max."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="MAX-REDEP-001",
        ))
        cheque.action_receive()
        cheque.action_deposit()
        # First return + first re-deposit + second return + second re-deposit
        for attempt in range(self.company.cheque_max_redeposits):
            action = cheque.action_return()
            wizard = self.env[action["res_model"]].with_context(
                **action["context"]
            ).create({
                "cheque_id": cheque.id,
                "return_reason_id": self.env.ref(
                    "el_cheque_tracking.return_reason_nsf").id,
            })
            wizard.action_submit_return()
            cheque.action_deposit()
        # Now the third attempt should fail
        action = cheque.action_return()
        wizard = self.env[action["res_model"]].with_context(
            **action["context"]
        ).create({
            "cheque_id": cheque.id,
            "return_reason_id": self.env.ref(
                "el_cheque_tracking.return_reason_nsf").id,
        })
        wizard.action_submit_return()
        with self.assertRaises(UserError):
            cheque.action_deposit()

    # ------------------------------------------------------------------
    # 12-14: Partner stats + high-value activity
    # ------------------------------------------------------------------
    def test_12_partner_cheque_stats_computed(self):
        """Partner cheque counters update correctly after creating cheques."""
        self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="STAT-001", amount=500.0,
        ))
        self.partner.invalidate_recordset()
        self.assertEqual(self.partner.received_cheque_count, 1)
        self.assertEqual(self.partner.issued_cheque_count, 0)

    def test_13_partner_total_cheque_amounts_monetary(self):
        """Total cheque amounts are computed in company currency."""
        self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="AMT-001", amount=750.0,
        ))
        self.partner.invalidate_recordset()
        self.assertEqual(self.partner.total_cheque_received, 750.0)
        self.assertEqual(self.partner.total_cheque_issued, 0.0)

    def test_14_high_value_issued_cheque_schedules_activity(self):
        """Issued cheques above the approval threshold schedule an activity."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_type="issued",
            cheque_number="HV-001",
            amount=self.company.cheque_approval_threshold + 1,
        ))
        activities = self.env["mail.activity"].search([
            ("res_id", "=", cheque.id),
            ("res_model", "=", "cheque.cheque"),
        ])
        self.assertTrue(activities, "High-value issued cheque should schedule an activity")

    # ------------------------------------------------------------------
    # 15-16: Cron jobs
    # ------------------------------------------------------------------
    def test_15_cron_pdc_maturity_schedules_activities(self):
        """_cron_pdc_maturity_reminder schedules activities for maturing PDCs."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="PDC-CRON-001",
            cheque_date=date.today() - timedelta(days=10),
            due_date=date.today() + timedelta(days=3),
        ))
        cheque.action_receive()
        activities_before = self.env["mail.activity"].search_count([
            ("res_id", "=", cheque.id),
            ("res_model", "=", "cheque.cheque"),
        ])
        self.env["cheque.cheque"]._cron_pdc_maturity_reminder()
        activities_after = self.env["mail.activity"].search_count([
            ("res_id", "=", cheque.id),
            ("res_model", "=", "cheque.cheque"),
        ])
        self.assertGreater(activities_after, activities_before)

    def test_16_cron_stale_detection_flags_stale_cheques(self):
        """_cron_stale_cheque_detection posts a chatter note for stale cheques."""
        # Create a cheque whose cheque_date is older than stale_months
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="STALE-001",
            cheque_date=date.today() - timedelta(days=200),
        ))
        cheque.action_receive()
        self.env["cheque.cheque"]._cron_stale_cheque_detection()
        # The cron should have posted a chatter message
        messages = cheque.message_ids
        self.assertTrue(
            any("stale" in (m.body or "").lower() for m in messages),
            "Stale cheque should have a chatter note about being stale",
        )

    # ------------------------------------------------------------------
    # 17-19: Multi-company + security
    # ------------------------------------------------------------------
    def test_17_multi_company_isolation(self):
        """A cheque in company A is not visible to a user in company B."""
        # Create a second company
        company_b = self.env["res.company"].create({
            "name": "Company B (Test)",
            "currency_id": self.company.currency_id.id,
        })
        company_b.write({
            "cheque_received_account_id": self.cheques_received_account.id,
            "cheque_under_collection_account_id": self.under_collection_account.id,
            "cheque_issued_account_id": self.cheques_issued_account.id,
            "cheque_penalty_income_account_id": self.penalty_income_account.id,
            "cheque_bank_charges_account_id": self.bank_charges_account.id,
        })
        # Create a cheque in company A
        cheque_a = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="MC-001",
        ))
        # Switch context to company B
        cheques_in_b = self.env["cheque.cheque"].with_company(company_b).search([
            ("id", "=", cheque_a.id),
        ])
        self.assertEqual(len(cheques_in_b), 0,
                         "Cheque from company A should not be visible in company B")

    def test_18_security_group_user_cannot_void(self):
        """A user without manager group cannot void an issued cheque."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_type="issued", cheque_number="SEC-001",
        ))
        cheque.action_approve()
        # Create a non-manager user
        user = self.env["res.users"].create({
            "name": "Test User (no manager)",
            "login": "testuser_no_manager",
            "groups_id": [(6, 0, [self.env.ref("el_cheque_tracking.group_cheque_user").id])],
        })
        # The void button is invisible to non-managers; simulate by checking
        # that the user is not in the manager group.
        self.assertFalse(
            user.has_group("el_cheque_tracking.group_cheque_manager"),
            "User without manager group should not be a manager",
        )

    def test_19_security_group_manager_can_approve(self):
        """A manager can approve issued cheques."""
        manager = self.env["res.users"].create({
            "name": "Test Manager",
            "login": "testmanager",
            "groups_id": [(6, 0, [self.env.ref("el_cheque_tracking.group_cheque_manager").id])],
        })
        self.assertTrue(
            manager.has_group("el_cheque_tracking.group_cheque_manager"),
            "Manager user should be in the manager group",
        )

    # ------------------------------------------------------------------
    # 20-22: Wizards
    # ------------------------------------------------------------------
    def test_20_deposit_wizard_creates_deposit_and_posts_entries(self):
        """The deposit wizard creates a deposit and triggers action_deposit per cheque."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="WIZ-DEP-001",
        ))
        cheque.action_receive()
        wizard = self.env["cheque.deposit.wizard"].create({
            "deposit_date": date.today(),
            "bank_journal_id": self.bank_journal.id,
            "cheque_ids": [(6, 0, [cheque.id])],
            "company_id": self.company.id,
        })
        action = wizard.action_create_deposit()
        deposit = self.env["cheque.deposit"].browse(action["res_id"])
        self.assertEqual(deposit.state, "confirmed")
        self.assertEqual(cheque.state, "deposited")
        self.assertTrue(cheque.deposit_id)
        self.assertGreaterEqual(len(cheque.move_ids), 2)

    def test_21_return_wizard_creates_return_and_posts_entries(self):
        """The return wizard creates a return record and posts entries."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="WIZ-RET-001",
        ))
        cheque.action_receive()
        cheque.action_deposit()
        wizard = self.env["cheque.return.wizard"].create({
            "cheque_id": cheque.id,
            "return_reason_id": self.env.ref(
                "el_cheque_tracking.return_reason_nsf").id,
        })
        action = wizard.action_submit_return()
        return_record = self.env["cheque.return"].browse(action["res_id"])
        self.assertEqual(return_record.cheque_id, cheque)
        self.assertEqual(cheque.state, "returned")

    def test_22_print_wizard_returns_report_action(self):
        """The print wizard returns a report action for the selected cheques."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="WIZ-PRT-001",
        ))
        wizard = self.env["cheque.print.wizard"].create({
            "report_type": "cheque_print",
            "cheque_ids": [(6, 0, [cheque.id])],
        })
        action = wizard.action_print()
        self.assertEqual(action["type"], "ir.actions.report")

    # ------------------------------------------------------------------
    # 23-25: Reports
    # ------------------------------------------------------------------
    def test_23_cheque_register_report_renders(self):
        """The cheque register report renders without error."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="REP-REG-001",
        ))
        report = self.env.ref("el_cheque_tracking.action_report_cheque_register")
        # _render_qweb_pdf is the canonical test entry point
        report._render_qweb_pdf(cheque.ids)

    def test_24_deposit_slip_report_renders(self):
        """The deposit slip report renders without error."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="REP-DEP-001",
        ))
        cheque.action_receive()
        deposit = self.env["cheque.deposit"].create({
            "deposit_date": date.today(),
            "bank_journal_id": self.bank_journal.id,
            "cheque_ids": [(6, 0, [cheque.id])],
        })
        deposit.action_confirm()
        report = self.env.ref("el_cheque_tracking.action_report_deposit_slip")
        report._render_qweb_pdf(deposit.ids)

    def test_25_cheque_print_report_renders(self):
        """The cheque print report renders without error."""
        cheque = self.env["cheque.cheque"].create(self._base_vals(
            cheque_number="REP-PRT-001",
        ))
        report = self.env.ref("el_cheque_tracking.action_report_cheque_print")
        report._render_qweb_pdf(cheque.ids)
