from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ConstructionRateAnalysis(models.Model):
    _name = 'el_construction.rate.analysis'
    _description = 'Rate Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    title = fields.Char(string='Title', required=True)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True, index=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True)
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project')
    date = fields.Date(string='Date', default=fields.Date.context_today)

    work_type_id = fields.Many2one('el_construction.work.type', string='Work Type')
    work_sub_type_id = fields.Many2one('el_construction.work.sub.type', string='Work Sub Type',
                                        domain="[('work_type_id', '=', work_type_id)]")
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    per_unit = fields.Char(string='Per Unit')

    # Lines
    material_line_ids = fields.One2many('el_construction.rate.analysis.line', 'rate_analysis_id',
                                         string='Material Lines', domain=[('line_type', '=', 'material')])
    equipment_line_ids = fields.One2many('el_construction.rate.analysis.line', 'rate_analysis_id',
                                          string='Equipment Lines', domain=[('line_type', '=', 'equipment')])
    labour_line_ids = fields.One2many('el_construction.rate.analysis.line', 'rate_analysis_id',
                                       string='Labour Lines', domain=[('line_type', '=', 'labour')])
    overhead_line_ids = fields.One2many('el_construction.rate.analysis.line', 'rate_analysis_id',
                                         string='Overhead Lines', domain=[('line_type', '=', 'overhead')])
    other_line_ids = fields.One2many('el_construction.rate.analysis.line', 'rate_analysis_id',
                                      string='Other Lines', domain=[('line_type', '=', 'other')])

    # Totals
    material_total = fields.Float(string='Material Total', compute='_compute_totals', store=True)
    equipment_total = fields.Float(string='Equipment Total', compute='_compute_totals', store=True)
    labour_total = fields.Float(string='Labour Total', compute='_compute_totals', store=True)
    overhead_total = fields.Float(string='Overhead Total', compute='_compute_totals', store=True)
    other_total = fields.Float(string='Other Total', compute='_compute_totals', store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_totals', store=True)

    @api.onchange('work_type_id')
    def _onchange_work_type_id(self):
        if self.work_sub_type_id and self.work_sub_type_id.work_type_id != self.work_type_id:
            self.work_sub_type_id = False

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.sub_project_id and self.sub_project_id.project_id != self.project_id:
            self.sub_project_id = False

    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        if self.uom_id and self.per_unit and not self.per_unit.strip():
            self.per_unit = self.uom_id.name

    @api.constrains('project_id', 'sub_project_id', 'company_id', 'work_type_id', 'work_sub_type_id')
    def _check_consistency(self):
        for rec in self:
            if rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('Rate Analysis company must match the Project company.'))
            if rec.sub_project_id and (rec.sub_project_id.project_id != rec.project_id or rec.sub_project_id.company_id != rec.company_id):
                raise ValidationError(_('Sub Project must belong to the same Project and Company.'))
            if rec.work_sub_type_id and rec.work_sub_type_id.work_type_id != rec.work_type_id:
                raise ValidationError(_('Work Sub Type must belong to the selected Work Type.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.rate.analysis') or 'New'
        return super().create(vals_list)

    @api.depends('material_line_ids.amount', 'equipment_line_ids.amount',
                 'labour_line_ids.amount', 'overhead_line_ids.amount', 'other_line_ids.amount')
    def _compute_totals(self):
        for rec in self:
            all_lines = rec.material_line_ids | rec.equipment_line_ids | rec.labour_line_ids | rec.overhead_line_ids | rec.other_line_ids
            rec.material_total = sum(l.amount for l in all_lines if l.line_type == 'material')
            rec.equipment_total = sum(l.amount for l in all_lines if l.line_type == 'equipment')
            rec.labour_total = sum(l.amount for l in all_lines if l.line_type == 'labour')
            rec.overhead_total = sum(l.amount for l in all_lines if l.line_type == 'overhead')
            rec.other_total = sum(l.amount for l in all_lines if l.line_type == 'other')
            rec.total_amount = rec.material_total + rec.equipment_total + rec.labour_total + rec.overhead_total + rec.other_total


class ConstructionRateAnalysisLine(models.Model):
    _name = 'el_construction.rate.analysis.line'
    _description = 'Rate Analysis Line'

    rate_analysis_id = fields.Many2one('el_construction.rate.analysis', string='Rate Analysis', required=True, ondelete='cascade', index=True)
    line_type = fields.Selection([
        ('material', 'Material'),
        ('equipment', 'Equipment'),
        ('labour', 'Labour'),
        ('overhead', 'Overhead'),
        ('other', 'Other'),
    ], string='Type', required=True, default='material')

    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)

    @api.constrains('quantity', 'unit_price', 'uom_id', 'product_id')
    def _check_values(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_('Rate Analysis quantity must be greater than zero.'))
            if line.unit_price < 0:
                raise ValidationError(_('Rate Analysis unit price cannot be negative.'))
            if line.product_id and line.uom_id and line.product_id.uom_id and not line.uom_id._has_common_reference(line.product_id.uom_id):
                raise ValidationError(_('Rate Analysis Unit of Measure must use the same category as the Product.'))

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.uom_id = self.product_id.uom_id.id
            self.unit_price = self.product_id.standard_price
