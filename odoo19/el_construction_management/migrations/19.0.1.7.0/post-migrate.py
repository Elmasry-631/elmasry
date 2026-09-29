from logging import getLogger

_logger = getLogger(__name__)


def migrate(cr, version):
    """Gantt planning release migration.

    Task dependency relations and Gantt configuration are schema/view changes
    handled by Odoo during module upgrade. No destructive data migration is
    required for this release.
    """
    if not version:
        return
    _logger.info('Construction Management Gantt planning migration applied from %s', version)
