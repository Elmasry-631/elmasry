import base64
import io

from odoo import api, fields, models, _
from odoo.exceptions import UserError


REPORTS = {
    'project': ('Project Dossier', 'el_construction.project', 'action_report_project'),
    'sub_project': ('Sub Project', 'el_construction.sub.project', 'action_report_sub_project'),
    'boq': ('BOQ', 'el_construction.boq', 'action_report_boq'),
    'rate_analysis': ('Rate Analysis', 'el_construction.rate.analysis', 'action_report_rate_analysis'),
    'budget': ('Budget', 'el_construction.budget', 'action_report_budget'),
    'phase': ('Phase / WBS', 'el_construction.phase', 'action_report_phase'),
    'work_order': ('Work Order', 'el_construction.work.order', 'action_report_work_order'),
    'material_requisition': ('Material Requisition', 'el_construction.material.requisition', 'action_report_material_requisition'),
    'subcontract': ('Subcontract', 'el_construction.subcontract', 'action_report_subcontract'),
    'consume_order': ('Consume Order', 'el_construction.consume.order', 'action_report_consume_order'),
    'ra_billing': ('RA Billing', 'el_construction.ra.billing', 'action_report_ra_billing'),
    'progress_billing': ('Progress Billing', 'el_construction.progress.billing', 'action_report_progress_billing'),
    'quality_check': ('Quality Inspection', 'el_construction.quality.check', 'action_report_quality_check'),
    'task': ('Task', 'el_construction.task', 'action_report_task'),
    'extra_expense': ('Extra Expense', 'el_construction.extra.expense', 'action_report_extra_expense'),
    'permit': ('Permit', 'el_construction.permit', 'action_report_permit'),
    'timesheet': ('Timesheet', 'el_construction.timesheet', 'action_report_timesheet'),
}


class ConstructionReportWizard(models.TransientModel):
    _name = 'el_construction.report.wizard'
    _description = 'Construction Report Center'

    report_type = fields.Selection(
        [(key, value[0]) for key, value in REPORTS.items()],
        string='Report', required=True,
    )
    output_format = fields.Selection([
        ('pdf', 'PDF'), ('xlsx', 'Excel (.xlsx)'),
    ], string='Output', default='pdf', required=True)
    project_id = fields.Many2one('el_construction.project', string='Project')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    include_archived = fields.Boolean(string='Include Archived', default=False)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        ctx_report = self.env.context.get('default_report_type') or self.env.context.get('report_type')
        if ctx_report in REPORTS:
            res['report_type'] = ctx_report
        ctx_project = self.env.context.get('default_project_id')
        if ctx_project:
            res['project_id'] = ctx_project
        return res

    def _get_records(self):
        self.ensure_one()
        if self.report_type not in REPORTS:
            raise UserError(_('Please select a report.'))
        _, model_name, _ = REPORTS[self.report_type]
        model = self.env[model_name]
        domain = []
        if 'project_id' in model._fields and self.project_id:
            domain.append(('project_id', '=', self.project_id.id))
        if 'active' in model._fields and not self.include_archived:
            domain.append(('active', '=', True))
        date_field = next((f for f in ('date', 'date_start', 'inspection_date') if f in model._fields), None)
        if date_field and self.date_from:
            domain.append((date_field, '>=', self.date_from))
        if date_field and self.date_to:
            domain.append((date_field, '<=', self.date_to))
        records = model.search(domain, order='id desc')
        if not records:
            raise UserError(_('No records match the selected report filters.'))
        return records

    def action_print(self):
        self.ensure_one()
        records = self._get_records()
        _, _, action_id = REPORTS[self.report_type]
        if self.output_format == 'pdf':
            return self.env.ref('el_construction_management.%s' % action_id).report_action(records)
        return self._action_excel(records)

    def _action_excel(self, records):
        try:
            import xlsxwriter
        except ImportError as exc:
            raise UserError(_('Excel export requires the Python package xlsxwriter on the Odoo server.')) from exc
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        title_fmt = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center', 'valign': 'vcenter'})
        header_fmt = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#E8EEF5'})
        text_fmt = workbook.add_format({'border': 1})
        amount_fmt = workbook.add_format({'border': 1, 'num_format': '#,##0.00'})
        for key, value in REPORTS.items():
            if key == self.report_type:
                report_title = value[0]
                break
        sheet = workbook.add_worksheet(report_title[:31])
        sheet.merge_range(0, 0, 0, 5, report_title, title_fmt)
        sheet.write(1, 0, 'Generated', header_fmt)
        sheet.write(1, 1, fields.Datetime.now().strftime('%Y-%m-%d %H:%M'))
        sheet.write(2, 0, 'Records', header_fmt)
        sheet.write(2, 1, len(records))
        columns = ['ID', 'Reference / Name', 'Project', 'Date', 'Status', 'Amount']
        for col, label in enumerate(columns):
            sheet.write(4, col, label, header_fmt)
        for row, rec in enumerate(records, start=5):
            name = rec.display_name or ''
            project = getattr(rec, 'project_id', False)
            date_value = getattr(rec, 'date', False) or getattr(rec, 'date_start', False)
            state = getattr(rec, 'state', False)
            amount = (getattr(rec, 'total_amount', 0.0) or getattr(rec, 'amount', 0.0) or 0.0) if hasattr(rec, '_fields') else 0.0
            sheet.write(row, 0, rec.id, text_fmt)
            sheet.write(row, 1, name, text_fmt)
            sheet.write(row, 2, project.display_name if project else '', text_fmt)
            sheet.write(row, 3, str(date_value or ''), text_fmt)
            sheet.write(row, 4, state or '', text_fmt)
            sheet.write_number(row, 5, float(amount or 0.0), amount_fmt)
        sheet.set_column('A:A', 10)
        sheet.set_column('B:B', 34)
        sheet.set_column('C:C', 28)
        sheet.set_column('D:E', 18)
        sheet.set_column('F:F', 18)
        workbook.close()
        output.seek(0)
        attachment = self.env['ir.attachment'].create({
            'name': '%s.xlsx' % report_title.replace('/', '-'),
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }


class ConstructionReportMenuWizard(models.TransientModel):
    _name = 'el_construction.report.menu.wizard'
    _description = 'Construction Report Menu Wizard'

    report_type = fields.Selection(
        [(key, value[0]) for key, value in REPORTS.items()], string='Report', required=True,
    )
    output_format = fields.Selection([('pdf', 'PDF'), ('xlsx', 'Excel (.xlsx)')], string='Output', default='pdf', required=True)
    project_id = fields.Many2one('el_construction.project', string='Project')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def action_print(self):
        values = {
            'report_type': self.report_type, 'output_format': self.output_format,
            'project_id': self.project_id.id, 'date_from': self.date_from, 'date_to': self.date_to,
        }
        wiz = self.env['el_construction.report.wizard'].create(values)
        return wiz.action_print()
