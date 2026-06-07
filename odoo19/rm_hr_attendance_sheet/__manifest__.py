{
    "name": "HR Attendance Sheet and Policies",
    "version": "19.0.1.0.0",
    "summary": "Attendance sheets, policies, overtime, lateness, absence, and payroll links",
    "description": """
        Policy-driven attendance sheets for Odoo 19 with overtime, lateness,
        absence, public holiday handling, batch sheet creation, manual change
        audit notes, and payslip linkage.
    """,
    "category": "Human Resources/Attendances",
    "author": "Ibrahim Elmasry",
    "depends": [
        "hr_attendance",
        "hr_holidays",
        "hr_payroll",
        "mail",
    ],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "data/hr_salary_rule_data.xml",
        "views/rm_overtime_rule_views.xml",
        "views/rm_lateness_rule_views.xml",
        "views/rm_absence_rule_views.xml",
        "views/rm_attendance_policy_views.xml",
        "views/rm_attendance_sheet_views.xml",
        "views/hr_version_views.xml",
        "views/resource_calendar_leaves_views.xml",
        "views/hr_payslip_views.xml",
        "wizards/rm_attendance_sheet_change_views.xml",
        "wizards/rm_attendance_sheet_batch_views.xml",
        "views/hr_menu.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
