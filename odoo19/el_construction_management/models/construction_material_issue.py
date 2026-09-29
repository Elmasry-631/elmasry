from .workflow_mixin import ConstructionWorkflowMixin
from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError, ValidationError


class ConstructionMaterialIssue(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.material.issue'
    _description = 'Construction Material Stock Operation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    issue_type = fields.Selection([
        ('issue', 'Issue to Site'),
        ('consume', 'Consume on Site'),
        ('return', 'Return to Warehouse'),
        ('wastage', 'Wastage / Scrap'),
    ], required=True, default='issue', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancelled', 'Cancelled')
    ], default='draft', tracking=True)
    project_id = fields.Many2one('el_construction.project', required=True, index=True)
    sub_project_id = fields.Many2one('el_construction.sub.project', index=True)
    work_order_id = fields.Many2one('el_construction.work.order', index=True)
    task_id = fields.Many2one('el_construction.task', index=True)
    material_requisition_id = fields.Many2one('el_construction.material.requisition', required=True, index=True)
    warehouse_id = fields.Many2one('stock.warehouse', required=True)
    source_location_id = fields.Many2one('stock.location', required=True)
    destination_location_id = fields.Many2one('stock.location')
    picking_id = fields.Many2one('stock.picking', readonly=True, copy=False, index=True)
    scrap_id = fields.Many2one('stock.scrap', readonly=True, copy=False, index=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company, index=True)
    date = fields.Date(default=fields.Date.context_today, required=True)
    notes = fields.Text()
    actual_cost = fields.Monetary(string='Actual Material Cost', compute='_compute_actual_cost', currency_field='company_currency_id')
    company_currency_id = fields.Many2one(related='company_id.currency_id', readonly=True)
    line_ids = fields.One2many('el_construction.material.issue.line', 'issue_id', string='Materials')

    @api.depends('picking_id', 'scrap_id')
    def _compute_actual_cost(self):
        try:
            Valuation = self.env['stock.valuation.layer']
        except KeyError:
            Valuation = False
        for rec in self:
            if not Valuation:
                rec.actual_cost = 0.0
                continue
            moves = rec.picking_id.move_ids if rec.picking_id else self.env['stock.move']
            scrap_moves = rec.line_ids.mapped('scrap_id').filtered(lambda scrap: scrap.move_id).mapped('move_id')
            if rec.scrap_id and rec.scrap_id.move_id:
                scrap_moves |= rec.scrap_id.move_id
            moves |= scrap_moves
            layers = Valuation.search([('stock_move_id', 'in', moves.ids)]) if moves else Valuation
            rec.actual_cost = abs(sum(layers.mapped('value')))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.material.issue') or 'New'
        records = super().create(vals_list)
        records._validate_scope()
        return records

    def _validate_scope(self):
        for rec in self:
            if rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('Project company must match the stock operation company.'))
            if rec.warehouse_id.company_id and rec.warehouse_id.company_id != rec.company_id:
                raise ValidationError(_('Warehouse company must match the stock operation company.'))
            if rec.sub_project_id and (rec.sub_project_id.project_id != rec.project_id or rec.sub_project_id.company_id != rec.company_id):
                raise ValidationError(_('Sub Project must belong to the same Project and Company.'))
            if rec.work_order_id and (rec.work_order_id.project_id != rec.project_id or rec.work_order_id.company_id != rec.company_id):
                raise ValidationError(_('Work Order must belong to the same Project and Company.'))
            if rec.task_id and (rec.task_id.project_id != rec.project_id or rec.task_id.company_id != rec.company_id):
                raise ValidationError(_('Task must belong to the same Project and Company.'))
            if rec.material_requisition_id.project_id != rec.project_id or rec.material_requisition_id.company_id != rec.company_id:
                raise ValidationError(_('Material Requisition must belong to the same Project and Company.'))
            if rec.issue_type != 'wastage' and not rec.destination_location_id:
                raise ValidationError(_('Destination Location is required for stock transfers.'))
            if rec.issue_type == 'wastage' and rec.destination_location_id:
                raise ValidationError(_('Wastage operations must not have a destination location.'))
            for line in rec.line_ids:
                if line.material_requisition_line_id and line.material_requisition_line_id.requisition_id != rec.material_requisition_id:
                    raise ValidationError(_('Each material line must belong to the selected Material Requisition.'))
                if line.product_id.company_id and line.product_id.company_id != rec.company_id:
                    raise ValidationError(_('Product company must match the stock operation company.'))
                if line.uom_id and not line.uom_id._has_common_reference(line.product_id.uom_id):
                    raise ValidationError(_('Material Unit of Measure must use the same category as the Product.'))

    def _get_internal_picking_type(self):
        self.ensure_one()
        picking_type = self.env['stock.picking.type'].search([
            ('warehouse_id', '=', self.warehouse_id.id), ('code', '=', 'internal'), ('company_id', '=', self.company_id.id)
        ], order='sequence, id', limit=1)
        if not picking_type:
            raise UserError(_('No Internal Transfer operation type exists for the selected warehouse.'))
        return picking_type

    def _check_available(self):
        for rec in self:
            for line in rec.line_ids:
                if rec.issue_type == 'wastage' or rec.issue_type in ('consume', 'return'):
                    source = rec.source_location_id
                else:
                    source = rec.source_location_id
                available = line.product_id.with_context(location=source.id).free_qty
                requested = line.uom_id._compute_quantity(line.quantity, line.product_id.uom_id) if line.uom_id else line.quantity
                if available < requested:
                    raise UserError(_('%s: insufficient available quantity at %s. Available: %s, requested: %s.') % (
                        line.product_id.display_name, source.display_name, available, requested))

    @api.onchange('issue_type', 'project_id', 'warehouse_id')
    def _onchange_stock_scope(self):
        for rec in self:
            if not rec.project_id or not rec.warehouse_id:
                continue
            rec.project_id._ensure_stock_locations()
            if rec.issue_type == 'issue':
                rec.source_location_id = rec.warehouse_id.lot_stock_id
                rec.destination_location_id = rec.project_id.site_location_id
            elif rec.issue_type == 'consume':
                rec.source_location_id = rec.project_id.site_location_id
                rec.destination_location_id = rec.project_id.consumption_location_id
            elif rec.issue_type == 'return':
                rec.source_location_id = rec.project_id.site_location_id
                rec.destination_location_id = rec.warehouse_id.lot_stock_id
            else:
                rec.source_location_id = rec.project_id.site_location_id
                rec.destination_location_id = False

    def _check_construction_stock_rules(self):
        for rec in self:
            if rec.source_location_id.company_id and rec.source_location_id.company_id != rec.company_id:
                raise ValidationError(_('Source Location company must match the operation company.'))
            if rec.destination_location_id and rec.destination_location_id.company_id and rec.destination_location_id.company_id != rec.company_id:
                raise ValidationError(_('Destination Location company must match the operation company.'))
            if rec.destination_location_id and rec.destination_location_id == rec.source_location_id:
                raise ValidationError(_('Source and Destination Locations cannot be the same.'))
            if rec.issue_type == 'issue':
                if rec.source_location_id != rec.warehouse_id.lot_stock_id or rec.destination_location_id != rec.project_id.site_location_id:
                    raise ValidationError(_('Issue to Site must transfer from the warehouse stock location to the Project Site Location.'))
            elif rec.issue_type == 'consume':
                if rec.source_location_id != rec.project_id.site_location_id or rec.destination_location_id != rec.project_id.consumption_location_id:
                    raise ValidationError(_('Consumption must transfer from the Project Site Location to its Consumption Location.'))
            elif rec.issue_type == 'return':
                if rec.source_location_id != rec.project_id.site_location_id or rec.destination_location_id != rec.warehouse_id.lot_stock_id:
                    raise ValidationError(_('Returns must transfer from the Project Site Location to the warehouse stock location.'))
            else:
                if rec.source_location_id != rec.project_id.site_location_id:
                    raise ValidationError(_('Wastage must be recorded from the Project Site Location.'))

            for line in rec.line_ids:
                if not line.material_requisition_line_id:
                    continue
                mreq_line = line.material_requisition_line_id
                if rec.issue_type in ('consume', 'return', 'wastage') and rec.state == 'draft':
                    issued_uom = mreq_line.uom_id or mreq_line.product_id.uom_id
                    operation_qty = line.quantity
                    if line.uom_id and issued_uom:
                        operation_qty = line.uom_id._compute_quantity(line.quantity, issued_uom)
                    outbound = mreq_line.consumed_qty + mreq_line.returned_qty + mreq_line.wastage_qty + operation_qty
                    if outbound > mreq_line.issued_qty + 1e-6:
                        raise UserError(_('The operation quantity exceeds the net quantity issued to the site for %s.') % line.product_id.display_name)
                if rec.issue_type == 'wastage' and not self.env.user.has_group('el_construction_management.group_construction_manager'):
                    if mreq_line.wastage_qty + line.quantity > mreq_line.allowed_wastage_qty + 1e-6:
                        raise UserError(_('Wastage exceeds the allowed limit for %s. Manager approval is required.') % line.product_id.display_name)

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Stock Operation Status.'))
        return super().write(vals)

    def action_confirm(self):
        for rec in self:
            if rec.state != 'draft':
                continue
            rec._lock_records()
            rec.invalidate_recordset(['state', 'picking_id', 'scrap_id'])
            if rec.state != 'draft':
                continue
            rec._validate_scope()
            rec._check_construction_stock_rules()
            if not rec.line_ids:
                raise UserError(_('Add at least one material line.'))
            rec._check_available()
            rec._create_stock_operation()
        return True

    def _create_stock_operation(self):
        self.ensure_one()
        if self.issue_type == 'wastage':
            scraps = self.env['stock.scrap']
            for line in self.line_ids:
                scrap = self.env['stock.scrap'].create({
                    'product_id': line.product_id.id,
                    'scrap_qty': line.quantity,
                    'product_uom_id': line.uom_id.id or line.product_id.uom_id.id,
                    'location_id': self.source_location_id.id,
                    'origin': self.name,
                    'company_id': self.company_id.id,
                    'construction_material_issue_id': self.id,
                })
                line.scrap_id = scrap.id
                scraps |= scrap
            self.scrap_id = scraps[:1].id if scraps else False
        else:
            picking_type = self._get_internal_picking_type()
            picking = self.env['stock.picking'].create({
                'picking_type_id': picking_type.id,
                'origin': self.name,
                'company_id': self.company_id.id,
                'location_id': self.source_location_id.id,
                'location_dest_id': self.destination_location_id.id,
            })
            for line in self.line_ids:
                move = self.env['stock.move'].create({
                    'name': line.description or line.product_id.display_name,
                    'picking_id': picking.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.uom_id.id or line.product_id.uom_id.id,
                    'location_id': self.source_location_id.id,
                    'location_dest_id': self.destination_location_id.id,
                    'company_id': self.company_id.id,
                    'construction_material_issue_id': self.id,
                    'material_requisition_line_id': line.material_requisition_line_id.id,
                })
                line.stock_move_id = move.id
            picking.construction_material_issue_id = self.id
            self.picking_id = picking.id
            picking.action_confirm()
            picking.action_assign()
        self._transition('confirmed', {'draft': {'confirmed'}})

    def action_done(self):
        for rec in self:
            if rec.state != 'confirmed':
                continue
            if rec.picking_id:
                if rec.picking_id.state not in ('done', 'cancel'):
                    rec.picking_id.button_validate()
                if rec.picking_id.state != 'done':
                    raise UserError(_('The related transfer must be completed before this operation is Done.'))
            scraps = rec.line_ids.mapped('scrap_id')
            if rec.scrap_id:
                scraps |= rec.scrap_id
            if scraps and any(scrap.state != 'done' for scrap in scraps):
                raise UserError(_('All related scraps must be validated before this operation is Done.'))
            rec._transition('done', {'confirmed': {'done'}})
        return True

    def action_cancel(self):
        for rec in self:
            if rec.state == 'done':
                raise UserError(_('Completed stock operations cannot be cancelled. Reverse the stock movement instead.'))
            if rec.picking_id and rec.picking_id.state not in ('cancel', 'done'):
                rec.picking_id.action_cancel()
            rec._transition('cancelled', {'draft': {'cancelled'}, 'confirmed': {'cancelled'}})
        return True

    def action_create_reversal(self):
        self.ensure_one()
        if self.state != 'done':
            raise UserError(_('Only a completed stock operation can be reversed.'))
        if self.issue_type == 'issue':
            return self._open_new_operation('return')
        if self.issue_type == 'return':
            return self._open_new_operation('issue')
        raise UserError(_("Automatic reversal is only supported for Issue to Site and Return to Warehouse operations. Consumption and Wastage require a controlled stock reversal process."))

    def _open_new_operation(self, issue_type):
        self.ensure_one()
        project = self.project_id
        project._ensure_stock_locations()
        warehouse = self.warehouse_id
        if issue_type == 'issue':
            source = warehouse.lot_stock_id
            destination = project.site_location_id
        elif issue_type == 'consume':
            source = project.site_location_id
            destination = project.consumption_location_id
        elif issue_type == 'return':
            source = project.site_location_id
            destination = warehouse.lot_stock_id
        else:
            source = project.site_location_id
            destination = False
        return {
            'type': 'ir.actions.act_window', 'name': _('Material Stock Operation'),
            'res_model': 'el_construction.material.issue', 'view_mode': 'form',
            'context': {
                'default_project_id': project.id, 'default_sub_project_id': self.sub_project_id.id,
                'default_work_order_id': self.work_order_id.id, 'default_material_requisition_id': self.id,
                'default_warehouse_id': warehouse.id, 'default_source_location_id': source.id,
                'default_destination_location_id': destination.id if destination else False,
                'default_company_id': self.company_id.id, 'default_issue_type': issue_type,
            },
        }

    def action_create_consumption(self):
        return self._open_new_operation('consume')

    def action_create_return(self):
        return self._open_new_operation('return')

    def action_create_wastage(self):
        return self._open_new_operation('wastage')

    def action_view_stock_document(self):
        self.ensure_one()
        record = self.picking_id or self.scrap_id
        if not record:
            raise UserError(_('No stock document has been created yet.'))
        return {
            'type': 'ir.actions.act_window',
            'res_model': record._name,
            'view_mode': 'form',
            'res_id': record.id,
        }

class ConstructionMaterialIssueLine(models.Model):
    _name = 'el_construction.material.issue.line'
    _description = 'Construction Material Stock Operation Line'

    issue_id = fields.Many2one('el_construction.material.issue', required=True, ondelete='cascade', index=True)
    material_requisition_line_id = fields.Many2one('el_construction.material.requisition.line', index=True)
    stock_move_id = fields.Many2one('stock.move', readonly=True, copy=False, index=True)
    scrap_id = fields.Many2one('stock.scrap', readonly=True, copy=False, index=True)
    product_id = fields.Many2one('product.product', required=True)
    description = fields.Char()
    quantity = fields.Float(required=True, default=1.0)
    uom_id = fields.Many2one('uom.uom', required=True)
    available_qty = fields.Float(compute='_compute_available_qty')

    @api.depends('product_id', 'issue_id.source_location_id')
    def _compute_available_qty(self):
        for line in self:
            if line.product_id and line.issue_id.source_location_id:
                line.available_qty = line.product_id.with_context(location=line.issue_id.source_location_id.id).free_qty
            else:
                line.available_qty = 0.0

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                line.description = line.product_id.display_name
                line.uom_id = line.product_id.uom_id

    @api.constrains('quantity', 'product_id', 'uom_id')
    def _check_values(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_('Material operation quantity must be greater than zero.'))
            if line.product_id and line.uom_id and not line.uom_id._has_common_reference(line.product_id.uom_id):
                raise ValidationError(_('Material Unit of Measure must use the same category as the Product.'))

    def write(self, vals):
        for line in self:
            if line.issue_id.state != 'draft':
                raise UserError(_('Material operation lines cannot be changed after confirmation.'))
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        issues = self.env['el_construction.material.issue'].browse([v.get('issue_id') for v in vals_list if v.get('issue_id')])
        if any(issue.state != 'draft' for issue in issues):
            raise UserError(_('Material operation lines can only be created in Draft.'))
        return super().create(vals_list)
