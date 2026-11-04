# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Ranjith R(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.

###############################################################################
import json
import logging

from odoo import http
from odoo.http import content_disposition, request
_logger = logging.getLogger(__name__)


class InventoryReportGenerator(http.Controller):
    """Controller for handling dynamic inventory report exports in XLSX format.
    This controller provides an HTTP endpoint for generating and exporting
    dynamic inventory reports in XLSX format. It takes input options and
    report data, creates an XLSX report, and sends it as an HTTP response."""

    @http.route('/inventory_dynamic_xlsx_reports', type='http', auth='user',
                methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_data,
                        report_name, dfr_data, **kw):
        """Generate and export a dynamic inventory report in XLSX format.
           This method handles the generation and export of dynamic inventory
           reports in XLSX format. It takes various parameters like the report
           model, export options, output format, and report data.
           model: The report model for which the report is generated.
           options: The export options and configuration.
           output_format: The desired output format, such as 'xlsx'.
           report_data: The data to be included in the report.
           report_name: The name of the generated report file.
           dfr_data: Additional data for report generation.
           kw: Additional keyword arguments.
           return: An HTTP response containing the generated XLSX report."""
        token = 'dummy-because-api-expects-one'
        if model != 'dynamic.inventory.report':
            return request.make_response(
                json.dumps({'error': 'Invalid report model.'}),
                headers=[('Content-Type', 'application/json')], status=400
            )
        if output_format != 'xlsx':
            return request.make_response(
                json.dumps({'error': 'Unsupported report format.'}),
                headers=[('Content-Type', 'application/json')], status=400
            )

        try:
            report_obj = request.env[model]
            response = request.make_response(
                None,
                headers=[
                    ('Content-Type',
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    ('Content-Disposition',
                     content_disposition(str(report_name or 'Inventory Report')
                                         + '.xlsx'))
                ]
            )
            report_obj.get_inventory_xlsx_report(
                options, response, report_data, dfr_data
            )
            response.set_cookie('fileToken', token)
            return response
        except Exception:
            _logger.exception(
                'Failed to generate the dynamic inventory XLSX report'
            )
            error = {
                'code': 500,
                'message': 'Unable to generate the inventory report.',
            }
            return request.make_response(
                json.dumps(error),
                headers=[('Content-Type', 'application/json')], status=500
            )
