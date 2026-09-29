"""Post-migration hook for 19.0.1.8.0.

No data migration is required: new planning fields are nullable/derived and
existing task dates/dependencies remain compatible.
"""


def migrate(cr, version):
    # Kept intentionally empty so the upgrade remains explicit and auditable.
    return None
