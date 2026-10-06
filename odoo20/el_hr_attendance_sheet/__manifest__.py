# -*- coding: utf-8 -*-
{
    'name': 'HR Attendance Sheet And Policies',
    'version': '20.0.1.0.1',
    'author': 'Ibrahim Elmasry',
    'summary': 'Calculate overtime, lateness, absence from attendance and feed payslip',
    'description': """
HR Attendance Sheet And Policies
=================================

One place to calculate overtime, absence and attendance.

Features
--------
* Public holidays definition with employee/department/tag scoping
* Configurable overtime rules per type (working day, weekend, public holiday)
* Multi-step lateness penalty matrix (rate or amount based)
* Multi-step absence penalty rules
* Escalation tiers per repetition level (1st, 2nd, 3rd... lateness/absence)
* Lateness step ranges configurable in hours or minutes
* Attendance policy aggregator linked to employee contract
* Attendance sheet per employee per period with day-by-day breakdown
* Handles multi working intervals in one day
* Handles overlapping attendance records
* Wizard to manually modify computed values with reason note
* Create payslip directly from attendance sheet
* Salary rules + structure for attendance inputs (OVERT, LATE, ABS, DIFF)
* Batch generation by department
* Multi-company aware via hr.version.company_id
* Full chatter + activity mixin on transactional models
* PDF report for attendance sheet

Author
------
Ibrahim Elmasry
    """,
    'depends': [
        'base',
        'hr_attendance',
        'hr',
        'hr_payroll',
        'hr_holidays',
        'mail',
        'calendar',
    ],
    'data': [
        # 1. Security FIRST
        'security/hr_attendance_sheet_groups.xml',
        'security/ir.access.csv',
        # 2. Data SECOND (sequences, salary rules, structure)
        'data/ir_sequence_data.xml',
        'data/hr_payroll_structure_data.xml',
        'data/hr_salary_rule_data.xml',
        'data/hr_structure_attendance_rules_action.xml',
        # 3. Views THIRD
        'views/hr_attendance_public_holiday_views.xml',
        'views/hr_attendance_rule_views.xml',
        'views/hr_attendance_policy_views.xml',
        'views/hr_attendance_sheet_views.xml',
        'views/hr_attendance_sheet_batch_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_payslip_views.xml',
        'views/hr_attendance_sheet_menus.xml',
        # 4. Wizards
        'wizard/hr_attendance_change_data_wizard_views.xml',
        'wizard/hr_attendance_sheet_batch_wizard_views.xml',
        'wizard/hr_attendance_create_payslip_wizard_views.xml',
        # 5. Reports
        'report/hr_attendance_sheet_report.xml',
        'report/hr_attendance_sheet_report_templates.xml',
    ],
    'installable': True,
    'post_init_hook': 'post_init_hook',
    'license': 'LGPL-3',
    'application': True,
    'auto_install': False,
    'category': 'Human Resources/Attendance',
}
