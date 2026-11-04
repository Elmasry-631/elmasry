"""Tests for hospital.admission + bed management."""

from odoo.tests import common, tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install')
class TestHospitalAdmission(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Partner = cls.env['res.partner']
        cls.Patient = cls.env['hospital.patient']
        cls.Physician = cls.env['hospital.physician']
        cls.Department = cls.env['hospital.department']
        cls.Ward = cls.env['hospital.ward']
        cls.Bed = cls.env['hospital.bed']
        cls.Admission = cls.env['hospital.admission']

        cls.department = cls.Department.create({'name': 'Test Adm Dept', 'code': 'TAD01'})
        cls.partner_doc = cls.Partner.create({'name': 'Dr. Adm Test'})
        cls.physician = cls.Physician.create({
            'partner_id': cls.partner_doc.id,
            'medical_license': 'LIC-ADM-001',
        })
        cls.partner_pat = cls.Partner.create({'name': 'Patient Adm'})
        cls.patient = cls.Patient.create({
            'partner_id': cls.partner_pat.id,
            'physician_id': cls.physician.id,
        })
        cls.ward = cls.Ward.create({
            'name': 'Test Ward',
            'code': 'TW01',
            'ward_type': 'general',
            'bed_capacity': 5,
        })
        cls.bed = cls.Bed.create({
            'ward_id': cls.ward.id,
            'bed_number': '01',
        })

    def test_01_create_admission(self):
        """Test basic admission creation."""
        adm = self.Admission.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'ward_id': self.ward.id,
            'bed_id': self.bed.id,
        })
        self.assertTrue(adm.id)
        self.assertEqual(adm.state, 'draft')
        self.assertTrue(adm.name.startswith('ADM/'))

    def test_02_admit_sets_bed_occupied(self):
        """Test that admitting a patient reserves the bed."""
        adm = self.Admission.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'ward_id': self.ward.id,
            'bed_id': self.bed.id,
        })
        adm.action_admit()
        self.assertEqual(adm.state, 'admitted')
        self.assertEqual(self.bed.state, 'occupied')
        self.assertEqual(self.bed.admission_id, adm)

    def test_03_discharge_frees_bed(self):
        """Test that discharging a patient frees the bed."""
        adm = self.Admission.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'ward_id': self.ward.id,
            'bed_id': self.bed.id,
        })
        adm.action_admit()
        adm.action_discharge()
        self.assertEqual(adm.state, 'discharged')
        self.assertEqual(self.bed.state, 'available')
        self.assertFalse(self.bed.admission_id)
        self.assertTrue(adm.discharge_date)

    def test_04_days_count(self):
        """Test that days_count is computed."""
        adm = self.Admission.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'ward_id': self.ward.id,
            'bed_id': self.bed.id,
        })
        adm.action_admit()
        adm.action_discharge()
        self.env.flush_all()
        self.assertTrue(adm.days_count >= 0)

    def test_05_cannot_admit_without_bed(self):
        """Test that admission without bed fails on admit."""
        adm = self.Admission.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'ward_id': self.ward.id,
        })
        with self.assertRaises(UserError):
            adm.action_admit()

    def test_06_cancel_frees_bed(self):
        """Test that cancelling an admitted admission frees the bed."""
        adm = self.Admission.create({
            'patient_id': self.patient.id,
            'physician_id': self.physician.id,
            'ward_id': self.ward.id,
            'bed_id': self.bed.id,
        })
        adm.action_admit()
        adm.action_cancel()
        self.assertEqual(adm.state, 'cancelled')
        self.assertEqual(self.bed.state, 'available')

    def test_07_bed_maintenance(self):
        """Test bed maintenance state."""
        self.assertEqual(self.bed.state, 'available')
        self.bed.action_set_maintenance()
        self.assertEqual(self.bed.state, 'maintenance')
        self.bed.action_set_available()
        self.assertEqual(self.bed.state, 'available')

    def test_08_ward_stats(self):
        """Test ward bed statistics computation."""
        self.env['hospital.bed'].create({
            'ward_id': self.ward.id,
            'bed_number': '02',
        })
        self.env.flush_all()
        self.assertEqual(self.ward.bed_count, 2)
        self.assertEqual(self.ward.available_count, 2)
        self.assertEqual(self.ward.occupied_count, 0)
