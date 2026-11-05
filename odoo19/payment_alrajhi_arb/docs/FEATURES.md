# Al Rajhi Bank (ARB) Payment Gateway

- **المسار والإصدار:** `odoo19/payment_alrajhi_arb` — Odoo 19
- **إصدار الحزمة:** `19.0.1.4.12`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Official-style ARB integration: token API, encrypted trandata, bank-hosted redirect, KSA Card/Mada checkout (Odoo 19).

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Official-style ARB integration: token API, encrypted trandata, bank-hosted redirect, KSA Card/Mada checkout (Odoo 19).
- نموذج Odoo: PaymentProvider: model _inherit
- نموذج Odoo: PaymentTransaction: model _inherit
- نقطة HTTP: '/payment/alrajhi_arb/return' (auth=public, csrf=False)
- نقطة HTTP: '/payment/alrajhi_arb/status/<int:tx_id>' (auth=public, csrf=False)

## التكوين والإضافات

الاعتماديات المعلنة: `payment`
