# Barcode Price Display

- **المسار والإصدار:** `odoo19/el_barcode_price_display` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Standalone barcode scanner price display page — no login needed

## الصلاحيات والحماية المكتشفة

### ACL

- access_barcode_price_user: model=product.model_product_product, group=group_barcode_price_user, read/write/create/delete=1/0/0/0

### المجموعات وقواعد السجلات

- المجموعات: `group_barcode_price_user`, `group_barcode_price_manager`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- '/price-display' (auth=public, csrf=False)
- '/price-display/search' (auth=public, csrf=False)

مواضع `sudo()` المرصودة:

- `controllers/main.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.