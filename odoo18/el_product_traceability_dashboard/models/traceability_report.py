from datetime import timedelta

from odoo import api, fields, models, tools


class ProductTraceabilityReport(models.Model):
    _name = "el.product.traceability.report"
    _description = "Product Traceability Movement Report"
    _auto = False
    _rec_name = "product_id"
    _order = "date desc, id desc"

    date = fields.Datetime(readonly=True)
    company_id = fields.Many2one("res.company", readonly=True)
    warehouse_id = fields.Many2one("stock.warehouse", readonly=True)
    product_id = fields.Many2one("product.product", readonly=True)
    product_tmpl_id = fields.Many2one("product.template", readonly=True)
    categ_id = fields.Many2one("product.category", readonly=True)
    lot_id = fields.Many2one("stock.lot", readonly=True)
    move_line_id = fields.Many2one("stock.move.line", readonly=True)
    move_id = fields.Many2one("stock.move", readonly=True)
    picking_id = fields.Many2one("stock.picking", readonly=True)
    production_id = fields.Many2one("mrp.production", readonly=True)
    purchase_order_id = fields.Many2one("purchase.order", readonly=True)
    purchase_line_id = fields.Many2one("purchase.order.line", readonly=True)
    sale_order_id = fields.Many2one("sale.order", readonly=True)
    partner_id = fields.Many2one("res.partner", readonly=True)
    location_id = fields.Many2one("stock.location", readonly=True)
    location_dest_id = fields.Many2one("stock.location", readonly=True)
    uom_id = fields.Many2one("uom.uom", readonly=True)
    operation_type = fields.Selection([
        ("receipt", "Purchase Receipt"),
        ("vendor_return", "Vendor Return"),
        ("manufacturing_consume", "Manufacturing Consumption"),
        ("manufacturing_produce", "Manufacturing Production"),
        ("internal", "Internal Transfer"),
        ("delivery", "Customer Delivery"),
        ("customer_return", "Customer Return"),
        ("scrap", "Scrap / Waste"),
        ("adjustment", "Inventory Adjustment"),
    ], readonly=True)
    reference = fields.Char(readonly=True)
    source_document = fields.Char(readonly=True)
    quantity = fields.Float(readonly=True)
    signed_quantity = fields.Float(readonly=True)
    unit_cost = fields.Float(readonly=True)
    total_value = fields.Float(readonly=True)
    purchase_unit_price = fields.Float(readonly=True)
    purchase_total_value = fields.Float(readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW el_product_traceability_report AS (
                SELECT
                    sml.id AS id,
                    sm.date AS date,
                    sm.company_id AS company_id,
                    wh.id AS warehouse_id,
                    sm.product_id AS product_id,
                    pp.product_tmpl_id AS product_tmpl_id,
                    pt.categ_id AS categ_id,
                    sml.lot_id AS lot_id,
                    sml.id AS move_line_id,
                    sm.id AS move_id,
                    sm.picking_id AS picking_id,
                    COALESCE(sm.raw_material_production_id, sm.production_id) AS production_id,
                    pol.order_id AS purchase_order_id,
                    pol.id AS purchase_line_id,
                    so.id AS sale_order_id,
                    COALESCE(po.partner_id, so.partner_id, sp.partner_id) AS partner_id,
                    sm.location_id AS location_id,
                    sm.location_dest_id AS location_dest_id,
                    sml.product_uom_id AS uom_id,
                    CASE
                        WHEN ss.id IS NOT NULL THEN 'scrap'
                        WHEN sm.raw_material_production_id IS NOT NULL THEN 'manufacturing_consume'
                        WHEN sm.production_id IS NOT NULL THEN 'manufacturing_produce'
                        WHEN spt.code = 'incoming' AND sm.origin_returned_move_id IS NOT NULL THEN 'customer_return'
                        WHEN spt.code = 'outgoing' AND sm.origin_returned_move_id IS NOT NULL THEN 'vendor_return'
                        WHEN spt.code = 'incoming' THEN 'receipt'
                        WHEN spt.code = 'outgoing' THEN 'delivery'
                        WHEN spt.code = 'internal' THEN 'internal'
                        WHEN sl_src.usage = 'inventory' OR sl_dst.usage = 'inventory' THEN 'adjustment'
                        ELSE 'adjustment'
                    END AS operation_type,
                    COALESCE(sm.reference, sp.name, mo.name, ss.name, 'Stock Move') AS reference,
                    COALESCE(po.name, so.name, mo.name, sp.origin, ss.name, sm.origin, '') AS source_document,
                    sml.quantity AS quantity,
                    CASE
                        WHEN ss.id IS NOT NULL THEN -sml.quantity
                        WHEN sm.raw_material_production_id IS NOT NULL THEN -sml.quantity
                        WHEN sm.production_id IS NOT NULL THEN sml.quantity
                        WHEN spt.code = 'outgoing' AND sm.origin_returned_move_id IS NULL THEN -sml.quantity
                        WHEN spt.code = 'incoming' THEN sml.quantity
                        WHEN spt.code = 'outgoing' AND sm.origin_returned_move_id IS NOT NULL THEN -sml.quantity
                        WHEN spt.code = 'internal' THEN 0.0
                        WHEN sl_dst.usage = 'internal' AND sl_src.usage = 'inventory' THEN sml.quantity
                        WHEN sl_src.usage = 'internal' AND sl_dst.usage = 'inventory' THEN -sml.quantity
                        ELSE 0.0
                    END AS signed_quantity,
                    CASE
                        WHEN COALESCE(svl.quantity, 0) = 0 THEN 0.0
                        ELSE ABS(COALESCE(svl.value, 0.0) / NULLIF(svl.quantity, 0))
                    END AS unit_cost,
                    CASE
                        WHEN COALESCE(svl.quantity, 0) = 0 THEN 0.0
                        ELSE ABS(COALESCE(svl.value, 0.0) * (sml.quantity / NULLIF(svl.quantity, 0)))
                    END AS total_value,
                    CASE WHEN spt.code = 'incoming' AND sm.origin_returned_move_id IS NULL
                         THEN COALESCE(pol.price_unit, 0.0) ELSE 0.0 END AS purchase_unit_price,
                    CASE WHEN spt.code = 'incoming' AND sm.origin_returned_move_id IS NULL
                         THEN sml.quantity * COALESCE(pol.price_unit, 0.0) ELSE 0.0 END AS purchase_total_value
                FROM stock_move_line sml
                JOIN stock_move sm ON sm.id = sml.move_id
                JOIN product_product pp ON pp.id = sm.product_id
                JOIN product_template pt ON pt.id = pp.product_tmpl_id
                LEFT JOIN stock_picking sp ON sp.id = sm.picking_id
                LEFT JOIN stock_picking_type spt ON spt.id = sp.picking_type_id
                LEFT JOIN stock_location sl_src ON sl_src.id = sm.location_id
                LEFT JOIN stock_location sl_dst ON sl_dst.id = sm.location_dest_id
                LEFT JOIN stock_scrap ss ON ss.id = sm.scrap_id
                LEFT JOIN mrp_production mo ON mo.id = COALESCE(sm.raw_material_production_id, sm.production_id)
                LEFT JOIN purchase_order_line pol ON pol.id = sm.purchase_line_id
                LEFT JOIN purchase_order po ON po.id = pol.order_id
                LEFT JOIN sale_order_line sol ON sol.id = sm.sale_line_id
                LEFT JOIN sale_order so ON so.id = sol.order_id
                LEFT JOIN stock_warehouse wh ON wh.id = spt.warehouse_id
                LEFT JOIN LATERAL (
                    SELECT
                        COALESCE(SUM(svl2.value), 0.0) AS value,
                        COALESCE(SUM(svl2.quantity), 0.0) AS quantity
                    FROM stock_valuation_layer svl2
                    WHERE svl2.stock_move_id = sm.id
                ) svl ON TRUE
                WHERE sm.state = 'done'
            )
        """)


class ProductTraceabilityManufacturing(models.Model):
    _name = "el.product.traceability.manufacturing"
    _description = "Product Traceability Manufacturing Genealogy"
    _auto = False
    _rec_name = "production_id"
    _order = "date desc, production_id desc"

    date = fields.Datetime(readonly=True)
    company_id = fields.Many2one("res.company", readonly=True)
    production_id = fields.Many2one("mrp.production", readonly=True)
    finished_product_id = fields.Many2one("product.product", readonly=True)
    finished_uom_id = fields.Many2one("uom.uom", readonly=True)
    finished_qty = fields.Float(readonly=True)
    component_product_id = fields.Many2one("product.product", readonly=True)
    component_uom_id = fields.Many2one("uom.uom", readonly=True)
    component_qty = fields.Float(readonly=True)
    component_value = fields.Float(readonly=True)
    state = fields.Char(readonly=True)
    reference = fields.Char(readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW el_product_traceability_manufacturing AS (
                SELECT
                    (raw.move_id::bigint * 1000000000 + fin.move_id) AS id,
                    mo.date_start AS date,
                    mo.company_id AS company_id,
                    mo.id AS production_id,
                    fin.product_id AS finished_product_id,
                    fin.product_uom_id AS finished_uom_id,
                    fin.quantity AS finished_qty,
                    raw.product_id AS component_product_id,
                    raw.product_uom_id AS component_uom_id,
                    raw.quantity AS component_qty,
                    CASE
                        WHEN COALESCE(svl.quantity, 0) = 0 THEN 0.0
                        ELSE ABS(COALESCE(svl.value, 0.0) * (raw.quantity / NULLIF(svl.quantity, 0)))
                    END AS component_value,
                    mo.state AS state,
                    mo.name AS reference
                FROM mrp_production mo
                JOIN (
                    SELECT
                        sm.id AS move_id,
                        sm.raw_material_production_id AS production_id,
                        sm.product_id,
                        sm.product_uom AS product_uom_id,
                        SUM(sml.quantity) AS quantity
                    FROM stock_move sm
                    JOIN stock_move_line sml ON sml.move_id = sm.id
                    WHERE sm.state = 'done' AND sm.raw_material_production_id IS NOT NULL
                    GROUP BY sm.id, sm.raw_material_production_id, sm.product_id, sm.product_uom
                ) raw ON raw.production_id = mo.id
                JOIN (
                    SELECT
                        sm.id AS move_id,
                        sm.production_id,
                        sm.product_id,
                        sm.product_uom AS product_uom_id,
                        SUM(sml.quantity) AS quantity
                    FROM stock_move sm
                    JOIN stock_move_line sml ON sml.move_id = sm.id
                    WHERE sm.state = 'done' AND sm.production_id IS NOT NULL
                    GROUP BY sm.id, sm.production_id, sm.product_id, sm.product_uom
                ) fin ON fin.production_id = mo.id
                LEFT JOIN LATERAL (
                    SELECT COALESCE(SUM(svl2.value), 0.0) AS value, COALESCE(SUM(svl2.quantity), 0.0) AS quantity
                    FROM stock_valuation_layer svl2
                    WHERE svl2.stock_move_id = raw.move_id
                ) svl ON TRUE
            )
        """)


class ProductTraceabilityDashboard(models.TransientModel):
    _name = "el.product.traceability.dashboard"
    _description = "Product Traceability Dashboard"

    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)
    date_from = fields.Date()
    date_to = fields.Date(default=fields.Date.context_today)

    def action_open_report(self):
        action = self.env.ref("el_product_traceability_dashboard.action_product_traceability_report").read()[0]
        domain = [("company_id", "=", self.company_id.id)]
        if self.date_from:
            domain.append(("date", ">=", fields.Datetime.to_datetime(self.date_from)))
        if self.date_to:
            end = fields.Datetime.to_datetime(self.date_to)
            domain.append(("date", "<", end + timedelta(days=1)))
        action["domain"] = domain
        return action

    @api.model
    def get_dashboard_data(self, filters=None):
        filters = filters or {}
        company_id = filters.get("company_id") or self.env.company.id
        domain = [("company_id", "=", company_id)]
        for key, op in (("date_from", ">="), ("date_to", "<=")):
            if filters.get(key):
                value = filters[key]
                if key == "date_to" and len(value) == 10:
                    value = f"{value} 23:59:59"
                domain.append(("date", op, value))
        for field_name in ("product_id", "categ_id", "partner_id", "lot_id", "warehouse_id", "operation_type"):
            value = filters.get(field_name)
            if value:
                domain.append((field_name, "=", value))

        Report = self.env["el.product.traceability.report"]
        rows = Report.search_read(
            domain,
            [
                "date", "operation_type", "product_id", "lot_id", "partner_id", "warehouse_id",
                "quantity", "signed_quantity", "total_value", "purchase_total_value", "reference",
                "source_document", "production_id", "purchase_order_id", "sale_order_id",
            ],
            limit=30000,
            order="date desc, id desc",
        )

        zero = lambda: {"qty": 0.0, "value": 0.0, "count": 0}
        metrics = {
            "receipt": zero(), "vendor_return": zero(), "manufacturing_consume": zero(),
            "manufacturing_produce": zero(), "internal": zero(), "delivery": zero(),
            "customer_return": zero(), "scrap": zero(), "adjustment": zero(),
        }
        products = {}
        vendors = {}
        activity = []
        manufacturing_mos = set()
        purchase_orders = set()
        lots = set()

        for row in rows:
            op = row.get("operation_type") or "adjustment"
            bucket = metrics.setdefault(op, zero())
            qty = row.get("quantity") or 0.0
            value = row.get("total_value") or 0.0
            bucket["qty"] += qty
            bucket["value"] += value
            bucket["count"] += 1
            if row.get("production_id"):
                manufacturing_mos.add(row["production_id"][0])
            if row.get("purchase_order_id"):
                purchase_orders.add(row["purchase_order_id"][0])
            if row.get("lot_id"):
                lots.add(row["lot_id"][0])

            product = row.get("product_id")
            if product:
                pid = product[0]
                item = products.setdefault(pid, {
                    "product_id": pid, "product_name": product[1], "qty_in": 0.0,
                    "qty_out": 0.0, "produced_qty": 0.0, "consumed_qty": 0.0,
                    "returned_qty": 0.0, "scrap_qty": 0.0, "movement_value": 0.0,
                })
                item["movement_value"] += value
                if op in ("receipt", "customer_return", "manufacturing_produce", "adjustment"):
                    item["qty_in"] += qty
                if op in ("delivery", "vendor_return", "manufacturing_consume", "scrap"):
                    item["qty_out"] += qty
                if op == "manufacturing_produce": item["produced_qty"] += qty
                if op == "manufacturing_consume": item["consumed_qty"] += qty
                if op in ("customer_return", "vendor_return"): item["returned_qty"] += qty
                if op == "scrap": item["scrap_qty"] += qty

            partner = row.get("partner_id")
            if partner and op in ("receipt", "vendor_return"):
                key = partner[0]
                vendor = vendors.setdefault(key, {"partner_id": key, "partner_name": partner[1], "received": 0.0, "returned": 0.0})
                if op == "receipt": vendor["received"] += qty
                else: vendor["returned"] += qty

            if len(activity) < 30:
                activity.append({
                    "date": row.get("date"), "operation_type": op,
                    "product_name": product[1] if product else "-",
                    "quantity": qty, "reference": row.get("reference") or "-",
                    "source_document": row.get("source_document") or "-",
                    "lot_name": row["lot_id"][1] if row.get("lot_id") else "-",
                })

        manufacturing_domain = [("company_id", "=", company_id)]
        if filters.get("date_from"):
            manufacturing_domain.append(("date", ">=", filters["date_from"]))
        if filters.get("date_to"):
            manufacturing_domain.append(("date", "<=", f"{filters['date_to']} 23:59:59"))
        if filters.get("product_id"):
            manufacturing_domain.append(("component_product_id", "=", filters["product_id"]))
        manufacturing = self.env["el.product.traceability.manufacturing"].search_read(
            manufacturing_domain,
            ["date", "production_id", "finished_product_id", "finished_qty", "component_product_id", "component_qty", "component_value", "reference"],
            limit=5000,
            order="date desc, id desc",
        )

        return {
            "metrics": metrics,
            "totals": {
                "movement_count": len(rows), "manufacturing_orders": len(manufacturing_mos),
                "purchase_orders": len(purchase_orders), "lots": len(lots),
                "current_stock": self._current_stock(company_id, filters),
            },
            "products": sorted(products.values(), key=lambda x: x["movement_value"], reverse=True)[:30],
            "vendors": sorted(vendors.values(), key=lambda x: x["received"], reverse=True)[:15],
            "activity": activity,
            "manufacturing": manufacturing[:100],
        }

    def _current_stock(self, company_id, filters):
        domain = [("company_id", "=", company_id)]
        if filters.get("product_id"):
            domain.append(("product_id", "=", filters["product_id"]))
        if filters.get("warehouse_id"):
            warehouse = self.env["stock.warehouse"].browse(filters["warehouse_id"])
            if warehouse.exists():
                domain.append(("location_id", "child_of", warehouse.view_location_id.id))
        quants = self.env["stock.quant"].search(domain, limit=100000)
        return sum(q.quantity for q in quants if q.location_id.usage == "internal")

    @api.model
    def get_filter_options(self, company_id=None):
        company_id = company_id or self.env.company.id
        Report = self.env["el.product.traceability.report"]
        base = [("company_id", "=", company_id)]
        products = Report.read_group(base, ["product_id"], ["product_id"], limit=5000)
        vendors = Report.read_group(base + [("partner_id", "!=", False)], ["partner_id"], ["partner_id"], limit=2000)
        lots = Report.read_group(base + [("lot_id", "!=", False)], ["lot_id"], ["lot_id"], limit=5000)
        warehouses = Report.read_group(base + [("warehouse_id", "!=", False)], ["warehouse_id"], ["warehouse_id"], limit=500)
        categories = Report.read_group(base + [("categ_id", "!=", False)], ["categ_id"], ["categ_id"], limit=1000)
        return {
            "products": [{"id": x["product_id"][0], "name": x["product_id"][1]} for x in products if x.get("product_id")],
            "vendors": [{"id": x["partner_id"][0], "name": x["partner_id"][1]} for x in vendors if x.get("partner_id")],
            "lots": [{"id": x["lot_id"][0], "name": x["lot_id"][1]} for x in lots if x.get("lot_id")],
            "warehouses": [{"id": x["warehouse_id"][0], "name": x["warehouse_id"][1]} for x in warehouses if x.get("warehouse_id")],
            "categories": [{"id": x["categ_id"][0], "name": x["categ_id"][1]} for x in categories if x.get("categ_id")],
        }
