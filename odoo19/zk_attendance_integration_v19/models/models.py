# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta, time
import logging

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    zk_emp_id = fields.Char(string='Attendance Machine No.')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('zk_emp_id', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)


class zk_attendance_tmp(models.Model):
    _name = 'hr.attendance.zk.temp'

    machine_id = fields.Many2one('hr.attendance.zk.machine', string="Attendance Machine", required=True)
    user_number = fields.Char(string="Machine User Id", index=True)
    user = fields.Many2one('hr.employee', compute='_compute_user', store=True, index=True)
    date = fields.Datetime(string="Date", index=True)
    local_date = fields.Datetime(string='Local Date', compute='_compute_local_date', store=True)
    date_temp = fields.Date(string="Date Temp", index=True, compute="_compute_date", store=True)
    inoutmode = fields.Char(string="In/Out Mode")
    logged = fields.Boolean(string="Logged", default=False, index=True)
    reversed = fields.Boolean(string='Reversed', default=False)

    @api.model
    def sudo_create_log(self, args):
        cr = self._cr
        cr.execute("""
            SELECT * FROM hr_attendance_zk_temp 
            WHERE date=%s AND inoutmode=%s AND user_number=%s AND machine_id=%s
        """, (args['date'], args['inoutmode'], args['user_number'], args['machine_id']))
        if not cr.dictfetchall():
            self.sudo().create(args)
        return True

    @api.depends('user_number')
    def _compute_user(self):
        for rec in self:
            if rec.user_number:
                emp = self.env['hr.employee'].search([('zk_emp_id', '=', rec.user_number)], limit=1)
                rec.user = emp.id if emp else False
            else:
                rec.user = False

    @api.depends('date')
    def _compute_date(self):
        for rec in self:
            if rec.date:
                local_time = rec.date + timedelta(hours=2)
                rec.date_temp = local_time.date()

    @api.depends('date')
    def _compute_local_date(self):
        for rec in self:
            if rec.date:
                rec.local_date = rec.date + timedelta(hours=2)

    def _is_valid_duration(self, check_in, check_out):
        duration_hours = (check_out - check_in).total_seconds() / 3600.0
        return 0.5 <= duration_hours <= 16.0

    def _is_same_workday(self, dt1, dt2):
        local_dt1 = dt1 + timedelta(hours=2)
        local_dt2 = dt2 + timedelta(hours=2)
        workday1 = local_dt1.date()
        if local_dt1.time() < time(4, 0):
            workday1 = (local_dt1 - timedelta(days=1)).date()
        workday2 = local_dt2.date()
        if local_dt2.time() < time(4, 0):
            workday2 = (local_dt2 - timedelta(days=1)).date()
        return workday1 == workday2

    def _has_conflicting_attendance(self, emp_id, check_in):
        return self.env['hr.attendance'].search([
            ('employee_id', '=', emp_id),
            ('check_in', '>=', check_in - timedelta(minutes=5)),
            ('check_in', '<=', check_in + timedelta(minutes=5))
        ], limit=1)

    def _has_overlapping_attendance(self, emp_id, check_in, check_out=False):
        attendance_env = self.env['hr.attendance']
        if check_out:
            return attendance_env.search([
                ('employee_id', '=', emp_id),
                ('check_in', '<', check_out),
                '|',
                ('check_out', '=', False),
                ('check_out', '>', check_in),
            ], limit=1)
        return attendance_env.search([
            ('employee_id', '=', emp_id),
            '|',
            ('check_out', '=', False),
            ('check_out', '>', check_in),
        ], limit=1)

    def _filter_duplicates_within_30m(self, punches_sorted):
        result = []
        i = 0
        while i < len(punches_sorted):
            first = punches_sorted[i]
            result.append(first)
            j = i + 1
            while j < len(punches_sorted):
                if (punches_sorted[j].date - first.date) <= timedelta(minutes=30):
                    j += 1
                else:
                    break
            i = j
        return result

    @api.model
    def process_data(self):
        _logger.info("=" * 80)
        _logger.info("🚀 بدء معالجة بيانات الحضور بمنطق محسّن: فصل الأيام + نافذة 16 ساعة")

        stats = {
            'updated_open': 0,
            'created': 0,
            'skipped_duplicate': 0,
            'skipped_invalid': 0,
            'errors': 0
        }

        try:
            _logger.info("📋 المرحلة 1: إغلاق السجلات المفتوحة ضمن نافذة 16 ساعة...")
            thirty_days_ago = datetime.now() - timedelta(days=30)
            open_attendances = self.env['hr.attendance'].search([
                ('check_out', '=', False),
                ('check_in', '>=', thirty_days_ago)
            ], order='check_in asc')

            _logger.info(f"   وجد {len(open_attendances)} سجل مفتوح")
            for open_att in open_attendances:
                emp_zk_id = open_att.employee_id.zk_emp_id
                if not emp_zk_id:
                    continue
                window_end = open_att.check_in + timedelta(hours=16)

                potential_checkouts = self.search([
                    ('user_number', '=', emp_zk_id),
                    ('date', '>', open_att.check_in),
                    ('date', '<=', window_end),
                    ('logged', '=', False)
                ], order='date asc')

                valid_checkouts = potential_checkouts.filtered(
                    lambda p: self._is_same_workday(open_att.check_in, p.date)
                )

                if valid_checkouts:
                    checkout_time = valid_checkouts[-1].date
                    if self._is_valid_duration(open_att.check_in, checkout_time):
                        local_checkout = checkout_time + timedelta(hours=2)
                        open_att.write({
                            'check_out': checkout_time,
                            'local_check_out': local_checkout,
                            'missing_check': False,
                            'no_checkout': False,
                        })
                        valid_checkouts.write({'logged': True})
                        stats['updated_open'] += 1
                        duration = (checkout_time - open_att.check_in).total_seconds() / 3600.0
                        _logger.info(f"   ✅ إغلاق: {open_att.employee_id.name} ({duration:.1f}h)")

            if stats['updated_open'] > 0:
                self.env.cr.commit()
                _logger.info(f"   📊 تم إغلاق {stats['updated_open']} سجل")

            _logger.info("📋 المرحلة 2: معالجة البصمات بمنطق فصل الأيام + 16 ساعة...")

            today_date_val = str(datetime.now().date())
            records = self.search([
                ('logged', '=', False),
                ('date_temp', '!=', today_date_val),
                ('user', '!=', False)
            ])

            if not records:
                _logger.info("   لا توجد سجلات جديدة للمعالجة")
                _logger.info("=" * 80)
                return self._return_stats(stats)

            _logger.info(f"   وجد {len(records)} بصمة غير معالجة")

            employees = list(set(records.mapped('user_number')))

            for emp_code in employees:
                emp_obj = self.env['hr.employee'].search([('zk_emp_id', '=', emp_code)], limit=1)
                if not emp_obj:
                    continue

                emp_records_sorted = records.filtered(
                    lambda x: x.user_number == emp_code
                ).sorted(key=lambda r: r.date)

                if not emp_records_sorted:
                    continue

                filtered_punches = self._filter_duplicates_within_30m(emp_records_sorted)

                _logger.info(f"   👤 {emp_obj.name}: {len(emp_records_sorted)} بصمة → بعد التصفية {len(filtered_punches)}")

                idx = 0
                while idx < len(filtered_punches):
                    first_punch = filtered_punches[idx]
                    date_in = first_punch.date
                    local_check_in = date_in + timedelta(hours=2)

                    window_end = date_in + timedelta(hours=16)

                    window_punches = []
                    j = idx
                    while j < len(filtered_punches):
                        punch = filtered_punches[j]
                        if punch.date <= window_end and self._is_same_workday(date_in, punch.date):
                            window_punches.append(punch)
                            j += 1
                        else:
                            break

                    if self._has_conflicting_attendance(emp_obj.id, date_in):
                        _logger.info(f"       ⏭️  تخطي: سجل موجود لنقطة الدخول")
                        for p in window_punches:
                            p.write({'logged': True})
                        stats['skipped_duplicate'] += 1
                        idx = j
                        continue

                    if len(window_punches) > 1:
                        last_punch = window_punches[-1]
                        date_out = last_punch.date
                        local_check_out = date_out + timedelta(hours=2)

                        duration_valid = self._is_valid_duration(date_in, date_out)

                        try:
                            if duration_valid:
                                if self._has_overlapping_attendance(emp_obj.id, date_in, date_out):
                                    _logger.info("       ⏭️  تخطي: تداخل مع سجل حضور قائم")
                                    for p in window_punches:
                                        p.write({'logged': True})
                                    stats['skipped_duplicate'] += 1
                                    idx = j
                                    continue

                                self.env['hr.attendance'].with_context(skip_validation=True).create({
                                    'employee_id': emp_obj.id,
                                    'check_in': date_in,
                                    'check_out': date_out,
                                    'local_check_in': local_check_in,
                                    'local_check_out': local_check_out,
                                    'missing_check': False,
                                    'no_checkout': False,
                                })
                                duration_hours = (date_out - date_in).total_seconds() / 3600.0
                                _logger.info(f"       ✅ حضور كامل: {local_check_in} → {local_check_out} ({duration_hours:.1f}h)")
                            else:
                                if self._has_overlapping_attendance(emp_obj.id, date_in):
                                    _logger.info("       ⏭️  تخطي: تداخل مع سجل حضور مفتوح")
                                    for p in window_punches:
                                        p.write({'logged': True})
                                    stats['skipped_duplicate'] += 1
                                    idx = j
                                    continue

                                self.env['hr.attendance'].with_context(skip_validation=True).create({
                                    'employee_id': emp_obj.id,
                                    'check_in': date_in,
                                    'check_out': False,
                                    'local_check_in': local_check_in,
                                    'local_check_out': False,
                                    'missing_check': True,
                                    'no_checkout': True,
                                })
                                _logger.info(f"       ⚠️ مدة غير صالحة، حفظ كحضور مفتوح: {local_check_in}")

                            for p in window_punches:
                                p.write({'logged': True})

                            stats['created'] += 1
                            self.env.cr.commit()

                        except Exception as e:
                            _logger.error(f"       ❌ خطأ: {str(e)}")
                            for p in window_punches:
                                p.write({'logged': True})
                            stats['errors'] += 1

                        idx = j
                    else:
                        try:
                            if self._has_overlapping_attendance(emp_obj.id, date_in):
                                _logger.info("       ⏭️  تخطي: تداخل مع سجل حضور مفتوح")
                                for p in window_punches:
                                    p.write({'logged': True})
                                stats['skipped_duplicate'] += 1
                                idx = j
                                continue

                            self.env['hr.attendance'].with_context(skip_validation=True).create({
                                'employee_id': emp_obj.id,
                                'check_in': date_in,
                                'check_out': False,
                                'local_check_in': local_check_in,
                                'local_check_out': False,
                                'missing_check': True,
                                'no_checkout': True,
                            })
                            _logger.info(f"       ✅ حضور مفتوح (لا خروج في نفس اليوم): {local_check_in}")

                            for p in window_punches:
                                p.write({'logged': True})

                            stats['created'] += 1
                            self.env.cr.commit()

                        except Exception as e:
                            _logger.error(f"       ❌ خطأ: {str(e)}")
                            for p in window_punches:
                                p.write({'logged': True})
                            stats['errors'] += 1

                        idx = j

            machines = self.env['hr.attendance.zk.machine'].search([])
            for m in machines:
                m.last_download_log = datetime.now()

            _logger.info("=" * 80)
            return self._return_stats(stats)

        except Exception as e:
            _logger.error(f"❌ خطأ عام: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': str(e)}


class zk_attendance_machine(models.Model):
    _name = "hr.attendance.zk.machine"

    machine_number = fields.Integer(string="Machine Number", default=0, readonly=True)
    name = fields.Char(string="Name")
    ip = fields.Char(string="IP", required=True)
    port = fields.Integer(string="port", default=4370)
    sync = fields.Boolean(string="Synced", default=False)
    model = fields.Char(string="Model")
    date_sync = fields.Datetime(string="Sync Date")
    date_sync_success = fields.Datetime(string="Successful Sync Date")
    manual_upload_sync_date = fields.Datetime(string="Last Manual Upload Date")
    sync_error = fields.Text(string="Sync Error")
    last_download_log = fields.Datetime('Last Download Log')

    @api.model
    def get_machine_last_download(self, args=None):
        if args and args.get('machine_id'):
            machine = self.search([('id', '=', int(args['machine_id']))], limit=1)
            if machine and machine.last_download_log:
                return str(machine.last_download_log - timedelta(days=30))
        return str(datetime.now() - timedelta(days=30))

    @api.model
    def update_machine_last_download(self, args=None):
        if args is None:
            args = {}
        return self.do_update_machine_last_download(args.get('machine_id'), args.get('last_datetime'))

    @api.model
    def do_update_machine_last_download(self, machine_id, last_download):
        machines = self.search([])
        for rec in machines:
            rec.write({'last_download_log': last_download})
        return True

    @api.model
    def create(self, values):
        res = super().create(values)
        res.machine_number = res.id
        return res

    def process(self):
        result = self.env['hr.attendance.zk.temp'].process_data()

        if isinstance(result, dict) and 'error' in result:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'خطأ',
                    'message': f"حدث خطأ: {result['error']}",
                    'type': 'danger',
                }
            }

        msg_parts = []
        if result.get('updated_open', 0) > 0:
            msg_parts.append(f"✅ إغلاق: {result['updated_open']}")
        if result.get('created', 0) > 0:
            msg_parts.append(f"✅ جديد: {result['created']}")
        if result.get('skipped_duplicate', 0) > 0:
            msg_parts.append(f"⏭️ مُكرر: {result['skipped_duplicate']}")
        if result.get('errors', 0) > 0:
            msg_parts.append(f"❌ أخطاء: {result['errors']}")

        if msg_parts:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'نجحت المعالجة',
                    'message': "\n".join(msg_parts),
                    'type': 'success',
                }
            }

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'معلومة',
                'message': 'لا توجد سجلات للمعالجة',
                'type': 'info',
            }
        }


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    no_checkout = fields.Boolean(string="Missing Check-out", default=False)
    missing_check = fields.Boolean(string="Missing Check", default=False)
    no_check_in = fields.Boolean(string="Missing Check-in", default=False)
    local_check_in = fields.Datetime(string="Local Check In")
    local_check_out = fields.Datetime(string="Local Check Out")

    hhmm_worked = fields.Char(string="Worked (hh:mm)", compute="_compute_hhmm_worked", store=False)

    @api.depends('worked_hours')
    def _compute_hhmm_worked(self):
        for rec in self:
            hours = rec.worked_hours or 0.0
            h = int(hours)
            m = int(round((hours - h) * 60.0))
            if m == 60:
                h += 1
                m = 0
            rec.hhmm_worked = f"{h:02d}:{m:02d}"

