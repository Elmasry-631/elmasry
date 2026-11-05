# Inter Company Transfer

- **المسار والإصدار:** `odoo19/el_inter_company_transfer` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automate inter-company stock, sale, purchase, and accounting documents

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `base`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_inter_company_transfer`.
- خطأ تحميل dependency `mail`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_inter_company_transfer`.
- خطأ تحميل dependency `stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_inter_company_transfer`.
- خطأ تحميل dependency `sale_management`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_inter_company_transfer`.
- خطأ تحميل dependency `sale_stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_inter_company_transfer`.
- خطأ تحميل dependency `purchase`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_inter_company_transfer`.
- خطأ تحميل dependency `purchase_stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_inter_company_transfer`.
- خطأ تحميل dependency `account`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_inter_company_transfer`.
- غياب مورد security/security_groups.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد security/ir.model.access.csv: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد data/inter_company_sequence.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/inter_company_config_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/stock_inter_company_transfer_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/return_inter_company_transfer_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/res_company_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/sale_order_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/purchase_order_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/stock_picking_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/account_move_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/inter_company_menus.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 19: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
