"""Quality Check workflow migration.

The workflow adds states and fields with safe defaults. Existing records retain
 their current inspection result and are not automatically reclassified, because
business ownership of historical QA records must be preserved.
"""

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    checks = env['el_construction.quality.check'].search([])
    # Existing terminal inspection results are intentionally preserved. The new
    # closed/cancelled lifecycle starts from future user actions.
    if checks:
        checks.invalidate_recordset()
