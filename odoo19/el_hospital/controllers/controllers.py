"""Hospital controller — JSON endpoint for the dashboard."""

import logging

from odoo import http
from odoo.http import request, route

_logger = logging.getLogger(__name__)


class HospitalController(http.Controller):
    """JSON endpoints for the hospital dashboard."""

    @route(
        '/hospital/dashboard/data',
        type='jsonrpc',
        auth='user',
        methods=['POST', 'GET'],
        csrf=False,
    )
    def get_dashboard_data(self, **kwargs):
        """Return all dashboard data for the current user.

        Response shape:
            {
                'kpi': {
                    'total_patients': int,
                    'total_physicians': int,
                    'appointments_today': int,
                    'active_admissions': int,
                    'total_beds': int,
                    'occupied_beds': int,
                    'available_beds': int,
                    'bed_occupancy_rate': float,
                    'pending_lab_tests': int,
                    'pending_radiology': int,
                    'monthly_revenue': float,
                    'currency': str,
                },
                'charts': {
                    'appointments_by_dept': {'labels': [], 'values': []},
                    'admissions_by_state': {'labels': [], 'values': []},
                    'beds_by_ward_type': {'labels': [], 'available': [], 'occupied': []},
                },
            }
        """
        if not request.env.user.has_group('el_hospital.group_hospital_user'):
            return {'error': 'Permission denied'}
        try:
            return request.env['hospital.dashboard'].get_dashboard_data()
        except Exception as exc:
            _logger.exception('[Hospital] get_dashboard_data failed: %s', exc)
            return {'error': str(exc)}
