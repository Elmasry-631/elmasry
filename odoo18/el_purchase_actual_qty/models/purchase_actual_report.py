from odoo import api, fields, models, tools


class PurchaseActualReport(models.Model):
    _name = "el.purchase.actual.report"
    _description = "Purchase Actual Quantity Analysis"
    _auto = False
    _rec_name = "order_name"
    _order = "order_date desc, id desc"

    order_id = fields.Many2one("purchase.order", readonly=True)
    order_name = fields.Char(string="PO", readonly=True)
    order_date = fields.Datetime(string="Order Date", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Vendor", readonly=True)
    product_id = fields.Many2one("product.product", string="Product", readonly=True)
    product_tmpl_id = fields.Many2one("product.template", string="Product Template", readonly=True)
    product_category_id = fields.Many2one("product.category", string="Product Category", readonly=True)
    company_id = fields.Many2one("res.company", readonly=True)
    currency_id = fields.Many2one("res.currency", readonly=True)
    buyer_id = fields.Many2one("res.users", string="Buyer", readonly=True)
    ordered_qty = fields.Float(string="Ordered Qty", readonly=True)
    actual_qty = fields.Float(string="Actual Qty", readonly=True)
    variance_qty = fields.Float(string="Variance Qty", readonly=True)
    variance_percent = fields.Float(string="Variance %", readonly=True)
    purchase_value = fields.Monetary(currency_field="currency_id", readonly=True)
    effective_unit_cost = fields.Monetary(currency_field="currency_id", readonly=True)
    variance_status = fields.Selection(
        [("none", "No Variance"), ("low", "Low"), ("medium", "Medium"), ("high", "High")],
        readonly=True,
    )

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW el_purchase_actual_report AS (
                SELECT
                    pol.id AS id,
                    po.id AS order_id,
                    po.name AS order_name,
                    po.date_order AS order_date,
                    po.partner_id AS partner_id,
                    pol.product_id AS product_id,
                    pt.id AS product_tmpl_id,
                    pt.categ_id AS product_category_id,
                    po.company_id AS company_id,
                    po.currency_id AS currency_id,
                    po.user_id AS buyer_id,
                    pol.product_qty AS ordered_qty,
                    pol.actual_qty AS actual_qty,
                    pol.product_qty - pol.actual_qty AS variance_qty,
                    CASE WHEN pol.product_qty = 0 THEN 0
                         ELSE (pol.product_qty - pol.actual_qty) / pol.product_qty * 100 END AS variance_percent,
                    pol.price_unit * pol.product_qty * (1 - pol.discount / 100.0) AS purchase_value,
                    CASE WHEN pol.actual_qty = 0 THEN 0
                         ELSE pol.price_unit * pol.product_qty * (1 - pol.discount / 100.0) / pol.actual_qty END AS effective_unit_cost,
                    CASE
                        WHEN pol.product_qty = 0 OR abs(pol.product_qty - pol.actual_qty) < 0.000001 THEN 'none'
                        WHEN abs((pol.product_qty - pol.actual_qty) / pol.product_qty) * 100 < 5 THEN 'low'
                        WHEN abs((pol.product_qty - pol.actual_qty) / pol.product_qty) * 100 < 10 THEN 'medium'
                        ELSE 'high'
                    END AS variance_status
                FROM purchase_order_line pol
                JOIN purchase_order po ON po.id = pol.order_id
                LEFT JOIN product_product pp ON pp.id = pol.product_id
                LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
                WHERE pol.display_type IS NULL
                  AND po.state != 'cancel'
                  AND pol.product_id IS NOT NULL
            )
        """)

    @api.model
    def get_dashboard_data(self, date_from=False, date_to=False, product_id=False):
        domain = [("company_id", "in", self.env.companies.ids)]
        if date_from:
            domain.append(("order_date", ">=", date_from))
        if date_to:
            domain.append(("order_date", "<=", date_to))
        if product_id:
            domain.append(("product_id", "=", product_id))
        rows = self.search_read(
            domain,
            [
                "order_id", "partner_id", "product_id", "product_category_id",
                "ordered_qty", "actual_qty", "variance_qty", "variance_percent",
                "purchase_value", "currency_id", "company_id",
            ],
            order="order_date desc, id desc",
            limit=10000,
        )
        ordered = actual = variance = value = 0.0
        high = 0
        vendors = {}
        products = {}
        for row in rows:
            oq = row["ordered_qty"] or 0.0
            aq = row["actual_qty"] or 0.0
            vq = row["variance_qty"] or 0.0
            ordered += oq
            actual += aq
            variance += vq
            value += row["purchase_value"] or 0.0
            if abs(row["variance_percent"] or 0.0) >= 10:
                high += 1
            vendor = row["partner_id"][1] if row["partner_id"] else "Undefined"
            product_id_val = row["product_id"][0] if row["product_id"] else False
            product = row["product_id"][1] if row["product_id"] else "Undefined"
            for bucket, key in ((vendors, vendor), (products, product)):
                item = bucket.setdefault(key, {"name": key, "id": product_id_val, "ordered": 0.0, "actual": 0.0, "variance": 0.0, "value": 0.0})
                item["ordered"] += oq
                item["actual"] += aq
                item["variance"] += vq
                item["value"] += row["purchase_value"] or 0.0
        return {
            "kpis": {
                "lines": len(rows),
                "ordered": ordered,
                "actual": actual,
                "variance": variance,
                "variance_percent": ordered and variance / ordered * 100.0 or 0.0,
                "value": value,
                "high": high,
            },
            "vendors": sorted(vendors.values(), key=lambda x: abs(x["variance"]), reverse=True)[:10],
            "products": sorted(products.values(), key=lambda x: abs(x["variance"]), reverse=True)[:10],
        }
