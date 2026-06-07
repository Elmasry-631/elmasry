from odoo import fields, models
from odoo.exceptions import UserError


class RmAttendanceSheetChangeWizard(models.TransientModel):
    _name = "rm.attendance.sheet.change.wizard"
    _description = "Modify Attendance Sheet Line"

    sheet_id = fields.Many2one("rm.attendance.sheet", required=True)
    line_id = fields.Many2one(
        "rm.attendance.sheet.line",
        required=True,
        domain="[('sheet_id', '=', sheet_id)]",
    )
    overtime_hours = fields.Float()
    late_in_minutes = fields.Float()
    difference_hours = fields.Float()
    is_absent = fields.Boolean()
    reason = fields.Text(required=True)

    def action_apply(self):
        self.ensure_one()
        if self.sheet_id.state != "draft":
            raise UserError(self.env._("Attendance changes are only allowed in draft state."))
        if not self.reason:
            raise UserError(self.env._("A reason is required."))
        self.line_id.write(
            {
                "overtime_hours": self.overtime_hours,
                "late_in_minutes": self.late_in_minutes,
                "difference_hours": self.difference_hours,
                "is_absent": self.is_absent,
                "change_note": self.reason,
                "changed_by": self.env.user.id,
                "changed_date": fields.Datetime.now(),
            }
        )
        self.sheet_id.message_post(
            body=self.env._(
                "Attendance line %(date)s was changed by %(user)s. Reason: %(reason)s",
                date=self.line_id.date,
                user=self.env.user.display_name,
                reason=self.reason,
            )
        )
        return {"type": "ir.actions.act_window_close"}

    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        if values.get("line_id"):
            line = self.env["rm.attendance.sheet.line"].browse(values["line_id"])
            values.update(
                {
                    "overtime_hours": line.overtime_hours,
                    "late_in_minutes": line.late_in_minutes,
                    "difference_hours": line.difference_hours,
                    "is_absent": line.is_absent,
                }
            )
        return values
