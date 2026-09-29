import csv
import io

from odoo import http
from odoo.http import request


class PurchaseActualExportController(http.Controller):
    @http.route("/purchase_actual_qty/export/csv", type="http", auth="user", methods=["GET"])
    def export_csv(self, **kwargs):
        Report = request.env["el.purchase.actual.report"].with_context(
            allowed_company_ids=request.env.companies.ids
        )
        rows = Report.search([], order="order_date desc, id desc")
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "PO", "Vendor", "Product", "Ordered Qty", "Actual Qty",
            "Variance Qty", "Variance %", "Purchase Value", "Effective Unit Cost",
            "Company", "Order Date",
        ])
        for row in rows:
            writer.writerow([
                row.order_name, row.partner_id.display_name, row.product_id.display_name,
                row.ordered_qty, row.actual_qty, row.variance_qty, row.variance_percent,
                row.purchase_value, row.effective_unit_cost, row.company_id.display_name,
                row.order_date.strftime("%Y-%m-%d") if row.order_date else "",
            ])
        return request.make_response(
            output.getvalue().encode("utf-8-sig"),
            headers=[
                ("Content-Type", "text/csv; charset=utf-8"),
                ("Content-Disposition", 'attachment; filename="purchase_actual_quantity.csv"'),
            ],
        )
