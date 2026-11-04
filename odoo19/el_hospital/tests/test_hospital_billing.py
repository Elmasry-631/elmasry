"""Tests for hospital.invoice.billing model."""

from odoo.tests import common, tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestHospitalBilling(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env['res.partner']
        cls.Patient = cls.env['hospital.patient']
        cls.Physician = cls.env['hospital.physician']
        cls.Billing = cls.env['hospital.invoice.billing']
        cls.BillingLine = cls.env['hospital.invoice.billing.line']

        cls.partner_doc = cls.Partner.create({'name': 'Dr. Billing Test'})
        cls.physician = cls.Physician.create({
            'partner_id': cls.partner_doc.id,
            'medical_license': 'LIC-BILL-001',
        })
        cls.partner_pat = cls.Partner.create({'name': 'Patient Billing'})
        cls.patient = cls.Patient.create({
            'partner_id': cls.partner_pat.id,
            'physician_id': cls.physician.id,
        })

    def test_01_create_billing(self):
        """Test basic billing creation."""
        bill = self.Billing.create({
            'patient_id': self.patient.id,
        })
        self.assertTrue(bill.id)
        self.assertEqual(bill.state, 'draft')
        self.assertTrue(bill.name.startswith('BILL/'))

    def test_02_line_subtotal(self):
        """Test that line subtotal is computed correctly."""
        bill = self.Billing.create({'patient_id': self.patient.id})
        line = self.BillingLine.create({
            'billing_id': bill.id,
            'name': 'Consultation Fee',
            'quantity': 2.0,
            'price_unit': 150.0,
        })
        self.assertEqual(line.price_subtotal, 300.0)

    def test_03_billing_total(self):
        """Test that billing total is the sum of line subtotals."""
        bill = self.Billing.create({'patient_id': self.patient.id})
        self.BillingLine.create({
            'billing_id': bill.id,
            'name': 'Consultation',
            'quantity': 1.0,
            'price_unit': 200.0,
        })
        self.BillingLine.create({
            'billing_id': bill.id,
            'name': 'Lab Test',
            'quantity': 1.0,
            'price_unit': 100.0,
        })
        self.env.flush_all()
        self.assertEqual(bill.amount_total, 300.0)

    def test_04_cannot_invoice_empty(self):
        """Test that invoicing without lines fails."""
        bill = self.Billing.create({'patient_id': self.patient.id})
        with self.assertRaises(UserError):
            bill.action_create_invoice()

    def test_05_create_invoice(self):
        """Test creating an account.move from billing."""
        bill = self.Billing.create({'patient_id': self.patient.id})
        self.BillingLine.create({
            'billing_id': bill.id,
            'name': 'Consultation',
            'quantity': 1.0,
            'price_unit': 250.0,
        })
        bill.action_create_invoice()
        self.assertEqual(bill.state, 'invoiced')
        self.assertTrue(bill.move_id.id)
        self.assertEqual(bill.move_id.partner_id, self.partner_pat)

    def test_06_cannot_invoice_twice(self):
        """Test that an invoiced billing cannot be re-invoiced."""
        bill = self.Billing.create({'patient_id': self.patient.id})
        self.BillingLine.create({
            'billing_id': bill.id,
            'name': 'Service',
            'quantity': 1.0,
            'price_unit': 100.0,
        })
        bill.action_create_invoice()
        with self.assertRaises(UserError):
            bill.action_create_invoice()
