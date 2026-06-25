# -*- coding: utf-8 -*-
import json
import logging

from odoo import models, api, fields

_logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------
# Models that should NEVER be tracked (internal / system / auto-generated)
# -----------------------------------------------------------------------
_EXCLUDED_MODELS = {
    'transaction.log',
    'transaction.tracker.config',
    'ir.logging',
    'ir.autovacuum',
    'ir.cron',
    'ir.http',
    'ir.qweb',
    'ir.attachment',
    'ir.translation',
    'ir.ui.view',
    'bus.bus',
    'bus.presence',
    'mail.mail',
    'mail.message',
    'mail.notification',
    'mail.tracking.value',
}

# Prefix patterns to skip
_EXCLUDED_PREFIXES = ('ir.', 'base.', 'transaction.', 'bus.', 'mail.', 'web.')

# Sensitive field name fragments to avoid logging (case-insensitive check)
_SENSITIVE_FIELD_PATTERNS = ('password', 'secret', 'api_key', 'api_secret', 'token', 'auth', 'private_key')


class Base(models.AbstractModel):
    """Inherit base model to intercept all CRUD operations and log them."""

    _inherit = 'base'

    # ------------------------------------------------------------------
    # Create hook
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if self._should_track():
            self._track_create(records)
        return records

    # ------------------------------------------------------------------
    # Write hook
    # ------------------------------------------------------------------
    def write(self, vals):
        old_values = {}
        if self._should_track():
            old_values = self._snapshot_old_values(vals)
        result = super().write(vals)
        if self._should_track() and not self.env.context.get('skip_transaction_tracking'):
            try:
                self._track_write(old_values, vals)
            except Exception:
                _logger.warning("Failed to track write on %s", self._name, exc_info=True)
        return result

    # ------------------------------------------------------------------
    # Unlink hook
    # ------------------------------------------------------------------
    def unlink(self):
        if self._should_track():
            self._track_unlink()
        return super().unlink()

    # ------------------------------------------------------------------
    # Tracking decision logic
    # ------------------------------------------------------------------
    @api.model
    def _should_track(self):
        """Determine whether the current operation should be tracked.

        Skip conditions (return False):
        1. Context flag 'skip_transaction_tracking' is set
        2. The model is in the excluded list
        3. The model starts with an excluded prefix
        4. Running in sudo without explicit tracking
        5. During module install/upgrade
        """
        # 1. Context flag
        if self.env.context.get('skip_transaction_tracking'):
            return False

        # 2. During install/upgrade — avoid massive log noise
        if self.env.context.get('install_mode'):
            return False

        # 3. Excluded models
        model_name = self._name
        if model_name in _EXCLUDED_MODELS:
            return False

        # 4. Excluded prefixes
        for prefix in _EXCLUDED_PREFIXES:
            if model_name.startswith(prefix):
                return False

        # 5. Check if there's a config for this model
        config = self.env['transaction.tracker.config']._get_config(model_name)
        if not config:
            return False

        return True

    # ------------------------------------------------------------------
    # Snapshot helpers
    # ------------------------------------------------------------------
    def _snapshot_old_values(self, vals):
        """Capture the current field values before write is applied.

        Only snapshots fields that appear in `vals`, and only for fields
        that actually exist on the model (skip computed / related)."""
        old_values = {}
        for record in self:
            snapshot = {}
            for fname in vals:
                field = self._fields.get(fname)
                if not field:
                    continue
                if field.compute and not field.store:
                    continue
                if any(p in fname.lower() for p in _SENSITIVE_FIELD_PATTERNS):
                    continue
                try:
                    val = getattr(record, fname, None)
                    if isinstance(val, models.BaseModel):
                        snapshot[fname] = val.id
                        snapshot[fname + '_display'] = val.display_name
                    else:
                        snapshot[fname] = val
                except Exception:
                    pass
            old_values[record.id] = snapshot
        return old_values

    def _snapshot_new_values(self, vals):
        """Capture field values after write is applied."""
        new_values = {}
        for record in self:
            snapshot = {}
            for fname in vals:
                field = self._fields.get(fname)
                if not field:
                    continue
                if field.compute and not field.store:
                    continue
                if any(p in fname.lower() for p in _SENSITIVE_FIELD_PATTERNS):
                    continue
                try:
                    val = getattr(record, fname, None)
                    if isinstance(val, models.BaseModel):
                        snapshot[fname] = val.id
                        snapshot[fname + '_display'] = val.display_name
                    else:
                        snapshot[fname] = val
                except Exception:
                    pass
            new_values[record.id] = snapshot
        return new_values

    # ------------------------------------------------------------------
    # Track methods — create log entries
    # ------------------------------------------------------------------
    def _track_create(self, records):
        """Log create operations for the given records."""
        TransactionLog = self.env['transaction.log']
        model_name = self._name
        module_name = self._get_module_name()
        ip_address = TransactionLog._get_ip_address()

        for record in records:
            try:
                display_name = record.display_name or ''
            except Exception:
                display_name = ''

            # Capture new values (skip binary, computed-non-stored, and sensitive fields)
            new_values = {}
            for fname, field in record._fields.items():
                if fname.startswith('_') or field.type in ('binary',):
                    continue
                if field.compute and not field.store:
                    continue
                if any(p in fname.lower() for p in _SENSITIVE_FIELD_PATTERNS):
                    continue
                try:
                    val = getattr(record, fname, None)
                    if isinstance(val, models.BaseModel):
                        new_values[fname] = val.id
                    else:
                        new_values[fname] = val
                except Exception:
                    pass

            try:
                TransactionLog.with_context(
                    skip_transaction_tracking=True
                ).sudo()._log_operation(
                    operation='create',
                    model_name=model_name,
                    res_id=record.id,
                    record_display_name=display_name[:200],
                    new_values=new_values,
                    module_name=module_name,
                    ip_address=ip_address,
                )
            except Exception:
                _logger.warning("Failed to track create on %s id=%s", model_name, record.id, exc_info=True)

    def _track_write(self, old_values, vals):
        """Log write operations."""
        TransactionLog = self.env['transaction.log']
        model_name = self._name
        module_name = self._get_module_name()
        ip_address = TransactionLog._get_ip_address()
        changed_fields = ', '.join(vals.keys())

        # Check for suspicious activity: bulk write on many records
        is_suspicious = len(self) > 50

        # Snapshot new values once for all records (not inside the loop)
        try:
            new_snapshots = self._snapshot_new_values(vals)
        except Exception:
            new_snapshots = {}

        for record in self:
            old_snap = old_values.get(record.id, {})
            new_snap = new_snapshots.get(record.id, {})

            try:
                display_name = record.display_name or ''
            except Exception:
                display_name = ''

            try:
                TransactionLog.with_context(
                    skip_transaction_tracking=True
                ).sudo()._log_operation(
                    operation='write',
                    model_name=model_name,
                    res_id=record.id,
                    record_display_name=display_name[:200],
                    old_values=old_snap,
                    new_values=new_snap,
                    changed_fields=changed_fields,
                    module_name=module_name,
                    ip_address=ip_address,
                    is_suspicious=is_suspicious,
                )
            except Exception:
                _logger.warning("Failed to track write on %s id=%s", model_name, record.id, exc_info=True)

    def _track_unlink(self):
        """Log unlink (delete) operations."""
        TransactionLog = self.env['transaction.log']
        model_name = self._name
        module_name = self._get_module_name()
        ip_address = TransactionLog._get_ip_address()

        # Suspicious: bulk delete
        is_suspicious = len(self) > 20

        for record in self:
            # Snapshot the record before it's deleted
            old_values = {}
            for fname, field in record._fields.items():
                if fname.startswith('_') or field.type in ('binary',):
                    continue
                if field.compute and not field.store:
                    continue
                if any(p in fname.lower() for p in _SENSITIVE_FIELD_PATTERNS):
                    continue
                try:
                    val = getattr(record, fname, None)
                    if isinstance(val, models.BaseModel):
                        old_values[fname] = val.id
                        old_values[fname + '_display'] = val.display_name
                    else:
                        old_values[fname] = val
                except Exception:
                    pass

            try:
                display_name = record.display_name or ''
            except Exception:
                display_name = ''

            try:
                TransactionLog.with_context(
                    skip_transaction_tracking=True
                ).sudo()._log_operation(
                    operation='unlink',
                    model_name=model_name,
                    res_id=record.id,
                    record_display_name=display_name[:200],
                    old_values=old_values,
                    module_name=module_name,
                    ip_address=ip_address,
                    is_suspicious=is_suspicious,
                )
            except Exception:
                _logger.warning("Failed to track unlink on %s id=%s", model_name, record.id, exc_info=True)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @api.model
    def _get_module_name(self):
        """Get the Odoo addon name that owns this model."""
        # Each model class carries __module__ which is the Python module path
        cls = type(self)
        module = getattr(cls, '__module__', '')
        # module looks like 'odoo.addons.sale.models.sale_order'
        parts = module.split('.')
        try:
            addons_idx = parts.index('addons')
            return parts[addons_idx + 1] if len(parts) > addons_idx + 1 else ''
        except ValueError:
            return ''
