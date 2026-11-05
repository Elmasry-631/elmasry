# Restrict Journal for Users (Whitelist)

- **المسار والإصدار:** `odoo18/el_restrict_journal` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Per-user journal whitelist — only allowed journals are visible

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `base`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_restrict_journal`.
- خطأ تحميل dependency `account`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_restrict_journal`.
- غياب مورد security/account_restrict_journal_groups.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد security/ir.model.access.csv: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد security/account_restrict_journal_rules.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/res_users_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/account_move_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
