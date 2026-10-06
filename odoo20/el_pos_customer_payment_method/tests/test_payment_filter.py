# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestElPosPaymentMethodFilter(TransactionCase):
    """Backend-side guarantees of the customer payment method feature.

    The live button filtering itself lives in the OWL payment screen patch
    (static/src/js/payment_screen.js); these tests lock down the data
    contract that patch relies on.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env["res.partner"]
        cls.PosConfig = cls.env["pos.config"]
        cls.PaymentMethod = cls.env["pos.payment.method"]

        cls.cash_method = cls.PaymentMethod.create(
            {"name": "EL Cash", "type": "pay_later"}
        )
        cls.bank_method = cls.PaymentMethod.create(
            {"name": "EL Bank", "type": "pay_later"}
        )
        cls.config = cls.PosConfig.create(
            {
                "name": "EL Test Shop",
                "el_pos_default_payment_method_ids": [
                    (6, 0, cls.bank_method.ids)
                ],
            }
        )
        config_methods = cls.config.payment_method_ids
        if cls.bank_method not in config_methods:
            cls.config.payment_method_ids = [
                (4, cls.bank_method.id, 0)
            ]
        cls.partner_with_list = cls.Partner.create(
            {
                "name": "EL Restricted Customer",
                "el_allowed_pos_payment_method_ids": [
                    (6, 0, cls.bank_method.ids)
                ],
            }
        )
        cls.partner_plain = cls.Partner.create({"name": "EL Free Customer"})

    def test_01_partner_field_stored(self):
        """The many2many on res.partner persists the allowed methods."""
        self.assertEqual(
            self.partner_with_list.el_allowed_pos_payment_method_ids,
            self.bank_method,
        )
        self.assertFalse(
            self.partner_plain.el_allowed_pos_payment_method_ids
        )

    def test_02_pos_data_fields_include_allowed_methods(self):
        """res.partner exposes the fields the payment screen filters on."""
        fields = self.Partner._load_pos_data_fields(self.config)
        self.assertIn("el_allowed_pos_payment_method_ids", fields)
        # Needed by the JS fallback when the order partner is a child
        # (invoice) address rather than the record holding the restriction.
        self.assertIn("commercial_partner_id", fields)

    def test_03_child_partner_resolves_to_commercial_partner(self):
        """A child address carries no list but points at the restricted one."""
        child = self.Partner.create(
            {
                "name": "EL Restricted Customer Invoice Address",
                "type": "invoice",
                "parent_id": self.partner_with_list.id,
            }
        )
        fields = self.Partner._load_pos_data_fields(self.config)
        data = child.read(fields, load=False)[0]
        self.assertEqual(
            data["commercial_partner_id"], self.partner_with_list.id
        )
        self.assertFalse(data["el_allowed_pos_payment_method_ids"])
        self.assertEqual(
            self.partner_with_list.read(fields, load=False)[0][
                "el_allowed_pos_payment_method_ids"
            ],
            self.bank_method.ids,
        )

    def test_04_partner_data_read_returns_method_ids(self):
        """A partner read with POS fields carries the allowed method ids."""
        fields = self.Partner._load_pos_data_fields(self.config)
        data = self.partner_with_list.read(fields, load=False)
        self.assertEqual(
            data[0]["el_allowed_pos_payment_method_ids"],
            self.bank_method.ids,
        )

    def test_05_pos_config_defaults_field_loaded(self):
        """The POS config loads its default methods field automatically.

        The POS reads the config with an empty field list, which the ORM
        resolves to every accessible field; assert the default methods
        survive a full read.
        """
        data = self.config.read([])[0]
        self.assertIn("el_pos_default_payment_method_ids", data)
        self.assertEqual(
            data["el_pos_default_payment_method_ids"], self.bank_method.ids
        )

    def test_06_settings_related_field_roundtrip(self):
        """The settings related field writes through to the POS config."""
        Settings = self.env["res.config.settings"]
        settings = Settings.create({"pos_config_id": self.config.id})
        settings.pos_el_default_payment_method_ids = [
            (6, 0, self.cash_method.ids)
        ]
        self.assertEqual(
            self.config.el_pos_default_payment_method_ids,
            self.cash_method,
        )
