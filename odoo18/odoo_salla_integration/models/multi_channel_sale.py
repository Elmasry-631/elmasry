# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
import psycopg2
from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.http import request
from datetime import datetime, timedelta, timezone
import requests
from urllib.parse import urlencode, urljoin
import random, string
from odoo import sql_db
from .sallaAPI import SallaApi

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
        self.with_context(operation=True).getAccessToken()
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
        """Release the session advisory lock acquired for this channel."""
        self.ensure_one()
        self.env.cr.execute(
            "SELECT pg_advisory_unlock(%s, %s)",
            (SALLA_ORDER_IMPORT_LOCK_CLASS, self.id),
        )
        return bool(self.env.cr.fetchone()[0])

    @staticmethod
    def _salla_is_connection_loss(exc):
        """True when the DB connection was dropped mid-operation.

        Long Salla API calls keep the DB connection idle; if PostgreSQL (or a
        pooler such as PgBouncer) kills it while idle, every later query raises
        ``cursor already closed`` / ``connection already closed``. Those errors
        are fatal for the current transaction but safe to retry on a fresh
        connection.
        """
        if isinstance(exc, psycopg2.InterfaceError):
            return True
        if isinstance(exc, psycopg2.OperationalError):
            return True
        message = str(exc)
        return any(keyword in message for keyword in (
            'cursor already closed',
            'connection already closed',
            'connection was closed',
            'server closed the connection',
            'connection reset',
            'terminating connection',
        ))

    def _salla_reconnect(self):
        """Return the same recordset on a brand-new DB connection.

        Odoo cursors cannot be revived after the physical connection is dropped.
        This borrows a fresh connection from the pool, swaps it onto the
        recordset's environment and drops the dead one, so a long import or
        resync can keep going instead of aborting the whole cron.
        """
        cr = self.env.cr
        try:
            new_cr = sql_db.db_connect(cr.dbname).cursor()
        except Exception:
            _logger.exception('Salla: could not open a fresh DB connection.')
            raise
        try:
            new_env = api.Environment(new_cr, self.env.uid, self.env.context)
        except Exception:
            try:
                new_cr.close()
            except Exception:
                pass
            raise
        # The old connection is dead (or being discarded); drop it so the pool
        # can forget it instead of leaking it.
        try:
            cr.close()
        except Exception:
            _logger.exception('Salla: failed to close the old DB connection.')
        _logger.warning('Salla: reconnected to the database on a fresh connection.')
        return self.with_env(new_env)

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
        current = self
        if not current._salla_try_acquire_order_import_lock():
            _logger.info(
                'Salla order import cron skipped for channel %s: another order import holds the lock',
                self.id,
            )
            return True
        try:
            attempts = 0
            while True:
                try:
                    kw = dict(
                        object="sale.order",
                        salla_from_date=current.import_order_date,
                        salla_to_date=datetime.now(timezone.utc),
                        from_cron=True,
                    )
                    if current.import_order_date:
                        kw.update({'filter_type': 'date'})
                    current.env["import.operation"].create({
                        "channel_id": current.id,
                    }).import_with_filter(**kw)
                    break
                except Exception as e:
                    if current._salla_is_connection_loss(e) and attempts < 3:
                        attempts += 1
                        _logger.exception(
                            'Salla order import cron lost its DB connection for channel %s '
                            '(attempt %s/3); reconnecting and continuing.',
                            current.id, attempts,
                        )
                        current = current._salla_reconnect()
                        # The old session (and its advisory lock) is gone.
                        if not current._salla_try_acquire_order_import_lock():
                            _logger.warning(
                                'Salla order import cron could not re-acquire the order '
                                'import lock for channel %s after reconnecting.',
                                current.id,
                            )
                            return True
                        continue
                    raise
        finally:
            try:
                current._salla_release_order_import_lock()
            except Exception:
                _logger.exception(
                    'Salla order import cron: failed to release the order import lock '
                    'for channel %s.',
                    self.id,
                )
        return True

    @api.model
    def cron_resync_salla_under_review_orders(self):
        """Global cron entry: resync stalled (non-terminal) Salla order mappings."""
        current = self
        channel_ids = current.search([
            ('channel', '=', 'salla'),
            ('state', '=', 'validate'),
            ('active', '=', True),
            ('import_under_review_order_cron', '=', True),
        ]).ids
        for channel_id in channel_ids:
            try:
                channel = current.browse(channel_id)
                channel.salla_resync_under_review_orders()
                current.env.cr.commit()
            except Exception as e:
                _logger.exception(
                    'Salla stalled-order resync cron failed for channel %s: %s',
                    channel_id, e,
                )
                if current._salla_is_connection_loss(e):
                    current = current._salla_reconnect()
                else:
                    try:
                        current.env.cr.rollback()
                    except Exception:
                        current = current._salla_reconnect()
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
        """Re-import stalled order mappings by store order ID (webhook fallback).

        Resistant to dropped DB connections: every order commits on its own, so
        if the connection dies mid-run (idle session timeout, PgBouncer, worker
        recycle) the resync reconnects on a fresh connection and keeps going
        through the remaining orders instead of aborting the whole cron and
        forcing a full restart.
        """
        self.ensure_one()
        current = self
        if not current._salla_try_acquire_order_import_lock():
            _logger.info(
                'Salla stalled-order resync skipped for channel %s: another order import holds the lock',
                self.id,
            )
            return True
        try:
            current._salla_ensure_in_progress_order_state()
            _logger.info(
                "+++++++++++Salla Stalled Order Resync Started (channel %s)++++++++++++",
                self.id,
            )
            pending_ids = current._salla_stalled_order_mappings().ids
            if not pending_ids:
                _logger.info(
                    'Salla stalled-order resync: nothing to process for channel %s',
                    self.id,
                )
                return True

            _logger.info(
                'Salla stalled-order resync: channel %s will process %s order(s)',
                self.id, len(pending_ids),
            )
            reconnects = 0
            while pending_ids:
                mapping = current.env['channel.order.mappings'].browse(pending_ids.pop(0))
                store_id = mapping.store_order_id
                if not store_id:
                    continue
                try:
                    current.env['import.operation'].create({
                        'channel_id': current.id,
                    }).import_with_filter(
                        object='sale.order',
                        filter_type='id',
                        object_id=store_id,
                        from_cron=True,
                        force_evaluate_feed=True,
                    )
                    # Stamp after attempt so this mapping rotates to the back of the queue.
                    mapping.salla_last_resync_at = fields.Datetime.now()
                    current._cr.commit()
                except Exception as e:
                    if current._salla_is_connection_loss(e):
                        if reconnects >= 3:
                            _logger.exception(
                                'Salla stalled-order resync lost its DB connection %s '
                                'times for channel %s; giving up this run, the next cron '
                                'run will resume.',
                                reconnects, current.id,
                            )
                            break
                        reconnects += 1
                        _logger.exception(
                            'Salla stalled-order resync lost its DB connection for channel %s '
                            'store order %s; reconnecting and continuing.',
                            current.id, store_id,
                        )
                        current = current._salla_reconnect()
                        if not current._salla_try_acquire_order_import_lock():
                            _logger.warning(
                                'Salla stalled-order resync could not re-acquire the order '
                                'import lock for channel %s after reconnecting.',
                                current.id,
                            )
                            break
                        # Retry the same order on the fresh connection.
                        pending_ids.insert(0, mapping.id)
                        continue
                    _logger.exception(
                        'Salla stalled-order resync failed for channel %s '
                        'store order %s: %s',
                        current.id, store_id, e,
                    )
                    try:
                        current._cr.rollback()
                    except Exception:
                        _logger.exception(
                            'Salla stalled-order resync: rollback failed for channel %s '
                            'store order %s; reconnecting.',
                            current.id, store_id,
                        )
                        current = current._salla_reconnect()
                        continue
                    try:
                        # Still rotate failed rows so they do not block the backlog.
                        mapping.salla_last_resync_at = fields.Datetime.now()
                        current._cr.commit()
                    except Exception:
                        _logger.exception(
                            'Salla stalled-order resync: failed to rotate mapping for '
                            'channel %s store order %s.',
                            current.id, store_id,
                        )
            return True
        finally:
            try:
                current._salla_release_order_import_lock()
            except Exception:
                _logger.exception(
                    'Salla stalled-order resync: failed to release the order import '
                    'lock for channel %s.',
                    self.id,
                )

    def _salla_run_import_with_reconnect(self, **kw):
        """Run one import job, reconnecting once if the DB connection is dropped."""
        current = self
        for attempt in range(1, 4):
            try:
                current.env["import.operation"].create({
                    "channel_id": current.id,
                }).import_with_filter(**kw)
                return
            except Exception as e:
                if not current._salla_is_connection_loss(e):
                    raise
                _logger.exception(
                    'Salla import lost its DB connection for channel %s (attempt %s/3); '
                    'reconnecting and continuing.',
                    current.id, attempt,
                )
                current = current._salla_reconnect()
        return

    def salla_import_category_cron(self):  # Cron implemented
        _logger.info("+++++++++++Import Category Cron Started++++++++++++")
        self._salla_run_import_with_reconnect(
            object="product.category",
            from_cron=True,
        )

    def salla_import_product_cron(self):
        _logger.info("+++++++++++Import Product Cron Started++++++++++++")
        self._salla_run_import_with_reconnect(
            object="product.template",
            from_cron=True,
        )

    def salla_import_partner_cron(self):
        _logger.info(
            "+++++ Import Partner Cron is not supported in Salla Connector ++++++")
        
    def connect_to_salla(self):
        base_url = self.get_base_url()
        data = { 
            'base_url': base_url,
            'salla_verification_key':self.salla_verification_key,
            'salla_store_id':self.salla_store_id,
            'instance_id':self.id,
        }
        res = requests.get(webkul_callback_url, params=data)
        if res.status_code == 200:
            data = res.json().get('data')
            return {
                    'type': 'ir.actions.act_url',
                    'target': 'self',
                    'url': data.get('url')
                    }
        return self.display_message("<span class='text-danger'>Authentication failed, Please verify the added Client Keys and Redirect URI</p>")
    
    def getAccessToken(self):
        status, message = True, ""
        data = { 
            'salla_verification_key':self.salla_verification_key,
            'salla_store_id':self.salla_store_id,
            'base_url':self.get_base_url(),
            'for_refresh_token':True,
        }
        try:
            response = requests.get(webkul_callback_url, params=data)
            response.raise_for_status()
            result = response.json()
            if result.get('status_code') == 200:
                data = result.get('data')
                access_token = data.get('access_token', '')
                store_name = data.get('store_name', '')
                message = f"<p class='text-success'>Connection refreshed successfully with {store_name}</p>"
                self.write({
                    'state': 'validate',
                    'refresh_token': data.get('refresh_token', ''),
                    'access_token': access_token,
                    # 'salla_token_expiry': datetime.now(),
                })
            else:
                status = False
                message += result.get('message_text', "")
        except Exception as e:
            return False, f"Error : {e}"
        return status, message
    
    def get_base_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('web.base.url')
