from odoo import fields, models, _


class ConstructionStockMove(models.Model):
    _inherit = 'stock.move'

    construction_material_issue_id = fields.Many2one(
        'el_construction.material.issue', string='Construction Stock Operation',
        index=True, copy=False,
    )
    material_requisition_line_id = fields.Many2one(
        'el_construction.material.requisition.line',
        string='Material Requisition Line', index=True, ondelete='set null', copy=False,
    )

    def _create_construction_actual_cost_entry(self):
        Cost = self.env['el_construction.cost.entry']
        Valuation = self.env['stock.valuation.layer']
        for move in self: 
            issue = move.construction_material_issue_id
            if not issue or issue.issue_type not in ('consume', 'wastage'):
                continue
            if issue.state != 'done' or not issue.project_id:
                continue
            layers = Valuation.search([('stock_move_id', '=', move.id)])
            amount = abs(sum(layers.mapped('value')))
            if not amount:
                continue
            Cost.create_from_source({
                'name': _('Material %s: %s') % (issue.issue_type.title(), move.reference or move.name),
                'project_id': issue.project_id.id,
                'sub_project_id': issue.sub_project_id.id,
                'date': move.date.date() if move.date else fields.Date.context_today(issue),
                'cost_type': 'actual',
                'cost_category': 'material',
                'amount': amount,
                'analytic_account_id': issue.project_id.analytic_account_id.id,
                'source_model': 'stock.move',
                'source_res_id': move.id,
                'source_ref': move.reference or move.name,
            })


class ConstructionStockPicking(models.Model):
    _inherit = 'stock.picking'

    construction_material_issue_id = fields.Many2one(
        'el_construction.material.issue', string='Construction Stock Operation',
        index=True, copy=False,
    )
    material_requisition_id = fields.Many2one(
        'el_construction.material.requisition', string='Material Requisition',
        index=True, ondelete='set null', copy=False,
    )

    def _action_done(self):
        result = super()._action_done()
        linked = self.mapped('construction_material_issue_id').filtered(lambda op: op.state == 'confirmed')
        linked._transition('done', {'confirmed': {'done'}})
        self.mapped('move_ids')._create_construction_actual_cost_entry()
        return result


class ConstructionStockScrap(models.Model):
    _inherit = 'stock.scrap'

    construction_material_issue_id = fields.Many2one(
        'el_construction.material.issue', string='Construction Stock Operation',
        index=True, copy=False,
    )

    def action_validate(self):
        result = super().action_validate()
        for scrap in self:
            issue = scrap.construction_material_issue_id
            move = scrap.move_id
            if issue and move:
                move.construction_material_issue_id = issue.id
                move._create_construction_actual_cost_entry()
        linked = self.mapped('construction_material_issue_id').filtered(lambda op: op.state == 'confirmed')
        linked._transition('done', {'confirmed': {'done'}})
        return result
