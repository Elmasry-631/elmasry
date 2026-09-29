def migrate(cr, version):
    cr.execute("""
        SELECT 1
          FROM information_schema.columns
         WHERE table_name = 'payment_provider'
           AND column_name = 'hyperpay_data_brands'
    """)
    if not cr.fetchone():
        cr.execute("""
            ALTER TABLE payment_provider
            ADD COLUMN hyperpay_data_brands VARCHAR
        """)
        cr.execute("""
            UPDATE payment_provider
               SET hyperpay_data_brands = 'VISA'
             WHERE code = 'hyperpay'
               AND hyperpay_data_brands IS NULL
        """)
