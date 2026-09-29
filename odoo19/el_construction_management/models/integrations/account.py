from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    construction_subcontract_id = fields.Many2one(
        'el_construction.subcontract', string='Construction Subcontract',
        index=True, ondelete='set null',
    )
    construction_progress_billing_id = fields.Many2one(
        'el_construction.progress.billing', string='Construction Progress Billing',
        index=True, ondelete='set null',
    )

    @api.constrains('construction_subcontract_id', 'company_id')
    def _check_construction_subcontract_company(self):
        for move in self:
            if (move.construction_subcontract_id
                    and move.company_id != move.construction_subcontract_id.company_id):
                raise ValidationError(_('Vendor Bill company must match the Construction Subcontract company.'))

    def action_post(self):
        result = super().action_post()
        Expense = self.env['el_construction.extra.expense']
        BudgetLine = self.env['el_construction.budget.line']
        for move in self.filtered(lambda m: m.move_type == 'in_invoice' and m.state == 'posted'):
            purchase_orders = move.invoice_line_ids.mapped('purchase_line_id.order_id')
            for po in purchase_orders:
                mreq = po.material_requisition_id
                if not mreq or not mreq.project_id:
                    continue
                invoice_lines = move.invoice_line_ids.filtered(
                    lambda line: line.purchase_line_id.order_id == po
                )
                for inv_line in invoice_lines:
                    if Expense.search_count([('source_move_line_id', '=', inv_line.id)]):
                        continue
                    domain = [
                        ('project_id', '=', mreq.project_id.id),
                        ('product_id', '=', inv_line.product_id.id),
                    ] if inv_line.product_id else [('project_id', '=', mreq.project_id.id)]
                    if mreq.sub_project_id:
                        domain.append(('sub_project_id', '=', mreq.sub_project_id.id))
                    budget_line = BudgetLine.search(domain, limit=1)
                    expense = Expense.create({
                        'project_id': mreq.project_id.id,
                        'sub_project_id': mreq.sub_project_id.id,
                        'company_id': move.company_id.id,
                        'product_id': inv_line.product_id.id,
                        'budget_line_id': budget_line.id if budget_line else False,
                        'quantity': inv_line.quantity,
                        'unit_price': inv_line.price_unit,
                        'description': f'Auto from Bill {move.name} - PO {po.name}',
                        'source_move_line_id': inv_line.id,
                    })
        return result
