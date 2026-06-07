from odoo import models, fields, api, _
from datetime import datetime, timedelta, date
from pytz import timezone, UTC
from odoo.exceptions import ValidationError, UserError

import logging

_logger = logging.getLogger(__name__)


class AdmissionRenewalWizard(models.TransientModel):
    _name = 'admission.renewal.wizard'
    _description = 'Admission Renewal Wizard'

    # الحقول الأساسية
    admission_id = fields.Many2one('student.admission', string='Old Admission', required=True,
                                   default=lambda self: self.env.context.get('active_id'), readonly=True)

    # حقول العميل (تظهر للقراءة فقط افتراضياً)
    client_id = fields.Many2one('res.partner', string='Client', related='admission_id.student_id', readonly=True)
    nurse_specialty_id = fields.Many2one('nurse.specialty', string='Nurse Specialty',
                                         related='admission_id.nurse_specialty_id', readonly=True)

    # حقول الباقة والتمريض (يمكن تغييرها عند التجديد)
    package_id = fields.Many2one('package.package', string='Package', related='admission_id.package_id', readonly=False)
    package_line_id_domain = fields.Many2many('package.package.line', compute='_compute_package_line_id_domain_wizard')
    package_line_ids = fields.Many2one('package.package.line', string='Package Details')
    trainer_id = fields.Many2one('res.partner', string='Nurse', domain="[('is_coach', '=', True)]")

    # حقول الجدول (يمكن تعديلها)
    weekday_ids = fields.Many2many('weekday', string='Days', required=True)
    start_duration = fields.Date(string='Start Date', required=True, default=lambda self: date.today())
    start_time = fields.Float(string='Start Time', help="Ex: 14.30 for 2:30 PM")
    end_time = fields.Float(string='End Time', help="Ex: 16.30 for 4:30 PM")

    # حقول الحساب
    n_of_reservations = fields.Integer(string='Number of Reservations', required=True, default=True, readonly=True)
    is_vip = fields.Boolean(string='VIP')
    duration = fields.Integer("Duration (Days)", compute='_compute_duration', store=True)
    end_duration = fields.Date(string='End Date', compute='_compute_end_duration', store=True, readonly=False)
    driver_id = fields.Many2one('res.partner', string='Driver')
    city_distance = fields.Many2one('city.distance' ,string='City Distance',store=True)

    # تعريف القيم الافتراضية من القبول القديم
    @api.model
    def default_get(self, fields):
        res = super(AdmissionRenewalWizard, self).default_get(fields)
        admission_id = self.env.context.get('active_id')
        if admission_id:
            admission = self.env['student.admission'].browse(admission_id)
            if 'weekday_ids' in fields and not res.get('weekday_ids'):
                res['weekday_ids'] = admission.weekday_ids.ids
            if 'trainer_id' in fields and not res.get('trainer_id'):
                res['trainer_id'] = admission.trainer_id.id
            if 'n_of_reservations' in fields and not res.get('n_of_reservations'):
                res['n_of_reservations'] = admission.n_of_reservations
            if 'is_vip' in fields and not res.get('is_vip'):
                res['is_vip'] = admission.is_vip
            if 'start_time' in fields and not res.get('start_time'):
                res['start_time'] = admission.start_date
            if 'end_time' in fields and not res.get('end_time'):
                res['end_time'] = admission.end_date
            # تعيين تاريخ البدء ليوم بعد انتهاء القبول القديم
            if 'start_duration' in fields and not res.get('start_duration'):
                if admission.end_duration:
                    res['start_duration'] = admission.end_duration + timedelta(days=1)
                else:
                    res['start_duration'] = date.today()
        return res

    @api.depends('start_duration', 'n_of_reservations', 'weekday_ids')
    def _compute_end_duration(self):
        for record in self:
            record.end_duration = False
            if not record.start_duration or not record.weekday_ids or not record.n_of_reservations:
                continue

            try:
                start_date = fields.Date.from_string(record.start_duration)
                weekdays = record.weekday_ids.mapped('name')
                weekday_map = {day: i for i, day in enumerate(
                    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])}

                selected_weekdays = sorted([weekday_map[day] for day in weekdays])
                reservations_left = record.n_of_reservations
                current_date = start_date

                while reservations_left > 0:
                    if current_date.weekday() in selected_weekdays:
                        reservations_left -= 1
                    current_date += timedelta(days=1)

                record.end_duration = current_date - timedelta(days=1)
            except Exception as e:
                _logger.error("Error computing end_duration: %s", e)
                record.end_duration = False

    @api.depends('start_duration', 'end_duration')
    def _compute_duration(self):
        for record in self:
            if record.start_duration and record.end_duration:
                delta = (record.end_duration - record.start_duration).days
                record.duration = int(delta) + 1 if delta >= 0 else 0
            else:
                record.duration = 0

    @api.constrains('n_of_reservations')
    def _check_n_of_reservations(self):
        for record in self:
            if record.n_of_reservations <= 0:
                raise ValidationError("The number of reservations cannot be 0 or negative.")

    @api.constrains('start_time', 'end_time')
    def _check_start_time_end_time(self):
        for record in self:
            if record.start_time <= 0:
                raise ValidationError("Enter a correct hour format for start time, EX: 13.50 (1:50 PM)")
            if record.end_time <= 0:
                raise ValidationError("Enter a correct hour format for end time, EX: 16.50 (4:50 PM)")

    def action_confirm(self):
        self.ensure_one()
        old_admission = self.admission_id

        # 1. إنشاء قبول جديد (نسخة من القديم مع التعديلات الجديدة)
        # ملاحظة: نستخدم start_date/end_date في الـ admission لتمثيل الوقت (Float)
        new_admission_vals = {
            'student_id': self.client_id.id,
            'sport_id': old_admission.sport_id.id,
            'level_id': old_admission.level_id.id,
            'trainer_id': self.trainer_id.id,
            'nurse_specialty_id': self.nurse_specialty_id.id,
            'package_id': self.package_id.id,
            'weekday_ids': [(6, 0, self.weekday_ids.ids)],
            'start_duration': self.start_duration,
            'start_date': self.start_time,  # تمرير وقت البدء
            'end_date': self.end_time,  # تمرير وقت الانتهاء
            'n_of_reservations': self.n_of_reservations,
            'is_vip': self.is_vip,
            'city_distance_id': old_admission.city_distance_id.id,
            'driver_id': old_admission.driver_id.id,
            'state': 'new',
        }

        # إنشاء القبول الجديد
        new_admission = self.env['student.admission'].create(new_admission_vals)

        # 2. التسجيل التلقائي للقبول الجديد (إنشاء الحجوزات)
        try:
            new_admission.action_enroll()
        except Exception as e:
            # في حال حدث خطأ أثناء إنشاء الحجوزات، نحذف القبول الجديد ونرجع الخطأ
            new_admission.unlink()
            raise UserError(_("Error during enrollment: %s") % str(e))

        # 3. إلغاء القبول القديم (حتى لا يتضارب مع الجديد)
        old_admission.write({'state': 'cancel'})

        # 4. إنشاء الفاتورة للقبول الجديد
        self.action_create_invoice(new_admission)

        # 5. فتح نموذج القبول الجديد
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'student.admission',
            'res_id': new_admission.id,
            'view_mode': 'form',
            'target': 'current',
            'name': _('New Admission'),
        }

    def action_create_invoice(self, admission_id):
        """دالة مساعدة لإنشاء الفاتورة للقبول المحدد"""
        if not admission_id:
            return

        sale_journals = self.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)

        # حساب الكمية بالشهور (تقريبي)
        days_per_month = 31
        invoice_line_quantity = 1
        if self.duration > 0:
            invoice_line_quantity = (self.duration + days_per_month - 1) // days_per_month

        move_vals = {
            'invoice_origin': admission_id.name or '',
            'move_type': 'out_invoice',
            'ref': admission_id.name or '',
            'journal_id': sale_journals.id if sale_journals else False,
            'partner_id': admission_id.student_id.id,
            'invoice_date': fields.date.today(),
            'currency_id': admission_id.student_id.currency_id.id or self.env.user.currency_id.id,
            'company_id': self.env.user.company_id.id,
            'invoice_line_ids': [],
            # نستخدم حقل ملاحظات لتخزين الرابط إذا لم يكن الحقل موجوداً
            'narration': f'Renewed from admission {self.admission_id.name}'
        }

        if admission_id.sport_id:
            move_vals['invoice_line_ids'] = [(0, 0, {
                'product_id': admission_id.sport_id.id,
                'name': f"{admission_id.sport_id.display_name} - Renewal",
                'product_uom_id': admission_id.sport_id.uom_id.id,
                'price_unit': admission_id.sport_id.lst_price,
                'quantity': invoice_line_quantity,
            })]

        self.env['account.move'].create(move_vals)

        @api.depends('package_id')
        def _compute_package_line_id_domain_wizard(self):
            for rec in self:
                rec.package_line_id_domain = rec.package_id.package_line_ids.ids