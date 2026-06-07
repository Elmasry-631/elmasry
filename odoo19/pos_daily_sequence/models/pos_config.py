# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PosConfig(models.Model):
    _inherit = 'pos.config'

    daily_sequence_id = fields.Many2one(
        'ir.sequence',
        string='Daily Order Sequence',
        help='Sequence used for generating daily order numbers in POS.',
        copy=False,
    )
    use_daily_sequence = fields.Boolean(
        string='Use Daily Order Sequence',
        default=False,
        help='Enable this to reset order numbers every day.\n'
             'Order numbers will start from 1 at the beginning of each day.',
    )
    daily_sequence_prefix = fields.Char(
        string='Sequence Prefix',
        default='POS-%(year)s%(month)s%(day)s-',
        help='Prefix for the daily order number sequence.\n'
             'Use %(year)s, %(month)s, %(day)s for date parts.\n'
             'Example: POS-%(year)s%(month)s%(day)s',
    )
    daily_sequence_reset_period = fields.Selection(
        selection=[
            ('day', 'Every Day'),
            ('session', 'Every Session'),
        ],
        string='Reset Sequence',
        default='day',
        required=True,
        help='Choose whether the POS order number restarts every day or every POS session.',
    )
    daily_sequence_padding = fields.Integer(
        string='Sequence Padding',
        default=4,
        help='Number of digits for the daily order number.\n'
             'For example, padding=4 will generate: 0001, 0002, etc.',
    )

    @api.onchange('use_daily_sequence')
    def _onchange_use_daily_sequence(self):
        """When enabling daily sequence, warn if no sequence is set."""
        if self.use_daily_sequence and not self.daily_sequence_id:
            self.daily_sequence_prefix = 'POS-%(year)s%(month)s%(day)s-'
            self.daily_sequence_padding = 4

    def _create_daily_sequence(self):
        """Create or get a daily sequence for this POS config."""
        self.ensure_one()
        if self.daily_sequence_id:
            return self.daily_sequence_id

        sequence_vals = {
            'name': _('POS Daily Sequence - %s') % self.name,
            'implementation': 'no_gap',
            'prefix': self.daily_sequence_prefix or 'POS-%(year)s%(month)s%(day)s-',
            'padding': self.daily_sequence_padding or 4,
            'number_increment': 1,
            'use_date_range': True,
        }

        sequence = self.env['ir.sequence'].sudo().create(sequence_vals)

        # Create default date range for today
        today = fields.Date.context_today(self)
        self.env['ir.sequence.date_range'].sudo().create({
            'sequence_id': sequence.id,
            'date_from': today,
            'date_to': today,
            'number_next': 1,
        })

        self.write({'daily_sequence_id': sequence.id})
        return sequence

    def write(self, vals):
        """Override write to handle sequence creation and updates."""
        result = super(PosConfig, self).write(vals)

        if (
            vals.get('use_daily_sequence')
            or vals.get('daily_sequence_reset_period') == 'day'
        ):
            for config in self:
                if config.use_daily_sequence and config.daily_sequence_reset_period == 'day' and not config.daily_sequence_id:
                    config._create_daily_sequence()
        return result

    def _create_session_sequence(self, session):
        """Create or get a sequence dedicated to one POS session."""
        self.ensure_one()
        session.ensure_one()

        if session.daily_sequence_id:
            return session.daily_sequence_id

        sequence = self.env['ir.sequence'].sudo().create({
            'name': _('POS Session Sequence - %(config)s - %(session)s') % {'config': self.name, 'session': session.name},
            'implementation': 'no_gap',
            'prefix': self.daily_sequence_prefix or 'POS-%(year)s%(month)s%(day)s-',
            'padding': self.daily_sequence_padding or 4,
            'number_increment': 1,
            'use_date_range': False,
        })
        session.sudo().write({'daily_sequence_id': sequence.id})
        return sequence

    def _generate_session_order_number(self, session):
        self.ensure_one()
        session = session or self.current_session_id
        if not session:
            return self._generate_day_order_number()

        sequence = self._create_session_sequence(session)
        return sequence.next_by_id()

    def _generate_day_order_number(self):
        """
        Generate a daily order number using the config's sequence.
        This method creates a date range for today if it does not exist yet,
        ensuring the sequence number resets to 1 at the start of each new day.
        """
        self.ensure_one()

        if not self.daily_sequence_id:
            self._create_daily_sequence()

        sequence = self.daily_sequence_id
        today = fields.Date.context_today(self)

        # Check if a date range exists for today
        date_range = self.env['ir.sequence.date_range'].sudo().search([
            ('sequence_id', '=', sequence.id),
            ('date_from', '<=', today),
            ('date_to', '>=', today),
        ], limit=1)

        # If no date range for today, create one (this resets the counter to 1)
        if not date_range:
            date_range = self.env['ir.sequence.date_range'].sudo().create({
                'sequence_id': sequence.id,
                'date_from': today,
                'date_to': today,
                'number_next': 1,
            })

        # Generate the next number from the sequence
        return sequence.with_context(ir_sequence_date=today).next_by_id()

    def _generate_daily_order_number(self, session=False):
        self.ensure_one()
        if self.daily_sequence_reset_period == 'session':
            return self._generate_session_order_number(session)
        return self._generate_day_order_number()

    def _get_or_create_today_date_range(self):
        """Ensure a date range exists for today and return it."""
        self.ensure_one()
        sequence = self.daily_sequence_id
        today = fields.Date.context_today(self)

        date_range = self.env['ir.sequence.date_range'].sudo().search([
            ('sequence_id', '=', sequence.id),
            ('date_from', '<=', today),
            ('date_to', '>=', today),
        ], limit=1)

        if not date_range:
            date_range = self.env['ir.sequence.date_range'].sudo().create({
                'sequence_id': sequence.id,
                'date_from': today,
                'date_to': today,
                'number_next': 1,
            })

        return date_range

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to set default values."""
        records = super(PosConfig, self).create(vals_list)
        return records
