# E-Book Store

- **المسار والإصدار:** `odoo19/el_ebook_store` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Sell e-books with unique access codes — online reader + download

## الصلاحيات والحماية المكتشفة

### ACL

- access_ebook_code_user: model=model_ebook_code, group=group_ebook_user, read/write/create/delete=1/0/0/0
- access_ebook_code_manager: model=model_ebook_code, group=group_ebook_manager, read/write/create/delete=1/1/1/1
- access_ebook_library_user: model=model_ebook_library, group=group_ebook_user, read/write/create/delete=1/0/0/0
- access_ebook_library_manager: model=model_ebook_library, group=group_ebook_manager, read/write/create/delete=1/1/1/1
- access_ebook_access_log_user: model=model_ebook_access_log, group=group_ebook_user, read/write/create/delete=1/0/0/0
- access_ebook_access_log_manager: model=model_ebook_access_log, group=group_ebook_manager, read/write/create/delete=1/1/1/1
- access_generate_codes_wizard: model=model_generate_codes_wizard, group=group_ebook_manager, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_ebook_user`, `group_ebook_manager`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- '/my/library' (auth=user)
- '/my/ebook/<int:library_id>/read' (auth=user)
- '/my/ebook/<int:library_id>/download' (auth=user)

مواضع `sudo()` المرصودة:

- `controllers/portal.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.