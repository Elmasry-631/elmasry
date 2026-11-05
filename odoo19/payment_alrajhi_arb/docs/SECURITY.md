# Al Rajhi Bank (ARB) Payment Gateway

- **المسار والإصدار:** `odoo19/payment_alrajhi_arb` — Odoo 19
- **إصدار الحزمة:** `19.0.1.4.12`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Official-style ARB integration: token API, encrypted trandata, bank-hosted redirect, KSA Card/Mada checkout (Odoo 19).

## الصلاحيات والحماية المكتشفة

### ACL

- لا توجد عناصر معلنة في ملفات الموديول.

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- '/payment/alrajhi_arb/return' (auth=public, csrf=False)
- '/payment/alrajhi_arb/status/<int:tx_id>' (auth=public, csrf=False)

مواضع `sudo()` المرصودة:

- `controllers/alrajhi_arb.py`
- `models/payment_provider.py`
- `models/payment_transaction.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.