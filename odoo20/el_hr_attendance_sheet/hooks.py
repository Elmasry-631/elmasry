# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Prepare the attendance payroll data right after installation.

    Three things happen here:

    * the rules the Attendance Structure inherited from
      hr_payroll.default_structure are dropped (they would double the salary);
    * the "Add Attendance Rules" server action is executed on every payroll
      structure, so overtime / lateness / absence are computed on payslips
      that use any structure — a payslip applies a single structure, so those
      rules have to sit next to the basic salary;
    * the result is logged.

    The action runs silently here so a notification cannot abort the
    installation; run it from the Structures list view to see the report, it
    is idempotent either way.
    """
    structure = env.ref(
        'el_hr_attendance_sheet.structure_attendance', raise_if_not_found=False)
    if not structure:
        return

    structure.action_clean_inherited_rules()
    structure.action_remove_duplicated_attendance_rules()

    action = env.ref(
        'el_hr_attendance_sheet.action_propagate_attendance_rules',
        raise_if_not_found=False,
    )
    structures = env['hr.payroll.structure'].search([])
    if not action or not structures:
        return
    try:
        action.with_context(
            attendance_propagate_silent=True,
            active_model='hr.payroll.structure',
            active_ids=structures.ids,
        ).run()
    except Exception:  # noqa: BLE001 - never block the install
        _logger.exception(
            "Could not propagate the attendance rules to the payroll "
            "structures. Run the 'Add Attendance Rules' server action "
            "manually once the module is installed.")
        return
    _logger.info(
        "Attendance rules propagated across %d payroll structure(s).",
        len(structures))