import secrets

from odoo import _, api
from odoo.exceptions import AccessError, UserError

# Runtime-only token. A caller cannot legitimately forge the workflow context from RPC.
_WORKFLOW_TOKEN = secrets.token_urlsafe(32)
_WORKFLOW_CONTEXT_KEY = '_construction_workflow_token'
_WORKFLOW_CREATE_CONTEXT_KEY = '_construction_workflow_create_token'


class ConstructionWorkflowMixin:
    """Server-side workflow helper with protected state transitions."""

    def _require_manager(self, message=None):
        if not self.env.user.has_group('el_construction_management.group_construction_manager'):
            raise AccessError(message or _('Only Construction Managers can perform this operation.'))

    def _transition(self, new_state, allowed, *, manager=False):
        if manager:
            self._require_manager()
        for record in self:
            if record.state != new_state and new_state not in allowed.get(record.state, set()):
                raise UserError(_(
                    'Invalid workflow transition: %(old)s → %(new)s.',
                    old=record.state, new=new_state,
                ))
        return self.with_context(**{_WORKFLOW_CONTEXT_KEY: _WORKFLOW_TOKEN}).write({'state': new_state})

    def _lock_records(self, records=None):
        records = records or self
        if not records:
            return
        ids = tuple(records.ids)
        if not ids:
            return
        # Centralized, parameterized row lock for the few operations that require
        # serialization (numbering, invoice creation, etc.).
        records.env.cr.execute(
            'SELECT id FROM %s WHERE id IN %%s FOR UPDATE' % records._table,
            [ids],
        )

    @api.model_create_multi
    def create(self, vals_list):
        """Prevent callers from injecting a non-initial workflow state at create time."""
        state_field = self._fields.get('state')
        if state_field:
            default_state = self.default_get(['state']).get('state')
            for vals in vals_list:
                if 'state' in vals and vals['state'] != default_state and not self.env.context.get(_WORKFLOW_CREATE_CONTEXT_KEY) == _WORKFLOW_TOKEN:
                    raise UserError(_(
                        'Records must be created in the initial Status (%(state)s). Use the workflow action to reach another Status.',
                        state=default_state or _('default'),
                    ))
        return super().create(vals_list)

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow actions to change the Status.'))
        return super().write(vals)

    def _workflow_write_allowed(self):
        return self.env.context.get(_WORKFLOW_CONTEXT_KEY) == _WORKFLOW_TOKEN
