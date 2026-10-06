# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.http import request
from datetime import datetime, timedelta, timezone
import requests
from urllib.parse import urlencode, urljoin
import random, string
from .sallaAPI import SallaApi
import psycopg2

from logging import getLogger
_logger = getLogger(__name__)

auth_url = "https://accounts.salla.sa/oauth2/auth"
token_url = "https://accounts.salla.sa/oauth2/token"
webkul_callback_url = "https://salla-connector.webkul.in/salla"

# Store statuses that should not be re-polled by the webhook-fallback cron.
SALLA_TERMINAL_STORE_STATUSES = (
    'completed',
    'canceled',
    'cancelled',
    'delivered',
)
# Skip mappings created less than this many hours ago (uses create_date).
SALLA_STALLED_ORDER_MIN_AGE_HOURS = 2
# Hard cap per cron run to protect Salla API / Odoo load.
SALLA_STALLED_ORDER_RESYNC_LIMIT = 200
# Advisory lock class for Salla order import/resync (channel id is the 2nd key).
SALLA_ORDER_IMPORT_LOCK_CLASS = 714001
# Webhook fallback sweep: every run re-checks the orders created in the last days (status and
# total against Odoo). Salla's order list does not follow the update sort: a status change of an
# order older than the last ~600 created was never seen, and its invoice waited for the daily
# check. 14 days (the daily check's range) are about 140 pages of the list per run.
SALLA_SWEEP_DAYS = 14
SALLA_SWEEP_MAX_PAGES = 300
# A never imported order is the order import's job: the sweep only retries the recent ones.
SALLA_SWEEP_NEW_ORDER_DAYS = 2
SALLA_UPDATED_SWEEP_PER_PAGE = 30
# Orders re-imported by ID per import.operation call (keeps ApiTransaction paging sane).
SALLA_ID_IMPORT_CHUNK = 10


class MultiChannelSale(models.Model):
    _inherit = 'multi.channel.sale'

    salla_client_id = fields.Char(string='Client id')
    salla_client_secret = fields.Char(string='Secret key')
    salla_redirect_url = fields.Char(
        string='Callback-Url', default=lambda self: self.get_redirect_url())
    refresh_token = fields.Char(string='Refresh Toekn')
    access_token = fields.Char(string='Access Toekn')
    salla_token_expiry = fields.Datetime()
    salla_verification_key = fields.Char(string="Verification Key", copy=False, default=lambda self: self.get_verification_key())
    salla_store_name = fields.Char('Store Name')
    salla_store_id = fields.Char('Store ID')
    salla_zero_tax_id = fields.Many2one(
        'account.tax', string='Tax for Salla lines without tax',
        domain="[('type_tax_use', '=', 'sale'), ('amount', '=', 0), ('company_id', '=', company_id)]",
        help='Applied to every Salla order line that arrives without a tax, for example exports '
             'outside Saudi Arabia. ZATCA e-invoicing refuses invoice lines without any tax, so '
             'pick the 0%% tax the accountant uses for such sales (e.g. "0%% EX").',
    )
    import_under_review_order_cron = fields.Boolean(
        string='Resync Stalled Orders',
        help='Fallback cron: every 2 hours, re-import non-invoiced Salla orders whose store '
             'status is not terminal (completed/canceled/delivered), by store order ID. '
             'Skips mappings created less than 2 hours ago, rotates by last resync time, '
             'and caps at 200 orders per run. Use when update webhooks miss status changes.',
    )

    def get_verification_key(self): # Generate 16 characters random string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    def get_redirect_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return  urljoin(base_url, 'salla/authenticate')
    
    def salla_available_configs(self):
        return {
            'to_show': [
                'connector_status',
                'webhook_available',
                'create_order_webhook',
                'update_order_webhook',
                'cron_available',
                'import_order_cron',
                'order_created_after',
                'import_under_review_order_cron',
                'import_category_cron',
                'import_product_cron',
                'product_created_after',
                'product_updated_after',
                'sync_order_invoice',
                'sync_order_shipment',
                'sync_order_cancel',
            ],
            'readonly': [
                'import_partner_cron',
                'partner_created_after',
                'partner_updated_after',
            ],
        }
        
    @api.constrains('salla_verification_key')
    def validate_vefication_key(self):
        key = self.salla_verification_key
        if len(key) < 8:
            raise UserError('The verification key should be minimum 8 characters long')
        channel = self.search([('channel','=','salla'),('salla_verification_key','=',key)])
        if len(channel) > 1:
            channel = channel - self
            raise UserError(f'The verification key [ {key} ] is already exists in other channel [ID: {channel.id}]')


    @api.model_create_multi
    def create(self, vals_list):
        records = super(MultiChannelSale, self).create(vals_list)
        if any(vals.get('import_under_review_order_cron') for vals in vals_list):
            self.set_channel_cron(
                'odoo_salla_integration.cron_resync_salla_under_review_orders',
                True,
            )
        return records

    def write(self, vals):
        for record in self:
            if record.channel == "salla" and (vals.get('salla_client_id') or vals.get('salla_client_secret')):
                vals.update({'refresh_token': False})
                # self.write({'refresh_token': False})
        res = super(MultiChannelSale, self).write(vals)
        if 'import_under_review_order_cron' in vals:
            enabled = self.env['multi.channel.sale'].search_count([
                ('channel', '=', 'salla'),
                ('import_under_review_order_cron', '=', True),
            ])
            self.set_channel_cron(
                'odoo_salla_integration.cron_resync_salla_under_review_orders',
                bool(enabled),
            )
        return res

    def get_core_feature_compatible_channels(self):
        channels = super(MultiChannelSale,
                         self).get_core_feature_compatible_channels()
        channels.append('salla')
        return channels

    def get_channel(self):
        channels = super(MultiChannelSale, self).get_channel()
        channels.append(('salla', 'Salla'))
        return channels

    @api.model
    def get_info_urls(self):
        urls = super(MultiChannelSale,self).get_info_urls()
        urls.update(
            salla = {
                'blog' : 'https://webkul.com/blog/user-guide-for-salla-odoo-connector/',
                'store': 'https://store.webkul.com/salla-odoo-connector.html',
            },
        )
        return urls

    def get_sallaApi(self, **kw):
        with SallaApi(self.salla_client_id, self.salla_client_secret, self.access_token, self.refresh_token, channel=self, **kw) as api:
            return api
        
    def get_store_info(self,access_token): 
        api = self.get_sallaApi()
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + str(access_token)
        }
        endpoint = "https://api.salla.dev/admin/v2/store/info"
        res = api.salla_response(endpoint,headers = headers)
        if res.get('status') in [200, 201]:
            return res.get('data',{}).get('name')
        

    def create_salla_connection(self, kwargs):
        code = kwargs['code']
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = urlencode({
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.salla_client_id,
            'client_secret': self.salla_client_secret,
        })
        response = requests.post(token_url, data, headers=headers)
        if response.status_code in [200, 201]:
            res = response.json()
            refresh_token = res.get('refresh_token', '')
            access_token = res.get('access_token', '')
            return self.write({
                'state': 'validate',
                'refresh_token': refresh_token,
                'access_token': access_token,
                'salla_store_name': self.get_store_info(access_token),
                'salla_token_expiry': datetime.now(),
            })
        else:
            _logger.error(
                'Authentication failed, please verify the added keys in the channel')
            _logger.info(response.content)
        return False

    def get_user_info(self):  # Call the api to check the tokens: valid or not
        api = self.get_sallaApi()
        endpoint = "https://api.salla.dev/admin/v2/oauth2/user/info"
        res = api.salla_response(endpoint)
        if res:
            return True
        return False

    def connect_salla(self):
        return self.getAccessToken()

    def import_salla(self, object, **kw): # if refresh token expired, channel state will be error
        if not kw.get('salla_token_checked'):
            # kw travels from page to page inside ApiTransaction: check once per run.
            self.with_context(operation=True).getAccessToken()
            kw['salla_token_checked'] = True
        with SallaApi(self.salla_client_id, self.salla_client_secret, self.access_token, self.refresh_token, channel=self, **kw) as api:
            if object == 'res.partner':
                data_list, kw = api.get_partners(**kw)
            elif object == 'sale.order':
                data_list, kw = api.get_orders(**kw)
            elif object == "product.template":
                data_list, kw = api.get_products(**kw)
            elif object == "product.category":
                data_list, kw = api.get_categories(**kw)
                # Salla returns a flattened category tree per request; stop
                # re-fetching when the API has no next page.
                if not kw.get('next_url'):
                    kw['page_size'] = (len(data_list) if data_list else 0) + 1
            elif object == "delivery.carrier":
                data_list, kw = api.get_shippings(**kw)
            else:
                data_list = []
                kw = {'message': 'Selected Channel does not allow this.'}
            # Customer imports manage page_size themselves because they traverse
            # multiple date windows to stay below Salla's 10,000-result cap.
            if object in ['product.template', 'sale.order']:
                kw.update({'page_size': kw.get('page_size') +
                           1 if not kw.get('next_url') else kw.get('page_size')})
            if object == 'sale.order':
                self._salla_maybe_advance_import_order_date(data_list, kw)
            return data_list, kw

    def _salla_parse_order_date(self, date_order):
        """Parse Salla order date_order payload into a naive datetime."""
        if not date_order:
            return False
        if isinstance(date_order, datetime):
            return date_order.replace(tzinfo=None) if date_order.tzinfo else date_order
        raw = str(date_order)
        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                continue
        _logger.warning('Salla: could not parse order date_order=%r', date_order)
        return False

    def _salla_maybe_advance_import_order_date(self, data_list, kw):
        """Advance import_order_date only for date-based cron imports, and only forward.

        By-ID imports (stalled resync / manual ID) must not rewrite the cursor — that
        caused concurrent updates on multi.channel.sale and could rewind the date.
        """
        if kw.get('import_order_date_updated'):
            return
        if not kw.get('from_cron'):
            return
        # Only the date-window order cron owns this cursor.
        if kw.get('filter_type') != 'date':
            return
        if not data_list:
            return
        new_date = self._salla_parse_order_date(data_list[0].get('date_order'))
        if not new_date:
            return
        # Monotonic SQL update reduces ORM flush races with other channel writers.
        self.env.cr.execute(
            """
            UPDATE multi_channel_sale
               SET import_order_date = %s,
                   write_date = (now() AT TIME ZONE 'UTC'),
                   write_uid = %s
             WHERE id = %s
               AND (import_order_date IS NULL OR import_order_date < %s)
            """,
            (new_date, self.env.uid, self.id, new_date),
        )
        self.invalidate_recordset(['import_order_date', 'write_date', 'write_uid'])
        kw['import_order_date_updated'] = True

    def _salla_try_acquire_order_import_lock(self):
        """Non-blocking per-channel session lock so order jobs do not overlap.

        Session locks survive mid-job ``cr.commit()`` calls inside ApiTransaction.
        Caller must always release with ``_salla_release_order_import_lock``.
        """
        self.ensure_one()
        self.env.cr.execute(
            "SELECT pg_try_advisory_lock(%s, %s)",
            (SALLA_ORDER_IMPORT_LOCK_CLASS, self.id),
        )
        return bool(self.env.cr.fetchone()[0])

    def _salla_release_order_import_lock(self):
        """Release the session advisory lock acquired for this channel.

        When the job failed, its transaction is aborted and no statement runs before a rollback:
        without it the unlock fails, the lock stays on the pooled connection and every later order
        import of the channel (sweep, backfill, audit) is skipped as "busy"."""
        self.ensure_one()
        query, params = "SELECT pg_advisory_unlock(%s, %s)", (SALLA_ORDER_IMPORT_LOCK_CLASS, self.id)
        try:
            self.env.cr.execute(query, params)
        except psycopg2.errors.InFailedSqlTransaction:
            self.env.cr.rollback()
            self.env.cr.execute(query, params)
        return bool(self.env.cr.fetchone()[0])

    def export_salla(self, record, **kw): # if token expired, channel will be in error
        self.with_context(operation=True).getAccessToken()
        with SallaApi(self.salla_client_id, self.salla_client_secret, self.access_token, self.refresh_token, channel=self, **kw) as api:
            if record._name == 'product.category':
                return api.post_category(record, record.id)
            elif record._name == 'product.template':
                res, object = api.post_product(record)
                return res, object
            else:
                raise NotImplementedError

    def update_salla(self, record, get_remote_id):
        try:
            self.with_context(operation=True).getAccessToken()
            channel = self.with_context(operation='update')
            with SallaApi(self.salla_client_id, self.salla_client_secret, self.access_token, self.refresh_token, channel=channel) as api:
                data_list = [False, {}]
                remote_id = get_remote_id(record)
                if record._name == 'product.template':
                    data_list = api.update_salla_product(record, remote_id)
                elif record._name == "product.category":
                    data_list = api.update_category(
                        record, record.id, remote_id)
        except Exception as e:
            _logger.error('Error: occurred %r', e, exc_info=True)
        return data_list

    def sync_quantity_salla(self, mapping, qty):
        with SallaApi(self.salla_client_id, self.salla_client_secret, self.access_token, self.refresh_token, channel=self) as api:
            if mapping.store_product_id == mapping.store_variant_id or mapping.store_variant_id == "No Variants":
                typ = "product"
                product_id = mapping.store_product_id
            else:
                typ = "variant"
                product_id = mapping.store_variant_id
            return api.set_quantity(product_id, qty, typ)

    # ++++++++++++++++++++++CORE METHODS++++++++++++++++++++++++
    def salla_post_do_transfer(self, stock_picking, mapping_ids, result):
        self.update_salla_order_status('delivered', mapping_ids.store_order_id)

    def salla_post_confirm_paid(self, invoice, mapping_ids, result):
        self.update_salla_order_status('completed', mapping_ids.store_order_id)

    def salla_post_cancel_order(self, sale_order, mapping_ids, result):
        self.update_salla_order_status('canceled', mapping_ids.store_order_id)

    def update_salla_order_status(self, slug, remote_id):
        "under_review, payment_pending , canceled , delivered, completed , shipped , restored , in_progress, delivering, restoring"
        try:
            order_status = self.order_state_ids.filtered(
                lambda order_state_id: order_state_id.channel_state == slug
            )
            if order_status:
                api = self.get_sallaApi()
                endpoint = api.import_url + f"orders/{remote_id}/status"
                data = {'slug': slug}
                if slug == 'completed' and order_status[0].odoo_set_invoice_state != 'paid':
                    _logger.error(
                        'Error: set invoice state in order state mapping for \'completed\' channel order state should be paid in channel configuration')
                else:
                    response = api.salla_response(
                        endpoint, method="POST", data=data)
            else:
                _logger.warning(
                    'Error: Can not update order state, please create order state  mapping for [{}] status in channel configuration'.format(slug))
        except Exception as e:
            _logger.error(
                'Exception occurred during realtime status sync to: {}'.format(slug), exc_info=True)


# ==================== Import Crons ==============================

    def salla_import_order_cron(self):  # Cron implemented
        _logger.info("+++++++++++Import Order Cron Started++++++++++++")
        if not self._salla_try_acquire_order_import_lock():
            _logger.info(
                'Salla order import cron skipped for channel %s: another order import holds the lock',
                self.id,
            )
            return True
        run_started = fields.Datetime.now()
        try:
            kw = dict(object="sale.order", from_cron=True)
            if self.import_order_date:
                kw.update(
                    filter_type='date',
                    # Salla filters by creation DATE only (yyyy-mm-dd). Overlap one
                    # day so a failed page or a boundary order is fetched again.
                    salla_from_date=(self.import_order_date - timedelta(days=1)).date(),
                    salla_to_date=(run_started + timedelta(days=1)).date(),
                )
            self.env["import.operation"].create({
                "channel_id": self.id,
            }).import_with_filter(**kw)
            if not self.import_order_date:
                # First full import: start the date window from this run.
                self.write({'import_order_date': run_started})
        finally:
            self._salla_release_order_import_lock()
        return True

    @api.model
    def cron_salla_sweep_updated_orders(self):
        """Global cron entry: re-import recently updated Salla orders (webhook fallback)."""
        channels = self.search([
            ('channel', '=', 'salla'),
            ('state', '=', 'validate'),
            ('active', '=', True),
        ])
        for channel in channels:
            try:
                channel.salla_sweep_updated_orders()
                self.env.cr.commit()
            except Exception as e:
                _logger.exception(
                    'Salla updated-orders sweep failed for channel %s: %s', channel.id, e,
                )
                self.env.cr.rollback()
        return True

    def salla_sweep_updated_orders(self):
        """Scan the Salla orders created in the last SALLA_SWEEP_DAYS days and re-import the ones
        whose status differs from the stored mapping, whose total differs from the Odoo order not
        invoiced yet (a coupon added or removed in Salla after the import), or, when recent, that
        were never imported."""
        self.ensure_one()
        if not self._salla_try_acquire_order_import_lock():
            _logger.info(
                'Salla updated-orders sweep skipped for channel %s: another order import holds the lock',
                self.id,
            )
            return True
        try:
            self.with_context(operation=True).getAccessToken()
            api = self.get_sallaApi()
            Mapping = self.env['channel.order.mappings']
            store_ids, changed, totals = [], {}, {}
            today = fields.Date.context_today(self)
            new_since = str(today - timedelta(days=SALLA_SWEEP_NEW_ORDER_DAYS))
            for page in range(1, SALLA_SWEEP_MAX_PAGES + 1):
                res = api.salla_response(api.import_url + 'orders', params={
                    'from_date': str(today - timedelta(days=SALLA_SWEEP_DAYS)),
                    'to_date': str(today + timedelta(days=1)),
                    'sort_by': 'created_at-desc',
                    'per_page': SALLA_UPDATED_SWEEP_PER_PAGE,
                    'page': page,
                })
                rows = (res or {}).get('data') or []
                if not rows:
                    break
                mappings = {mapping.store_order_id: mapping for mapping in Mapping.search([
                    ('channel_id', '=', self.id),
                    ('store_order_id', 'in', [str(row.get('id')) for row in rows]),
                ])}
                for row in rows:
                    store_id = str(row.get('id'))
                    slug = (row.get('status') or {}).get('slug') or ''
                    mapping = mappings.get(store_id)
                    total = row.get('total') or {}
                    ref = str(row.get('reference_id') or '')
                    if ref and total.get('amount') is not None:
                        totals[ref] = (float(total['amount']), total.get('currency') or '')
                    if not mapping:
                        created = ((row.get('date') or {}).get('date') or '')[:10]
                        if not created or created >= new_since:
                            store_ids.append(store_id)
                    elif (mapping.store_order_status or '') != slug:
                        store_ids.append(store_id)
                    elif self._salla_order_total_changed(mapping.order_name, totals.get(ref)):
                        store_ids.append(store_id)
                        changed[store_id] = ref
                links = ((res or {}).get('pagination') or {}).get('links') or {}
                if not links.get('next'):
                    break
            _logger.info('Salla sweep: channel %s, %s order(s) to (re)import, %s of them for their total',
                         self.id, len(store_ids), len(changed))
            # the import invoices an order on Salla's total read here (_salla_order_target)
            ImportOp = self.env['import.operation'].with_context(salla_order_totals=totals)
            for start in range(0, len(store_ids), SALLA_ID_IMPORT_CHUNK):
                ImportOp.create({'channel_id': self.id}).import_with_filter(
                    object='sale.order',
                    filter_type='id',
                    object_id=','.join(store_ids[start:start + SALLA_ID_IMPORT_CHUNK]),
                    from_cron=True,
                    force_evaluate_feed=True,
                )
                self.env.cr.commit()
            # a confirmed order is not rewritten by the import: it is brought to Salla's total now,
            # before its invoice (a draft one was rewritten and already matches)
            for store_id, ref in changed.items():
                order = Mapping.search([('channel_id', '=', self.id), ('store_order_id', '=', store_id)], limit=1).order_name
                if not self._salla_order_total_changed(order, totals.get(ref)):
                    continue
                try:
                    with self.env.cr.savepoint():
                        self._salla_bring_order_to_total(order, totals[ref][0])
                except Exception as e:  # the daily check corrects it later
                    _logger.warning("Salla sweep: order %s not brought to Salla's total: %s", ref, e)
            if changed:
                self.env.cr.commit()
        finally:
            self._salla_release_order_import_lock()
        return True

    @api.model
    def cron_resync_salla_under_review_orders(self):
        """Global cron entry: resync stalled (non-terminal) Salla order mappings."""
        channels = self.search([
            ('channel', '=', 'salla'),
            ('state', '=', 'validate'),
            ('active', '=', True),
            ('import_under_review_order_cron', '=', True),
        ])
        for channel in channels:
            try:
                channel.salla_resync_under_review_orders()
                self._cr.commit()
            except Exception as e:
                _logger.exception(
                    'Salla stalled-order resync cron failed for channel %s: %s',
                    channel.id, e,
                )
                self._cr.rollback()
        return True

    def _salla_ensure_in_progress_order_state(self):
        """Ensure in_progress is mapped; data.xml noupdate won't update existing channels."""
        self.ensure_one()
        if self.channel != 'salla':
            return
        OrderState = self.env['channel.order.states']
        exists = OrderState.search_count([
            ('channel_id', '=', self.id),
            ('channel_state', '=', 'in_progress'),
        ])
        if not exists:
            OrderState.create({
                'channel_id': self.id,
                'channel_state': 'in_progress',
                'odoo_order_state': 'sale',
            })
            _logger.info(
                'Salla channel %s: added missing in_progress order state mapping',
                self.id,
            )

    def _salla_ensure_category_feeds(self, store_categ_id):
        """Fetch an unknown Salla category (with its tree) and create the missing
        category feeds, so a product or order is not rejected because a category
        was created in Salla after the last category import."""
        self.ensure_one()
        CategoryFeed = self.env['category.feed']
        created = CategoryFeed
        try:
            api = self.get_sallaApi()
            categories, _kw = api.get_categories(filter_type='id', object_id=str(store_categ_id))
        except Exception as e:
            _logger.warning('Salla: could not fetch category %s on demand: %s', store_categ_id, e)
            return created
        for vals in categories or []:
            store_id = str(vals.get('store_id') or '')
            if not store_id:
                continue
            if not CategoryFeed.search([('channel_id', '=', self.id), ('store_id', '=', store_id)], limit=1):
                created |= CategoryFeed.create(vals)
        if created:
            _logger.info('Salla: category %s fetched on demand, %s feed(s) created', store_categ_id, len(created))
        return created

    def _salla_stalled_order_mappings(self):
        """Non-invoiced, non-cancelled mappings stuck on non-terminal Salla statuses.

        Age uses create_date (not write_date). Ordering uses salla_last_resync_at so
        never-tried / least-recently-tried mappings rotate through the backlog instead
        of the same oldest create_date rows every run.
        """
        self.ensure_one()
        min_create_date = fields.Datetime.now() - timedelta(
            hours=SALLA_STALLED_ORDER_MIN_AGE_HOURS,
        )
        return self.env['channel.order.mappings'].search([
            ('channel_id', '=', self.id),
            ('store_order_id', '!=', False),
            ('is_invoiced', '=', False),
            ('order_name', '!=', False),
            ('order_name.state', '!=', 'cancel'),
            ('store_order_status', 'not in', list(SALLA_TERMINAL_STORE_STATUSES)),
            ('create_date', '<=', min_create_date),
        ], order='salla_last_resync_at asc nulls first, create_date asc',
           limit=SALLA_STALLED_ORDER_RESYNC_LIMIT)

    def salla_resync_under_review_orders(self):
        """Re-import stalled order mappings by store order ID (webhook fallback)."""
        self.ensure_one()
        if not self._salla_try_acquire_order_import_lock():
            _logger.info(
                'Salla stalled-order resync skipped for channel %s: another order import holds the lock',
                self.id,
            )
            return True
        try:
            self._salla_ensure_in_progress_order_state()
            _logger.info(
                "+++++++++++Salla Stalled Order Resync Started (channel %s)++++++++++++",
                self.id,
            )
            mappings = self._salla_stalled_order_mappings()
            if not mappings:
                _logger.info(
                    'Salla stalled-order resync: nothing to process for channel %s',
                    self.id,
                )
                return True

            _logger.info(
                'Salla stalled-order resync: channel %s will process %s order(s)',
                self.id, len(mappings),
            )
            ImportOp = self.env['import.operation']
            for mapping in mappings:
                store_id = mapping.store_order_id
                if not store_id:
                    continue
                try:
                    ImportOp.create({
                        'channel_id': self.id,
                    }).import_with_filter(
                        object='sale.order',
                        filter_type='id',
                        object_id=store_id,
                        from_cron=True,
                        force_evaluate_feed=True,
                    )
                    # Stamp after attempt so this mapping rotates to the back of the queue.
                    mapping.salla_last_resync_at = fields.Datetime.now()
                    self._cr.commit()
                except Exception as e:
                    _logger.exception(
                        'Salla stalled-order resync failed for channel %s '
                        'store order %s: %s',
                        self.id, store_id, e,
                    )
                    self._cr.rollback()
                    try:
                        # Still rotate failed rows so they do not block the backlog.
                        mapping.invalidate_recordset()
                        if mapping.exists():
                            mapping.salla_last_resync_at = fields.Datetime.now()
                            self._cr.commit()
                    except Exception:
                        self._cr.rollback()
            return True
        finally:
            self._salla_release_order_import_lock()

    def salla_import_category_cron(self):  # Cron implemented
        _logger.info("+++++++++++Import Category Cron Started++++++++++++")
        kw = dict(
            object="product.category",
            from_cron=True,
        )
        self.env["import.operation"].create({
            "channel_id": self.id,
        }).import_with_filter(**kw)

    def salla_import_product_cron(self):
        _logger.info("+++++++++++Import Product Cron Started++++++++++++")
        kw = dict(
            object="product.template",
            from_cron=True,
        )
        self.env["import.operation"].create({
            "channel_id": self.id,
        }).import_with_filter(**kw)

    def salla_import_partner_cron(self):
        _logger.info(
            "+++++ Import Partner Cron is not supported in Salla Connector ++++++")
        
    def _log_salla_proxy_call(self, action, url, params, response=None, error=None):
        """Log Webkul proxy handshake without raising."""
        self.ensure_one()
        safe_params = dict(params or {})
        _logger.info(
            "Salla %s: channel_id=%s state=%s store_id=%r verification_key=%r "
            "base_url=%r proxy=%s params=%s",
            action,
            self.id,
            self.state,
            self.salla_store_id,
            self.salla_verification_key,
            self.get_base_url(),
            url,
            safe_params,
        )
        if error is not None:
            _logger.exception("Salla %s: request failed: %s", action, error)
            return
        if response is None:
            return
        body = response.text or ''
        if len(body) > 2000:
            body = body[:2000] + '...<truncated>'
        _logger.info(
            "Salla %s: status=%s reason=%s content_type=%s body=%s",
            action,
            response.status_code,
            response.reason,
            response.headers.get('Content-Type'),
            body,
        )
        try:
            payload = response.json()
        except ValueError:
            _logger.warning("Salla %s: response is not JSON", action)
            return
        _logger.info(
            "Salla %s: json_keys=%s status_code=%s message=%s message_text=%s "
            "has_url=%s has_access_token=%s",
            action,
            list(payload.keys()) if isinstance(payload, dict) else type(payload),
            payload.get('status_code') if isinstance(payload, dict) else None,
            payload.get('message') if isinstance(payload, dict) else None,
            payload.get('message_text') if isinstance(payload, dict) else None,
            bool(isinstance(payload, dict) and (payload.get('data') or {}).get('url')),
            bool(isinstance(payload, dict) and (payload.get('data') or {}).get('access_token')),
        )

    def connect_to_salla(self):
        self.ensure_one()
        data = {
            'base_url': self.get_base_url(),
            'salla_verification_key': self.salla_verification_key,
            'salla_store_id': self.salla_store_id or '',
            'instance_id': self.id,
        }
        try:
            res = requests.get(webkul_callback_url, params=data, timeout=30)
        except Exception as e:
            self._log_salla_proxy_call('connect_to_salla', webkul_callback_url, data, error=e)
            return self.display_message(
                "<span class='text-danger'>Authentication failed: "
                f"could not reach Webkul proxy ({e})</span>"
            )
        self._log_salla_proxy_call('connect_to_salla', res.url, data, response=res)
        if res.status_code == 200:
            payload = res.json() if res.content else {}
            oauth_url = (payload.get('data') or {}).get('url')
            if oauth_url:
                return {
                    'type': 'ir.actions.act_url',
                    'target': 'self',
                    'url': oauth_url,
                }
            _logger.error("Salla connect_to_salla: HTTP 200 but no data.url in payload")
        return self.display_message(
            "<span class='text-danger'>Authentication failed, Please verify the added "
            f"Client Keys and Redirect URI "
            f"(proxy HTTP {res.status_code}; see Odoo log for body)</span>"
        )

    def getAccessToken(self):
        self.ensure_one()
        status, message = True, ""
        data = {
            'salla_verification_key': self.salla_verification_key,
            'salla_store_id': self.salla_store_id or '',
            'base_url': self.get_base_url(),
            'for_refresh_token': True,
        }
        try:
            response = requests.get(webkul_callback_url, params=data, timeout=30)
            self._log_salla_proxy_call('getAccessToken', response.url, data, response=response)
            response.raise_for_status()
            result = response.json()
            if result.get('status_code') == 200:
                token_data = result.get('data') or {}
                access_token = token_data.get('access_token', '')
                store_name = token_data.get('store_name', '')
                message = (
                    f"<p class='text-success'>Connection refreshed successfully "
                    f"with {store_name}</p>"
                )
                # Write the channel row only when something changed: every write
                # locks the row and makes concurrent imports fail with
                # "could not serialize access due to concurrent update".
                vals = {}
                if self.state != 'validate':
                    vals['state'] = 'validate'
                if (token_data.get('refresh_token') or '') != (self.refresh_token or ''):
                    vals['refresh_token'] = token_data.get('refresh_token', '')
                if (access_token or '') != (self.access_token or ''):
                    vals['access_token'] = access_token
                if vals:
                    self.write(vals)
            else:
                status = False
                message += result.get('message_text', "") or (
                    f"Proxy rejected refresh (status_code={result.get('status_code')})"
                )
        except Exception as e:
            self._log_salla_proxy_call(
                'getAccessToken', webkul_callback_url, data, error=e,
            )
            return False, f"Error : {e}"
        return status, message
    
    def get_base_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('web.base.url')
