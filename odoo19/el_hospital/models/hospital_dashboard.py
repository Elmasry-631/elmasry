"""Hospital Dashboard model — transient model for the dashboard view."""

from odoo import api, fields, models, _
from collections import defaultdict


class HospitalDashboard(models.Model):
    """Transient dashboard model — provides KPIs for the OWL dashboard."""

    _name = 'hospital.dashboard'
    _description = 'Hospital Dashboard'
    _transient = True

    # ─── KPI fields (computed, not stored) ────────────────────────────
    total_patients = fields.Integer(compute='_compute_kpis')
    total_physicians = fields.Integer(compute='_compute_kpis')
    total_appointments_today = fields.Integer(compute='_compute_kpis')
    total_active_admissions = fields.Integer(compute='_compute_kpis')
    total_beds = fields.Integer(compute='_compute_kpis')
    occupied_beds = fields.Integer(compute='_compute_kpis')
    available_beds = fields.Integer(compute='_compute_kpis')
    bed_occupancy_rate = fields.Float(compute='_compute_kpis', help='Percentage 0-100')
    pending_lab_tests = fields.Integer(compute='_compute_kpis')
    pending_radiology = fields.Integer(compute='_compute_kpis')
    monthly_revenue = fields.Monetary(compute='_compute_kpis')
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=lambda self: self.env.company.currency_id,
    )

    def _compute_kpis(self):
        for rec in self:
            rec.total_patients = self.env['hospital.patient'].search_count([])
            rec.total_physicians = self.env['hospital.physician'].search_count([])
            # Today's appointments
            today = fields.Datetime.today()
            rec.total_appointments_today = self.env['hospital.appointment'].search_count([
                ('appointment_date', '>=', today.replace(hour=0, minute=0, second=0)),
                ('appointment_date', '<=', today.replace(hour=23, minute=59, second=59)),
            ])
            rec.total_active_admissions = self.env['hospital.admission'].search_count([
                ('state', '=', 'admitted'),
            ])
            beds = self.env['hospital.bed'].search([])
            rec.total_beds = len(beds)
            rec.occupied_beds = len(beds.filtered(lambda b: b.state == 'occupied'))
            rec.available_beds = len(beds.filtered(lambda b: b.state == 'available'))
            rec.bed_occupancy_rate = (rec.occupied_beds / rec.total_beds * 100) if rec.total_beds else 0.0
            rec.pending_lab_tests = self.env['hospital.lab.test'].search_count([
                ('state', 'in', ['requested', 'in_progress']),
            ])
            rec.pending_radiology = self.env['hospital.radiology.order'].search_count([
                ('state', 'in', ['requested', 'in_progress']),
            ])
            # Monthly revenue
            from datetime import date
            month_start = date.today().replace(day=1)
            billings = self.env['hospital.invoice.billing'].search([
                ('billing_date', '>=', month_start),
                ('state', '=', 'paid'),
            ])
            rec.monthly_revenue = sum(billings.mapped('amount_total'))

    @api.model
    def get_dashboard_data(self):
        """Return all dashboard data as a dict (for the JSON endpoint)."""
        dash = self.create({})
        return {
            'kpi': {
                'total_patients': dash.total_patients,
                'total_physicians': dash.total_physicians,
                'appointments_today': dash.total_appointments_today,
                'active_admissions': dash.total_active_admissions,
                'total_beds': dash.total_beds,
                'occupied_beds': dash.occupied_beds,
                'available_beds': dash.available_beds,
                'bed_occupancy_rate': round(dash.bed_occupancy_rate, 1),
                'pending_lab_tests': dash.pending_lab_tests,
                'pending_radiology': dash.pending_radiology,
                'monthly_revenue': dash.monthly_revenue,
                'currency': dash.currency_id.name,
            },
            'charts': self._get_chart_data(),
        }

    @api.model
    def _get_chart_data(self):
        """Aggregate data for charts."""
        # Appointments by department
        appointments = self.env['hospital.appointment'].read_group(
            [('state', 'in', ['confirmed', 'done'])],
            ['department_id', 'id:count'],
            ['department_id'],
        )
        dept_labels = []
        dept_values = []
        for appt in appointments:
            dept = appt.get('department_id')
            label = dept[1] if dept and isinstance(dept, (list, tuple)) else _('No Department')
            dept_labels.append(label)
            dept_values.append(appt.get('department_id_count', 0))

        # Admissions by state (last 30 days)
        from datetime import timedelta
        date_30 = fields.Date.context_today(self) - timedelta(days=30)
        admissions = self.env['hospital.admission'].read_group(
            [('admission_date', '>=', date_30)],
            ['state', 'id:count'],
            ['state'],
        )
        adm_labels = []
        adm_values = []
        for adm in admissions:
            state = adm.get('state', 'unknown')
            adm_labels.append(state)
            adm_values.append(adm.get('state_count', 0))

        # Bed occupancy by ward type
        beds = self.env['hospital.bed'].search([])
        ward_type_counts = defaultdict(lambda: {'available': 0, 'occupied': 0, 'maintenance': 0})
        for bed in beds:
            ward_type = bed.ward_id.ward_type if bed.ward_id else 'general'
            ward_type_counts[ward_type][bed.state] += 1

        ward_labels = list(ward_type_counts.keys())
        ward_available = [v['available'] for v in ward_type_counts.values()]
        ward_occupied = [v['occupied'] for v in ward_type_counts.values()]

        return {
            'appointments_by_dept': {
                'labels': dept_labels,
                'values': dept_values,
            },
            'admissions_by_state': {
                'labels': adm_labels,
                'values': adm_values,
            },
            'beds_by_ward_type': {
                'labels': ward_labels,
                'available': ward_available,
                'occupied': ward_occupied,
            },
        }
