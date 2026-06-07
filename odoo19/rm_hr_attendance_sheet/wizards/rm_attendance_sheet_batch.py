from odoo import fields, models
from odoo.exceptions import UserError


class RmAttendanceSheetBatchWizard(models.TransientModel):
    _name = "rm.attendance.sheet.batch.wizard"
    _description = "Batch Create Attendance Sheets"

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    department_id = fields.Many2one("hr.department")
    employee_ids = fields.Many2many("hr.employee", string="Employees")
    employee_category_ids = fields.Many2many("hr.employee.category", string="Employee Tags")
    calculate_now = fields.Boolean(default=True)
    summary = fields.Text(readonly=True)

    def action_create_sheets(self):
        self.ensure_one()
        if self.date_from > self.date_to:
            raise UserError(self.env._("Period start must be before period end."))
        domain = [("active", "=", True)]
        if self.department_id:
            domain.append(("department_id", "child_of", self.department_id.id))
        if self.employee_ids:
            domain.append(("id", "in", self.employee_ids.ids))
        if self.employee_category_ids:
            domain.append(("category_ids", "in", self.employee_category_ids.ids))
        employees = self.env["hr.employee"].search(domain)
        sheet_model = self.env["rm.attendance.sheet"]
        created = sheet_model
        skipped = []
        errors = []
        for employee in employees:
            version = sheet_model._find_version(employee, self.date_from)
            if not version:
                skipped.append(f"{employee.name}: no active employee record")
                continue
            duplicate = sheet_model.search(
                [
                    ("employee_id", "=", employee.id),
                    ("date_from", "=", self.date_from),
                    ("date_to", "=", self.date_to),
                    ("state", "!=", "cancelled"),
                ],
                limit=1,
            )
            if duplicate:
                skipped.append(f"{employee.name}: duplicate sheet")
                continue
            try:
                sheet = sheet_model.create(
                    {
                        "employee_id": employee.id,
                        "version_id": version.id,
                        "date_from": self.date_from,
                        "date_to": self.date_to,
                    }
                )
                if self.calculate_now:
                    sheet.action_calculate()
                created |= sheet
            except Exception as exc:
                errors.append(f"{employee.name}: {exc}")
        self.summary = self.env._(
            "Created: %(created)s\nSkipped: %(skipped)s\nErrors: %(errors)s",
            created=len(created),
            skipped=len(skipped),
            errors=len(errors),
        )
        if created:
            return {
                "type": "ir.actions.act_window",
                "name": self.env._("Attendance Sheets"),
                "res_model": "rm.attendance.sheet",
                "view_mode": "list,form",
                "domain": [("id", "in", created.ids)],
            }
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }
