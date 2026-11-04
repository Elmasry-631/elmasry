"""Tests for hospital.appointment model."""

from odoo.tests import common, tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestHospitalAppointment(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env['res.partner']
        cls.Patient = cls.env['hospital.patient']
        cls.Physician = cls.env['hospital.physician']
        cls.Department = cls.env['hospital.department']
        cls.Appointment = cls.env['hospital.appointment']

        cls.department = cls.Department.create({'name': 'Test Dept', 'code': 'TD01'})
        cls.partner_doc = cls.Partner.create({'name': 'Dr. Appointment Test'})
        cls.physician = cls.Physician.create({
            'partner_id': cls.partner_doc.id,
            'medical_license': 'LIC-APPT-001',
        })
        cls.partner_pat = cls.Partner.create({'name': 'Patient Appt'})
        cls.patient = cls.Patient.create({
            'partner_id': cls.partner_pat.id,
            'physician_id': cls.physician.id,
        })

    def test_01_create_appointment(self):
        """Test basic appointment creation."""
        appt = self.Appointment.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'appointment_date': '2026-12-01 10:00:00',
        })
        self.assertTrue(appt.id)
        self.assertEqual(appt.state, 'draft')
        self.assertTrue(appt.name.startswith('AP/'))

    def test_02_state_draft_to_confirmed(self):
        """Test appointment confirmation."""
        appt = self.Appointment.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'appointment_date': '2026-12-01 10:00:00',
        })
        appt.action_confirm()
        self.assertEqual(appt.state, 'confirmed')

    def test_03_state_confirmed_to_done(self):
        """Test marking appointment as done."""
        appt = self.Appointment.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'appointment_date': '2026-12-01 10:00:00',
        })
        appt.action_confirm()
        appt.action_done()
        self.assertEqual(appt.state, 'done')

    def test_04_done_creates_medical_record(self):
        """Test that marking done auto-creates a medical record."""
        appt = self.Appointment.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'appointment_date': '2026-12-01 10:00:00',
        })
        appt.action_confirm()
        appt.action_done()
        self.assertTrue(appt.medical_record_id.id)
        self.assertEqual(appt.medical_record_id.patient_id, self.patient)

    def test_05_cancel_appointment(self):
        """Test appointment cancellation."""
        appt = self.Appointment.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'appointment_date': '2026-12-01 10:00:00',
        })
        appt.action_confirm()
        appt.action_cancel()
        self.assertEqual(appt.state, 'cancelled')

    def test_06_cannot_cancel_done(self):
        """Test that done appointments cannot be cancelled."""
        appt = self.Appointment.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'appointment_date': '2026-12-01 10:00:00',
        })
        appt.action_confirm()
        appt.action_done()
        with self.assertRaises(UserError):
            appt.action_cancel()

    def test_07_reset_to_draft(self):
        """Test resetting cancelled appointment to draft."""
        appt = self.Appointment.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'appointment_date': '2026-12-01 10:00:00',
        })
        appt.action_confirm()
        appt.action_cancel()
        appt.action_draft()
        self.assertEqual(appt.state, 'draft')
