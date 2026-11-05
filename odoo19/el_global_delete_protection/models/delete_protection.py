"""Central ORM deletion guard with a server-only, scoped maintenance bypass."""

from contextlib import contextmanager
from contextvars import ContextVar

from odoo import _, models
from odoo.exceptions import UserError


_trusted_delete_scope = ContextVar("el_global_delete_protection_scope", default=False)


@contextmanager
def allow_internal_deletion():
    """Allow deletion only inside an explicit trusted Python maintenance scope.

    This capability is intentionally not represented in ``env.context``: RPC
    callers can choose context values, but cannot set this process-local token.
    Trusted server code should import this helper and wrap only the exact
    cleanup operation that requires deletion.
    """
    token = _trusted_delete_scope.set(True)
    try:
        yield
    finally:
        _trusted_delete_scope.reset(token)


class BaseModel(models.AbstractModel):
    _inherit = "base"

    def unlink(self):
        return _guarded_unlink(self, super().unlink)


def _guarded_unlink(records, parent_unlink):
    if _trusted_delete_scope.get():
        return parent_unlink()
    raise UserError(_("Deleting records is disabled by the system administrator."))


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def unlink(self):
        # Guard before ir.attachment's own filestore and reference cleanup.
        return _guarded_unlink(self, super().unlink)
