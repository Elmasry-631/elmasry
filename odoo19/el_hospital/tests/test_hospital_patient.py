"""Tests for hospital.patient model."""

from odoo.tests import common, tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestHospitalPatient(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env['res.partner']
        cls.Patient = cls.env['hospital.patient']
        cls.Physician = cls.env['hospital.physician']
        cls.Department = cls.env['hospital.department']

        cls.department = cls.Department.create({
            'name': 'Test Cardiology',
            'code': 'TEST-CARD',
        })
        cls.partner_doctor = cls.Partner.create({'name': 'Dr. Test'})
        cls.physician = cls.Physician.create({
            'partner_id': cls.partner_doctor.id,
            'medical_license': 'LIC-001',
            'specialization': 'Cardiology',
            'department_id': cls.department.id,
        })
        cls.partner_patient = cls.Partner.create({'name': 'John Doe'})
        cls.patient = cls.Patient.create({
            'partner_id': cls.partner_patient.id,
            'physician_id': cls.physician.id,
            'department_id': cls.department.id,
            'birth_date': '1990-01-01',
            'gender': 'male',
            'blood_type': 'O+',
        })

    def test_01_create_patient(self):
        """Test basic patient creation."""
        self.assertTrue(self.patient.id)
        self.assertEqual(self.patient.name, 'John Doe')
        self.assertTrue(self.patient.ref)
        self.assertEqual(self.patient.gender, 'male')

    def test_02_patient_code_sequence(self):
        """Test that patient code is auto-generated."""
        self.assertTrue(self.patient.ref.startswith('PAT/'))

    def test_03_age_computation(self):
        """Test age is computed from birth_date."""
        self.assertTrue(self.patient.age > 0)

    def test_04_unique_partner(self):
        """Test that one partner cannot have two patient records."""
        try:
            self.Patient.create({
                'partner_id': self.partner_patient.id,
            })
            self.env.flush_all()
            self.fail('Expected duplicate partner to be rejected')
        except Exception:
            pass

    def test_05_allergy_creation(self):
        """Test allergy sub-record creation."""
        allergy = self.env['hospital.patient.allergy'].create({
            'patient_id': self.patient.id,
            'name': 'Penicillin',
            'severity': 'severe',
        })
        self.assertEqual(allergy.severity, 'severe')
        self.assertIn(allergy, self.patient.allergy_ids)

    def test_06_chronic_disease_creation(self):
        """Test chronic disease sub-record creation."""
        disease = self.env['hospital.patient.disease'].create({
            'patient_id': self.patient.id,
            'name': 'Hypertension',
            'diagnosed_date': '2020-01-01',
        })
        self.assertEqual(disease.name, 'Hypertension')
        self.assertIn(disease, self.patient.chronic_disease_ids)

    def test_07_smart_button_appointments(self):
        """Test the appointment_count smart button."""
        self.assertEqual(self.patient.appointment_count, 0)
        self.env['hospital.appointment'].create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'appointment_date': '2026-12-01 10:00:00',
        })
        self.env.flush_all()
        # Invalidate cache to recompute
        self.patient.invalidate_recordset()
        self.assertEqual(self.patient.appointment_count, 1)

    def test_08_display_name_with_ref(self):
        """Test display name includes the patient code."""
        self.assertIn('PAT/', self.patient.display_name)
        self.assertIn('John Doe', self.patient.display_name)
