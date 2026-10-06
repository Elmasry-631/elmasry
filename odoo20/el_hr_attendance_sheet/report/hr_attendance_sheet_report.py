# -*- coding: utf-8 -*-
from odoo import models


class HrAttendanceSheetReport(models.AbstractModel):
    _name = 'report.el_hr_attendance_sheet.report_hr_attendance_sheet'
    _description = 'HR Attendance Sheet Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.attendance.sheet'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'hr.attendance.sheet',
            'docs': docs,
            'data': data or {},
        }
