# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TransactionTrackerConfig(models.Model):
    _name = 'transaction.tracker.config'
    _description = 'Transaction Tracker Configuration'
    _order = 'model_name'
    _rec_name = 'model_name'

    # ------------------------------------------------------------------
    # Fields
    # ------------------------------------------------------------------
    model_id = fields.Many2one(
        'ir.model',
        string='Model',
        required=True,
        ondelete='cascade',
        help='The Odoo model to configure tracking for',
    )
    model_name = fields.Char(
        string='Model Name',
        related='model_id.model',
        store=True,
        index=True,
    )
    track_create = fields.Boolean(
        string='Track Create',
        default=True,
        help='Track when records are created in this model',
    )
    track_write = fields.Boolean(
        string='Track Write',
        default=True,
        help='Track when records are modified in this model',
    )
    track_unlink = fields.Boolean(
        string='Track Delete',
        default=True,
        help='Track when records are deleted in this model',
    )
    track_read = fields.Boolean(
        string='Track Read',
        default=False,
        help='Track when records are viewed/read (WARNING: generates high volume)',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    # ------------------------------------------------------------------
    # Constraints
    # ------------------------------------------------------------------
    _check_model_uniq = models.Constraint(
        'UNIQUE(model_id)',
        'Each model can only have one tracker configuration.',
    )

    # ------------------------------------------------------------------
    # CRUD overrides
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        self._invalidate_tracker_cache()
        return records

    def write(self, vals):
        result = super().write(vals)
        self._invalidate_tracker_cache()
        return result

    def unlink(self):
        result = super().unlink()
        self._invalidate_tracker_cache()
        return result

    # ------------------------------------------------------------------
    # Configuration helpers
    # ------------------------------------------------------------------
    @api.model
    def _get_config(self, model_name):
        """Get the tracker configuration for a model.
        Returns the config record or False if tracking is disabled."""
        # Use cache to avoid repeated DB queries
        if not hasattr(self.pool, '_transaction_tracker_cache'):
            self.pool._transaction_tracker_cache = {}
        cache_key = 'transaction_tracker_config_%s' % model_name
        cached = self.pool._transaction_tracker_cache.get(cache_key)
        if cached is not None:
            return cached

        config = self.with_context(active_test=True).sudo().search([
            ('model_name', '=', model_name),
        ], limit=1)

        self.pool._transaction_tracker_cache[cache_key] = config or False
        return config or False

    @api.model
    def _invalidate_tracker_cache(self):
        """Clear the tracker config cache after changes."""
        if hasattr(self.pool, '_transaction_tracker_cache'):
            self.pool._transaction_tracker_cache.clear()

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def action_track_all(self):
        """Enable all tracking operations for selected configs."""
        self.write({
            'track_create': True,
            'track_write': True,
            'track_unlink': True,
            'active': True,
        })

    def action_untrack_all(self):
        """Disable all tracking operations for selected configs."""
        self.write({
            'track_create': False,
            'track_write': False,
            'track_unlink': False,
            'track_read': False,
        })

    @api.model
    def action_auto_populate_models(self):
        """Create tracker configs for all installed models that don't have one yet."""
        existing = self.search([]).mapped('model_id')
        models = self.env['ir.model'].search([
            ('transient', '=', False),
            ('id', 'not in', existing.ids),
        ])
        for model in models:
            # Skip internal/technical models
            if model.model.startswith(('ir.', 'base.', 'transaction.')):
                continue
            self.create({
                'model_id': model.id,
                'track_create': True,
                'track_write': True,
                'track_unlink': True,
                'track_read': False,
            })
        self._invalidate_tracker_cache()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('%d model configurations created.') % len(models),
                'type': 'success',
                'sticky': False,
            },
        }
