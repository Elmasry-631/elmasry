from odoo import models, fields, api, _


class ConstructionTenderRfqCompareWizard(models.TransientModel):
    _name = 'el_construction.tender.rfq.compare.wizard'
    _description = 'RFQ Bid Comparison'

    rfq_id = fields.Many2one('el_construction.tender.rfq', string='RFQ', required=True, readonly=True)
    vendor_ids = fields.One2many(related='rfq_id.vendor_ids', string='Vendors', readonly=True)
    comparison_html = fields.Html(string='Comparison Matrix', compute='_compute_comparison_html', sanitize=False)

    @api.depends('rfq_id', 'rfq_id.vendor_ids.bid_line_ids.unit_price', 'rfq_id.line_ids')
    def _compute_comparison_html(self):
        for wiz in self:
            rfq = wiz.rfq_id
            vendors = rfq.vendor_ids
            lines = rfq.line_ids
            if not vendors or not lines:
                wiz.comparison_html = '<p class="text-muted">No vendors or requested items to compare yet.</p>'
                continue

            head_cells = ''.join(
                '<th style="padding:6px 10px;border-bottom:2px solid #cbd5e1;text-align:right;white-space:nowrap;">%s</th>'
                % (v.partner_id.display_name or '')
                for v in vendors
            )
            body_rows = ''
            for line in lines:
                row_cells = ''
                for v in vendors:
                    bid = v.bid_line_ids.filtered(lambda b: b.rfq_line_id == line)
                    if bid and bid[0].is_lowest and bid[0].unit_price:
                        style = ('padding:6px 10px;text-align:right;background:#dcfce7;'
                                 'font-weight:700;color:#166534;')
                    else:
                        style = 'padding:6px 10px;text-align:right;'
                    value = ('%.2f' % bid[0].unit_price) if bid and bid[0].unit_price else '—'
                    row_cells += '<td style="%s">%s</td>' % (style, value)
                body_rows += (
                    '<tr><td style="padding:6px 10px;border-bottom:1px solid #e5e7eb;">%s</td>%s</tr>'
                    % (line.description or '', row_cells)
                )
            total_cells = ''.join(
                '<td style="padding:6px 10px;text-align:right;font-weight:700;border-top:2px solid #cbd5e1;">%.2f</td>'
                % v.total_amount
                for v in vendors
            )
            wiz.comparison_html = (
                '<table style="width:100%%;border-collapse:collapse;font-size:13px;">'
                '<thead><tr><th style="padding:6px 10px;border-bottom:2px solid #cbd5e1;text-align:left;">Item</th>%s</tr></thead>'
                '<tbody>%s</tbody>'
                '<tfoot><tr><td style="padding:6px 10px;border-top:2px solid #cbd5e1;font-weight:700;">Total</td>%s</tr></tfoot>'
                '</table>'
            ) % (head_cells, body_rows, total_cells)
