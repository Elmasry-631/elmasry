# -*- coding: utf-8 -*-
from . import models
from . import report


def post_init_hook(env):
    """Auto-populate tracker configs for all installed models after install."""
    # Get existing configs
    existing_model_ids = env['transaction.tracker.config'].search([]).mapped('model_id').ids

    # Get all non-transient models
    models = env['ir.model'].search([
        ('transient', '=', False),
        ('id', 'not in', existing_model_ids),
    ])

    # Excluded prefixes
    excluded_prefixes = ('ir.', 'base.', 'transaction.', 'bus.', 'mail.', 'web.')

    created = 0
    for model in models:
        if model.model.startswith(excluded_prefixes):
            continue
        env['transaction.tracker.config'].create({
            'model_id': model.id,
            'track_create': True,
            'track_write': True,
            'track_unlink': True,
            'track_read': False,
        })
        created += 1

    # Initialize the cache
    env.registry._transaction_tracker_cache = {}
