# -*- coding: utf-8 -*-
# el_restrict_journal — Test suite (WHITELIST mode)
#
# 13 test methods covering the WHITELIST semantics:
#   1.  User allowed_journal_ids field setup
#   2.  account.move create BLOCKED with non-allowed journal
#   3.  account.move write BLOCKED when switching to non-allowed journal
#   4.  account.payment create BLOCKED with non-allowed journal
#   5.  account.payment write BLOCKED when switching to non-allowed journal
#   6.  Admin user (no allowed list) NOT blocked — sees all
#   7.  account.move create SUCCEEDS with allowed journal
#   8.  account.payment create SUCCEEDS with allowed journal
#   9.  Multiple journals in allowed list (>=2)
#  10.  Res.users.write privilege escalation prevention
#  11.  Constraint catches direct ORM writes
#  12.  Record rule: user can READ allowed journal
#  13.  Record rule: user CANNOT SEE non-allowed journal (HIDDEN, not read-only)

from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError, AccessError


@tagged("post_install", "-at_install")
class TestRestrictJournal(TransactionCase):
    """Test suite for el_restrict_journal — WHITELIST mode."""

    def setUp(self):
        super().setUp()
        self.Users = self.env["res.users"]
        self.Journal = self.env["account.journal"]
        self.Move = self.env["account.move"]
        self.Payment = self.env["account.payment"]

        self.group_user = self.env.ref(
            "el_restrict_journal.group_restrict_journal_user"
        )
        self.group_manager = self.env.ref(
            "el_restrict_journal.group_restrict_journal_manager"
        )

        self.company = self.env.ref("base.main_company")

        # Create two journals: one allowed, one not-allowed
        self.journal_allowed = self.Journal.create(
            {
                "name": "Test Allowed Journal",
                "code": "TAJ",
                "type": "sale",
                "company_id": self.company.id,
            }
        )
        self.journal_not_allowed = self.Journal.create(
            {
                "name": "Test Not-Allowed Journal",
                "code": "TNJ",
                "type": "sale",
                "company_id": self.company.id,
            }
        )

        # Create a regular accountant user (no allowed list yet = unrestricted)
        self.user_accountant = self.Users.create(
            {
                "name": "Test Accountant",
                "login": "test_accountant@example.com",
                "email": "test_accountant@example.com",
                "group_ids": [
                    (6, 0, [
                        self.env.ref("account.group_account_invoice").id,
                    ])
                ],
            }
        )

        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "company_id": self.company.id,
            }
        )

    # ------------------------------------------------------------------
    # Test 1: User allowed_journal_ids field setup
    # ------------------------------------------------------------------
    def test_01_user_allowed_journal_ids_field(self):
        """Test that allowed_journal_ids can be assigned to a user."""
        self.user_accountant.write(
            {"allowed_journal_ids": [(6, 0, [self.journal_allowed.id])]}
        )
        self.assertEqual(
            self.user_accountant.allowed_journal_ids,
            self.journal_allowed,
            "User should have the allowed journal in allowed_journal_ids",
        )
        # User should also be auto-added to group_restrict_journal_user
        self.assertIn(
            self.group_user,
            self.user_accountant.group_ids,
            "User with non-empty allowed_journal_ids should be auto-added "
            "to group_restrict_journal_user",
        )

    # ------------------------------------------------------------------
    # Test 2: account.move create BLOCKED with non-allowed journal
    # ------------------------------------------------------------------
    def test_02_move_create_blocked(self):
        """Test that creating an account.move with a non-allowed journal raises."""
        # Admin allows only journal_allowed for accountant
        self.user_accountant.write(
            {"allowed_journal_ids": [(6, 0, [self.journal_allowed.id])]}
        )
        # Try to create move with the NOT-allowed journal
        with self.assertRaises(ValidationError):
            self.Move.with_user(self.user_accountant.id).create(
                {
                    "journal_id": self.journal_not_allowed.id,
                    "partner_id": self.partner.id,
                    "company_id": self.company.id,
                    "date": "2026-01-01",
                }
            )

    # ------------------------------------------------------------------
    # Test 3: account.move write BLOCKED when switching to non-allowed
    # ------------------------------------------------------------------
    def test_03_move_write_blocked(self):
        """Test that writing an account.move's journal_id to non-allowed raises."""
        self.user_accountant.write(
            {"allowed_journal_ids": [(6, 0, [self.journal_allowed.id])]}
        )
        # Create move with ALLOWED journal (should succeed)
        move = self.Move.with_user(self.user_accountant.id).create(
            {
                "journal_id": self.journal_allowed.id,
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "date": "2026-01-01",
            }
        )
        # Now try to switch to NOT-allowed journal
        with self.assertRaises(ValidationError):
            move.with_user(self.user_accountant.id).write(
                {"journal_id": self.journal_not_allowed.id}
            )

    # ------------------------------------------------------------------
    # Test 4: account.payment create BLOCKED with non-allowed journal
    # ------------------------------------------------------------------
    def test_04_payment_create_blocked(self):
        """Test that creating an account.payment with a non-allowed journal raises."""
        bank_allowed = self.Journal.create(
            {
                "name": "Bank Allowed",
                "code": "BA1",
                "type": "bank",
                "company_id": self.company.id,
            }
        )
        bank_not_allowed = self.Journal.create(
            {
                "name": "Bank Not Allowed",
                "code": "BNA1",
                "type": "bank",
                "company_id": self.company.id,
            }
        )
        self.user_accountant.write(
            {"allowed_journal_ids": [(6, 0, [bank_allowed.id])]}
        )
        with self.assertRaises(ValidationError):
            self.Payment.with_user(self.user_accountant.id).create(
                {
                    "journal_id": bank_not_allowed.id,
                    "payment_type": "inbound",
                    "partner_type": "customer",
                    "partner_id": self.partner.id,
                    "amount": 100.0,
                    "company_id": self.company.id,
                }
            )

    # ------------------------------------------------------------------
    # Test 5: account.payment write BLOCKED when switching to non-allowed
    # ------------------------------------------------------------------
    def test_05_payment_write_blocked(self):
        """Test that writing an account.payment's journal_id to non-allowed raises."""
        bank_allowed = self.Journal.create(
            {
                "name": "Bank Allowed",
                "code": "BA2",
                "type": "bank",
                "company_id": self.company.id,
            }
        )
        bank_not_allowed = self.Journal.create(
            {
                "name": "Bank Not Allowed",
                "code": "BNA2",
                "type": "bank",
                "company_id": self.company.id,
            }
        )
        self.user_accountant.write(
            {"allowed_journal_ids": [(6, 0, [bank_allowed.id])]}
        )
        payment = self.Payment.with_user(self.user_accountant.id).create(
            {
                "journal_id": bank_allowed.id,
                "payment_type": "inbound",
                "partner_type": "customer",
                "partner_id": self.partner.id,
                "amount": 100.0,
                "company_id": self.company.id,
            }
        )
        with self.assertRaises(ValidationError):
            payment.with_user(self.user_accountant.id).write(
                {"journal_id": bank_not_allowed.id}
            )

    # ------------------------------------------------------------------
    # Test 6: Admin user (no allowed list) NOT blocked — sees all
    # ------------------------------------------------------------------
    def test_06_admin_not_restricted(self):
        """Test that admin user (empty allowed_journal_ids) can use any journal."""
        admin = self.env.ref("base.user_admin")
        self.assertFalse(
            admin.allowed_journal_ids,
            "Admin should have no allowed_journal_ids by default",
        )
        # Admin can create with ANY journal (including the "not allowed" one)
        move = self.Move.with_user(admin.id).create(
            {
                "journal_id": self.journal_not_allowed.id,
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "date": "2026-01-01",
            }
        )
        self.assertTrue(move.id, "Admin should be able to create move in any journal")

    # ------------------------------------------------------------------
    # Test 7: account.move create SUCCEEDS with allowed journal
    # ------------------------------------------------------------------
    def test_07_move_create_allowed(self):
        """Test that creating a move with an allowed journal succeeds."""
        self.user_accountant.write(
            {"allowed_journal_ids": [(6, 0, [self.journal_allowed.id])]}
        )
        move = self.Move.with_user(self.user_accountant.id).create(
            {
                "journal_id": self.journal_allowed.id,
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "date": "2026-01-01",
            }
        )
        self.assertTrue(move.id, "Move with allowed journal should be created")

    # ------------------------------------------------------------------
    # Test 8: account.payment create SUCCEEDS with allowed journal
    # ------------------------------------------------------------------
    def test_08_payment_create_allowed(self):
        """Test that creating a payment with an allowed bank journal succeeds."""
        bank_allowed = self.Journal.create(
            {
                "name": "Bank Allowed",
                "code": "BA3",
                "type": "bank",
                "company_id": self.company.id,
            }
        )
        bank_not_allowed = self.Journal.create(
            {
                "name": "Bank Not Allowed",
                "code": "BNA3",
                "type": "bank",
                "company_id": self.company.id,
            }
        )
        self.user_accountant.write(
            {"allowed_journal_ids": [(6, 0, [bank_allowed.id])]}
        )
        payment = self.Payment.with_user(self.user_accountant.id).create(
            {
                "journal_id": bank_allowed.id,
                "payment_type": "inbound",
                "partner_type": "customer",
                "partner_id": self.partner.id,
                "amount": 100.0,
                "company_id": self.company.id,
            }
        )
        self.assertTrue(payment.id, "Payment with allowed journal should be created")

    # ------------------------------------------------------------------
    # Test 9: Multiple journals in allowed list (>=2)
    # ------------------------------------------------------------------
    def test_09_multi_journal_allowed(self):
        """Test that a user can have multiple allowed journals."""
        # Allow two journals
        self.user_accountant.write(
            {
                "allowed_journal_ids": [
                    (6, 0, [self.journal_allowed.id, self.journal_not_allowed.id])
                ]
            }
        )
        self.assertEqual(
            len(self.user_accountant.allowed_journal_ids),
            2,
            "User should have 2 allowed journals",
        )
        # Both should be allowed (no ValidationError)
        move1 = self.Move.with_user(self.user_accountant.id).create(
            {
                "journal_id": self.journal_allowed.id,
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "date": "2026-01-01",
            }
        )
        self.assertTrue(move1.id)
        move2 = self.Move.with_user(self.user_accountant.id).create(
            {
                "journal_id": self.journal_not_allowed.id,
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "date": "2026-01-02",
            }
        )
        self.assertTrue(move2.id)

    # ------------------------------------------------------------------
    # Test 10: Res.users.write privilege escalation prevention
    # ------------------------------------------------------------------
    def test_10_privilege_escalation_prevented(self):
        """Test that a non-manager user cannot edit allowed_journal_ids."""
        with self.assertRaises(AccessError):
            self.user_accountant.with_user(self.user_accountant.id).write(
                {"allowed_journal_ids": [(6, 0, [self.journal_allowed.id])]}
            )

    # ------------------------------------------------------------------
    # Test 11: Constraint catches direct ORM writes
    # ------------------------------------------------------------------
    def test_11_constrains_layer(self):
        """Test that @api.constrains catches the violation."""
        self.user_accountant.write(
            {"allowed_journal_ids": [(6, 0, [self.journal_allowed.id])]}
        )
        with self.assertRaises(ValidationError):
            self.Move.with_user(self.user_accountant.id).create(
                {
                    "journal_id": self.journal_not_allowed.id,
                    "partner_id": self.partner.id,
                    "company_id": self.company.id,
                    "date": "2026-01-01",
                }
            )

    # ------------------------------------------------------------------
    # Test 12: Record rule — user CAN READ allowed journal
    # ------------------------------------------------------------------
    def test_12_record_rule_read_allowed(self):
        """Test that a restricted user can READ their allowed journal."""
        self.user_accountant.write(
            {"allowed_journal_ids": [(6, 0, [self.journal_allowed.id])]}
        )
        journals = self.Journal.with_user(self.user_accountant.id).search(
            [("id", "=", self.journal_allowed.id)]
        )
        self.assertIn(
            self.journal_allowed,
            journals,
            "Restricted user should be able to READ their allowed journal",
        )

    # ------------------------------------------------------------------
    # Test 13: Record rule — user CANNOT SEE non-allowed journal (HIDDEN)
    # ------------------------------------------------------------------
    def test_13_record_rule_non_allowed_hidden(self):
        """Test that a restricted user CANNOT SEE non-allowed journals at all."""
        self.user_accountant.write(
            {"allowed_journal_ids": [(6, 0, [self.journal_allowed.id])]}
        )
        # Search for the non-allowed journal — should return EMPTY
        journals = self.Journal.with_user(self.user_accountant.id).search(
            [("id", "=", self.journal_not_allowed.id)]
        )
        self.assertEqual(
            len(journals),
            0,
            "Restricted user should NOT see non-allowed journals at all "
            "(they should be HIDDEN, not just read-only)",
        )

    # ------------------------------------------------------------------
    # Test 14: Clearing allowed_journal_ids removes user from group
    # ------------------------------------------------------------------
    def test_14_clear_allowed_removes_group(self):
        """Test that clearing allowed_journal_ids auto-removes user from group."""
        # Set allowed list → user in group
        self.user_accountant.write(
            {"allowed_journal_ids": [(6, 0, [self.journal_allowed.id])]}
        )
        self.assertIn(
            self.group_user,
            self.user_accountant.group_ids,
            "User should be in group after setting allowed list",
        )
        # Clear allowed list → user removed from group
        self.user_accountant.write(
            {"allowed_journal_ids": [(5, 0, 0)]}  # Clear all
        )
        self.assertNotIn(
            self.group_user,
            self.user_accountant.group_ids,
            "User should be REMOVED from group after clearing allowed list",
        )
        # User should now see ALL journals (unrestricted)
        journals = self.Journal.with_user(self.user_accountant.id).search([])
        self.assertIn(
            self.journal_not_allowed,
            journals,
            "After clearing allowed list, user should see all journals again",
        )
