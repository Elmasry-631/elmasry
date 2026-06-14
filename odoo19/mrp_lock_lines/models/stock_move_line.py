from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    is_last_line = fields.Boolean(
        compute="_compute_is_last_line",
        store=False,
        string="Is Last Line",
        help="Indicates whether this is the last component line in the "
             "Manufacturing Order. Only the last line remains editable.",
    )

    @api.depends("production_id")
    def _compute_is_last_line(self):
        productions = self.mapped("production_id")
        for prod in productions:
            lines = self.search(
                [
                    ("move_id.raw_material_production_id", "=", prod.id),
                ],
                order="id asc",
            )
            last_line_id = lines[-1].id if lines else False
            for record in self.filtered(lambda r: r.production_id == prod):
                record.is_last_line = record.id == last_line_id
        for record in self.filtered(lambda r: not r.production_id):
            record.is_last_line = False


class StockMove(models.Model):
    _inherit = "stock.move"

    is_last_line = fields.Boolean(
        compute="_compute_is_last_line",
        store=False,
        string="Is Last Line",
    )

    @api.depends("raw_material_production_id")
    def _compute_is_last_line(self):
        productions = self.mapped("raw_material_production_id")
        for prod in productions:
            lines = self.search(
                [
                    ("raw_material_production_id", "=", prod.id),
                ],
                order="id asc",
            )
            last_line_id = lines[-1].id if lines else False
            for record in self.filtered(lambda r: r.raw_material_production_id == prod):
                record.is_last_line = record.id == last_line_id
        for record in self.filtered(lambda r: not r.raw_material_production_id):
            record.is_last_line = False