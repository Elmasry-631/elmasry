# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrAttendanceChangeDataWizard(models.TransientModel):
    _name = 'hr.attendance.change.data.wizard'
    _description = 'Change Attendance Data Wizard'

    sheet_line_id = fields.Many2one(
        'hr.attendance.sheet.line',
        string='Sheet Line',
        required=True,
    )
    new_overtime_hours = fields.Float(string='New Overtime Hours')
    new_late_in_minutes = fields.Float(string='New Late In (minutes)')
    new_difference_hours = fields.Float(string='New Difference Hours')
    reason = fields.Text(
        string='Reason for Change',
        required=True,
    )

    def action_apply(self):
        self.ensure_one()
        if not self.reason:
            raise UserError(_("A reason for the change is required."))
        line = self.sheet_line_id
        if line.sheet_id.state != 'computed':
            raise UserError(_(
                "Sheet %s must be in Computed state to change line data."
            ) % line.sheet_id.name)
        old_note = line.note or ""
        new_note = _("%s\n[Changed by %s] Overtime: %s → %s, "
                     "Late: %s → %s, Diff: %s → %s\nReason: %s") % (
            old_note,
            self.env.user.name,
            line.overtime_hours, self.new_overtime_hours,
            line.late_in_minutes, self.new_late_in_minutes,
            line.difference_hours, self.new_difference_hours,
            self.reason,
        )
        line.write({
            'overtime_hours': self.new_overtime_hours,
            'late_in_minutes': self.new_late_in_minutes,
            'difference_hours': self.new_difference_hours,
            'note': new_note,
            'changed_manually': True,
        })
        return {'type': 'ir.actions.act_window_close'}
