# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, AccessError


class InterCompanyTransferRequest(models.Model):
    _name = 'inter.company.transfer.request'
    _description = 'Inter Company Transfer Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        tracking=True,
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False)

    # Requesting company: the company that needs the goods
    company_id = fields.Many2one(
        'res.company',
        string='Requesting Company',
        required=True,
        default=lambda self: self.env.company,
        readonly=True,
        tracking=True,
        help="Company of the user that created the request (the goods recipient).",
    )

    # Warehouse of the requesting company that will receive the goods
    source_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Destination Warehouse',
        required=True,
        domain="[('company_id', '=', company_id)]",
        tracking=True,
        help="Warehouse of the requesting company where the goods will be delivered.",
    )

    # Company that owns the stock
    dest_company_id = fields.Many2one(
        'res.company',
        string='Source Company (Stock Owner)',
        required=True,
        domain="[('id', '!=', company_id)]",
        tracking=True,
        help="Company owning the stock requested by the requesting company.",
    )

    # Warehouse of the source company where the stock is stored
    dest_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Source Warehouse',
        required=True,
        domain="[('company_id', '=', dest_company_id)]",
        context={'el_inter_company_warehouse': True},
        tracking=True,
        help="Warehouse of the source company holding the requested products.",
    )

    line_ids = fields.One2many(
        'inter.company.transfer.request.line',
        'request_id',
        string='Products',
        copy=True,
    )

    user_id = fields.Many2one(
        'res.users',
        string='Requested By',
        default=lambda self: self.env.user,
        readonly=True,
        tracking=True,
    )

    confirmed_by = fields.Many2one(
        'res.users',
        string='Confirmed By',
        readonly=True,
        tracking=True,
    )

    confirmed_date = fields.Datetime(
        string='Confirmed Date',
        readonly=True,
        tracking=True,
    )

    # Outgoing transfer, created in the source (stock owner) company
    picking_id = fields.Many2one(
        'stock.picking',
        string='Outgoing Transfer',
        readonly=True,
        copy=False,
        help="Stock transfer created in the source company to deliver the requested goods.",
    )

    # Incoming transfer, created in the requesting company
    incoming_picking_id = fields.Many2one(
        'stock.picking',
        string='Incoming Transfer',
        readonly=True,
        copy=False,
        help="Stock transfer created in the requesting company to receive the goods.",
    )

    note = fields.Text(string='Internal Notes')

    # Computed helpers used by the views
    is_draft = fields.Boolean(compute='_compute_is_draft')
    can_confirm = fields.Boolean(compute='_compute_can_confirm')

    @api.depends('state')
    def _compute_is_draft(self):
        for record in self:
            record.is_draft = record.state == 'draft'

    @api.onchange('dest_company_id')
    def _onchange_dest_company_id(self):
        """Propose the default warehouse of the company owning the stock."""
        if not self.dest_company_id:
            return
        warehouse = self.env['stock.warehouse'].sudo().search(
            [('company_id', '=', self.dest_company_id.id)], limit=1)
        if warehouse:
            self.dest_warehouse_id = warehouse.id

    @api.depends('state', 'dest_company_id')
    def _compute_can_confirm(self):
        for record in self:
            record.can_confirm = record.state == 'draft' and record._can_access_source_company()

    # ------------------------------------------------------------------
    # CRUD / constraints
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals.get('name') == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('inter.company.transfer.request') or _('New')
        return super().create(vals_list)

    @api.constrains('company_id', 'dest_company_id')
    def _check_companies_different(self):
        for record in self:
            if record.company_id and record.dest_company_id and record.company_id == record.dest_company_id:
                raise ValidationError(_("The requesting company and the source company must be different."))

    @api.constrains('line_ids')
    def _check_lines(self):
        for record in self:
            if not record.line_ids:
                raise ValidationError(_("You must add at least one product line."))
            for line in record.line_ids:
                if line.product_qty <= 0:
                    raise ValidationError(_("Quantity must be greater than zero for %s.") % line.product_id.display_name)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _can_access_source_company(self):
        """Whether the current user is allowed to handle the source company stock.

        A request can only be confirmed by a user who works in the source company
        (the company owning the stock), or by a stock manager.
        """
        self.ensure_one()
        if self.env.su:
            return True
        if self.env.user.has_group('stock.group_stock_manager'):
            return True
        return self.env.company == self.dest_company_id

    def _allowed_company_ids(self):
        """Companies involved in the transfer (source + requesting)."""
        self.ensure_one()
        companies = self.env['res.company']
        if self.dest_company_id:
            companies |= self.dest_company_id
        if self.company_id:
            companies |= self.company_id
        return companies.ids

    def _get_inter_company_transit_location(self):
        """Standard Odoo inter-company transit location (shared by all companies)."""
        location = self.env.ref('stock.stock_location_inter_company', raise_if_not_found=False)
        if not location:
            raise UserError(_("The inter-company transit location is not available in this database."))
        if not location.active:
            location.sudo().write({'active': True})
        return location

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def action_confirm(self):
        """Confirm the request and create the stock transfers in both companies."""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_("Only draft requests can be confirmed."))
        if not self._can_access_source_company():
            raise AccessError(_("You don't have access to the source company (%s).") % self.dest_company_id.display_name)
        if not self.line_ids:
            raise UserError(_("You must add at least one product line before confirming the request."))

        outgoing_picking = self._create_outgoing_picking()
        incoming_picking = self._create_incoming_picking()

        self.write({
            'state': 'confirmed',
            'confirmed_by': self.env.user.id,
            'confirmed_date': fields.Datetime.now(),
            'picking_id': outgoing_picking.id,
            'incoming_picking_id': incoming_picking.id,
        })

        self.message_post(
            body=_("Transfer request confirmed by %s. Outgoing transfer %s created in %s and incoming transfer %s created in %s.") % (
                self.env.user.name,
                outgoing_picking.name,
                self.dest_company_id.display_name,
                incoming_picking.name,
                self.company_id.display_name,
            ),
            subtype_xmlid='mail.mt_note',
        )
        return self.action_view_picking()

    def _create_outgoing_picking(self):
        """Create the delivery in the source company: source stock -> inter-company transit."""
        self.ensure_one()
        source_warehouse = self.dest_warehouse_id.sudo()
        src_location = source_warehouse.lot_stock_id
        if not src_location:
            raise UserError(_("The source warehouse %s has no stock location.") % source_warehouse.display_name)
        transit_location = self._get_inter_company_transit_location()

        picking_env = self.env['stock.picking'].with_company(self.dest_company_id).with_context(
            allowed_company_ids=self._allowed_company_ids(),
        )
        picking = picking_env.create({
            'picking_type_id': source_warehouse.out_type_id.id,
            'location_id': src_location.id,
            'location_dest_id': transit_location.id,
            'origin': self.name,
            'partner_id': self.company_id.partner_id.id,
        })
        if picking.location_dest_id != transit_location:
            picking.location_dest_id = transit_location

        move_env = self.env['stock.move'].with_company(self.dest_company_id).with_context(
            allowed_company_ids=self._allowed_company_ids(),
        )
        for line in self.line_ids:
            move_env.create({
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_qty,
                'uom_id': line.product_uom_id.id,
                'location_id': src_location.id,
                'location_dest_id': transit_location.id,
                'picking_id': picking.id,
                'company_id': self.dest_company_id.id,
            })

        picking.action_confirm()
        return picking

    def _create_incoming_picking(self):
        """Create the receipt in the requesting company: inter-company transit -> its warehouse."""
        self.ensure_one()
        transit_location = self._get_inter_company_transit_location()
        dest_warehouse = self.source_warehouse_id.sudo()
        dest_location = dest_warehouse.wh_input_stock_loc_id or dest_warehouse.lot_stock_id
        if not dest_location:
            raise UserError(_("The destination warehouse %s has no stock location.") % dest_warehouse.display_name)

        # The receipt belongs to the requesting company, so it is created with elevated
        # rights: the user confirming the request may only work in the source company.
        picking_env = self.env['stock.picking'].sudo().with_company(self.company_id).with_context(
            allowed_company_ids=self._allowed_company_ids(),
        )
        picking = picking_env.create({
            'picking_type_id': dest_warehouse.in_type_id.id,
            'location_id': transit_location.id,
            'location_dest_id': dest_location.id,
            'origin': self.name,
            'partner_id': self.dest_company_id.partner_id.id,
        })
        if picking.location_dest_id != dest_location:
            picking.location_dest_id = dest_location

        move_env = self.env['stock.move'].sudo().with_company(self.company_id).with_context(
            allowed_company_ids=self._allowed_company_ids(),
        )
        for line in self.line_ids:
            move_env.create({
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_qty,
                'uom_id': line.product_uom_id.id,
                'location_id': transit_location.id,
                'location_dest_id': dest_location.id,
                'picking_id': picking.id,
                'company_id': self.company_id.id,
            })

        picking.action_confirm()
        return picking

    def action_done(self):
        """Mark the request as done."""
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_("Only confirmed requests can be marked as done."))
        if self.picking_id and self.picking_id.state != 'done':
            raise UserError(_("The outgoing stock transfer (%s) is not completed yet.") % self.picking_id.name)

        self.write({'state': 'done'})
        self.message_post(
            body=_("Transfer request marked as done by %s.") % self.env.user.name,
            subtype_xmlid='mail.mt_note',
        )

    def action_cancel(self):
        """Cancel the request and its stock transfers."""
        self.ensure_one()
        if self.state in ('done', 'cancel'):
            raise UserError(_("Cannot cancel a completed or already cancelled request."))
        for picking in (self.picking_id | self.incoming_picking_id):
            if picking and picking.state not in ('draft', 'cancel', 'done'):
                picking.action_cancel()

        self.write({'state': 'cancel'})
        self.message_post(
            body=_("Transfer request cancelled by %s.") % self.env.user.name,
            subtype_xmlid='mail.mt_note',
        )

    def action_reset_to_draft(self):
        """Reset a cancelled request back to draft."""
        self.ensure_one()
        if self.state != 'cancel':
            raise UserError(_("Only cancelled requests can be reset to draft."))

        self.write({'state': 'draft'})
        self.message_post(
            body=_("Transfer request reset to draft by %s.") % self.env.user.name,
            subtype_xmlid='mail.mt_note',
        )

    def action_view_picking(self):
        """Open the outgoing stock transfer."""
        self.ensure_one()
        if not self.picking_id:
            raise UserError(_("No stock transfer has been created yet."))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Outgoing Transfer'),
            'res_model': 'stock.picking',
            'res_id': self.picking_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_incoming_picking(self):
        """Open the incoming stock transfer."""
        self.ensure_one()
        if not self.incoming_picking_id:
            raise UserError(_("No incoming stock transfer has been created yet."))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Incoming Transfer'),
            'res_model': 'stock.picking',
            'res_id': self.incoming_picking_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
