from . import models


def post_init_hook(env):
    # Backfill confirmed_by_id from chatter tracking (actual confirmer),
    # not write_uid. In Odoo 18 sale.order, state tracking stores
    # new_value_char='أمر البيع' (or 'sale' in English).
    env.cr.execute("""
        UPDATE sale_order so SET confirmed_by_id = sub.create_uid
        FROM (
          SELECT DISTINCT ON (m.res_id) m.res_id, m.create_uid
          FROM mail_message m
          JOIN mail_tracking_value t ON t.mail_message_id=m.id
          JOIN ir_model_fields f ON f.id=t.field_id
          WHERE m.model='sale.order'
            AND f.model='sale.order' AND f.name='state'
            AND t.new_value_char IN ('أمر البيع', 'sale', 'Sales Order')
          ORDER BY m.res_id, m.create_date DESC
        ) sub
        WHERE so.id=sub.res_id AND so.state='sale' AND so.confirmed_by_id IS NULL
    """)
    # Fallback for orders without chatter tracking (e.g. imported)
    env.cr.execute("""
        UPDATE sale_order SET confirmed_by_id = COALESCE(write_uid, user_id, create_uid)
        WHERE state='sale' AND confirmed_by_id IS NULL
    """)
