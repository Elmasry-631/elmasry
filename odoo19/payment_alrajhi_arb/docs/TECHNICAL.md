# Al Rajhi Bank (ARB) Payment Gateway

- **المسار والإصدار:** `odoo19/payment_alrajhi_arb` — Odoo 19
- **إصدار الحزمة:** `19.0.1.4.12`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Official-style ARB integration: token API, encrypted trandata, bank-hosted redirect, KSA Card/Mada checkout (Odoo 19).

## المكونات المكتشفة

- Python: 10 file(s)
- XML: 3 file(s)

### نماذج وامتدادات Odoo

- PaymentProvider: model _inherit
- PaymentTransaction: model _inherit

### الملفات المصدرية ذات الصلة

- `controllers/__init__.py`
- `controllers/alrajhi_arb.py`
- `views/payment_provider_views.xml`
- `views/arb_redirect_form_templates.xml`
- `models/payment_provider.py`
- `models/payment_transaction.py`
- `models/__init__.py`

### حقول معلنة

- `code (Selection)`
- `arb_tranportal_id (Char)`
- `arb_tranportal_password (Char)`
- `arb_resource_key (Char)`
- `arb_endpoint_url_test (Char)`
- `arb_endpoint_url_prod (Char)`
- `arb_track_id (Char)`
- `arb_return_token (Char)`

### XML IDs

- `views/payment_provider_views.xml::payment_provider_form_alrajhi_arb`
- `views/arb_redirect_form_templates.xml::arb_redirect_form_view`
- `views/arb_redirect_form_templates.xml::arb_redirect_form`
- `data/payment_provider_data.xml::payment_provider_alrajhi_arb`