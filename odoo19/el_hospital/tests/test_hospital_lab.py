"""Tests for hospital.lab.test + radiology models."""

from odoo.tests import common, tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestHospitalLab(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env['res.partner']
        cls.Patient = cls.env['hospital.patient']
        cls.Physician = cls.env['hospital.physician']
        cls.LabTest = cls.env['hospital.lab.test']
        cls.Radiology = cls.env['hospital.radiology.order']

        cls.partner_doc = cls.Partner.create({'name': 'Dr. Lab Test'})
        cls.physician = cls.Physician.create({
            'partner_id': cls.partner_doc.id,
            'medical_license': 'LIC-LAB-001',
        })
        cls.partner_pat = cls.Partner.create({'name': 'Patient Lab'})
        cls.patient = cls.Patient.create({
            'partner_id': cls.partner_pat.id,
            'physician_id': cls.physician.id,
        })

    def test_01_create_lab_test(self):
        """Test basic lab test creation."""
        lab = self.LabTest.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'test_type': 'blood',
            'test_name': 'Complete Blood Count',
        })
        self.assertTrue(lab.id)
        self.assertEqual(lab.state, 'requested')
        self.assertTrue(lab.name.startswith('LAB/'))

    def test_02_lab_state_requested_to_in_progress(self):
        """Test lab test start."""
        lab = self.LabTest.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'test_name': 'CBC',
        })
        lab.action_start()
        self.assertEqual(lab.state, 'in_progress')

    def test_03_lab_complete_requires_result(self):
        """Test that completing a lab test requires a result."""
        lab = self.LabTest.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'test_name': 'CBC',
        })
        lab.action_start()
        with self.assertRaises(UserError):
            lab.action_complete()

    def test_04_lab_complete_with_result(self):
        """Test completing a lab test with result."""
        lab = self.LabTest.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'test_name': 'CBC',
            'result': 'All values within normal range.',
        })
        lab.action_start()
        lab.action_complete()
        self.assertEqual(lab.state, 'completed')
        self.assertTrue(lab.result_date)

    def test_05_lab_cancel(self):
        """Test cancelling a lab test."""
        lab = self.LabTest.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'test_name': 'CBC',
        })
        lab.action_cancel()
        self.assertEqual(lab.state, 'cancelled')

    def test_06_create_radiology(self):
        """Test basic radiology order creation."""
        rad = self.Radiology.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'modality': 'xray',
            'study_name': 'Chest X-Ray',
        })
        self.assertTrue(rad.id)
        self.assertEqual(rad.state, 'requested')
        self.assertTrue(rad.name.startswith('RAD/'))

    def test_07_radiology_complete(self):
        """Test completing a radiology order."""
        rad = self.Radiology.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'modality': 'ct',
            'study_name': 'Head CT',
            'result': 'No abnormalities detected.',
        })
        rad.action_start()
        rad.action_complete()
        self.assertEqual(rad.state, 'completed')
        self.assertTrue(rad.result_date)

    def test_08_cannot_cancel_completed(self):
        """Test that completed orders cannot be cancelled."""
        rad = self.Radiology.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'modality': 'mri',
            'study_name': 'Brain MRI',
        })
        rad.action_start()
        rad.action_complete()
        with self.assertRaises(UserError):
            rad.action_cancel()
