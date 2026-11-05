# Dashboard Builder

- **المسار والإصدار:** `odoo20/el_dashboard_builder` — Odoo 20
- **إصدار الحزمة:** `20.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Drag-and-drop dashboard builder with customizable widgets

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `base`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_dashboard_builder`.
- خطأ تحميل dependency `web`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_dashboard_builder`.
- خطأ تحميل dependency `mail`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_dashboard_builder`.
- خطأ تحميل dependency `base_setup`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_dashboard_builder`.
- غياب مورد security/dashboard_security.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/dashboard_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/dashboard_menu.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/dashboard_templates.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد wizard/item_config_wizard_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد report/dashboard_report_templates.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد data/ir_sequence_data.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد data/dashboard_default_widgets.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 20: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
