# تقرير إصلاح مشروع Elmasry Odoo

**التاريخ:** 2026-11-04  
**المصدر:** `elmasry.zip`  
**النطاق:** إصلاح ساكن ومراجعة مصدرية لمجلدات Odoo 17–20. لم يتم تشغيل Odoo أو تثبيت الموديولات على قاعدة بيانات.

## 1. ملخص التنفيذ

- عدد الموديولات ذات `__manifest__.py`: **112**.
- الموديول الذي احتاج إصلاحات مؤكدة من الفحص الساكن والمراجعة اليدوية: `odoo20/el_dashboard_builder`.
- تم تعديل **3 ملفات** داخل هذا الموديول.
- لم يتم تعديل النسخة الأصلية `elmasry.zip`.
- نسخة التسليم الكاملة لا تتضمن مجلد Git `.git` لتقليل الحجم؛ جميع ملفات المصدر الموجودة خارج `.git` تم الاحتفاظ بها، بما فيها الأرشيفات الداخلية.

## 2. التغييرات المنفذة

### Odoo 20 — `el_dashboard_builder`

#### `static/src/xml/dashboard_templates.xml`
1. استبدال عنصر QWeb غير صالح داخل `aria-label` في موضعين باستخدام `t-attf-aria-label`.
2. تهريب عامل المقارنة `<` داخل قيمة XML attribute إلى `&lt;`.
3. إغلاق عنصر `input` بصيغة XML ذاتية الإغلاق.

#### `controllers/controllers.py`
1. نقل route `/dashboard/builder/<int:dashboard_id>` من helper إلى `dashboard_view`، وهي الدالة التي تنفذ عرض Dashboard فعليًا.
2. إزالة تعريف helper المكرر `_get_dashboard_filters` الذي كان يلغي التعريف السابق.
3. إضافة استيراد `_` المستخدم في ترجمة عنوان الفلتر.
4. استبدال `eval()` بـ `ast.literal_eval()` عند قراءة `filter_domain`، لتقييد التحليل إلى القيم الحرفية بدل تنفيذ تعبيرات Python عامة.
5. تصحيح رابط الحذف ليشير إلى External ID الموجود `el_dashboard_builder.action_dashboard_builder_list`.

#### `tests/test_dashboard_builder.py`
- تصحيح 8 مراجع XML ID من `dashboard_builder.*` إلى الاسم التقني الصحيح `el_dashboard_builder.*`.

## 3. نتائج التحقق الساكن بعد الإصلاح

| الفحص | الملفات المفحوصة | الإخفاقات |
|---|---:|---:|
| Python AST parsing | 1,140 | 0 |
| XML parsing | 706 | 0 |
| Manifest literal parsing | 112 | 0 |
| JavaScript `node --check` | 89 | 0 |
| مراجع XML IDs في اختبارات `el_dashboard_builder` | 8 | 0 مراجع مفقودة |

تم التحقق كذلك من عدم وجود تعريفات مكررة لطرق Controller بعد الإصلاح، ومن أن route عرض Dashboard أصبح مرتبطًا بـ `dashboard_view`.

## 4. نقاط لم يتم تعديلها عمدًا

### اعتماديات غير موجودة في الأرشيف

- `odoo19/el_prevent_negative_stock` يعتمد على `nmo_sale_order_approval_workflow` و`nmo_stock_user_restriction`.
- `odoo19/smsa_express_delivery_carrier` يعتمد على `odoo_shipping_service_apps`.
- `odoo19/deduction_management` يعتمد على `hr_work_entry_enterprise`، وهو اعتماد Enterprise وليس جزءًا من Odoo Community القياسي.

لم أحذف هذه الاعتماديات من Manifest لأن ذلك قد يجعل الموديول يثبت ظاهريًا بينما يفقد تكاملًا أو منطقًا مطلوبًا. يلزم توفير الموديولات الناقصة أو اعتماد بديل متوافق بعد مراجعة الوظائف.

### موديول `meno` في الإصدارات 17 و18 و19 و20

يعدل هذا الموديول `database.expiration_date` إلى سنة 5000 ويستدعي `cr.commit()` أثناء التنفيذ/الترقية. لم أعدّل هذا السلوك أو أساعد على تجاوز آليات الترخيص أو انتهاء الصلاحية. يجب استبعاده أو استبداله بآلية مرخصة ومصرح بها قبل استخدامه إنتاجيًا.

### UTF-8 BOM في `ai_finance_suite` (Odoo 19)

تم العثور على BOM في أربعة ملفات Python. لم يتم حذفها لأن فحص Python AST نجح معها، ووجود BOM وحده ليس خطأ parsing في Python. يمكن توحيد الترميز لاحقًا كتغيير تنسيقي مستقل، وليس باعتباره إصلاح عطل مثبت.

## 5. ما لم يتم إثباته

- لم يتم تشغيل اختبارات Odoo (`TransactionCase`) لعدم توفر حزمة/بيئة Odoo في بيئة الفحص الحالية.
- لم يتم تثبيت `el_dashboard_builder` على قاعدة بيانات Odoo 20.
- لم يتم اختبار HTTP routes أو صلاحيات المستخدمين أو multi-company أو assets داخل المتصفح.
- لم يتم تأكيد توافق كل استدعاءات ORM مع Odoo 20 runtime.

لذلك نتائج الاختبارات أعلاه **ساكنة فقط** ولا تعني شهادة تثبيت أو تشغيل ناجح.

## 6. خطوات التحقق المطلوبة في بيئة Odoo 20

1. ضع مجلد `el_dashboard_builder` ضمن `addons_path`.
2. حدّث قائمة التطبيقات.
3. نفّذ تثبيتًا تجريبيًا على قاعدة بيانات غير إنتاجية.
4. شغّل اختبارات الموديول باستخدام `--test-enable --stop-after-init` مع اسم قاعدة اختبار.
5. اختبر فتح `/dashboard/builder/<id>`، وصفحة التحرير، ومشاركة Dashboard، والحذف، والـ widget data APIs.
6. اختبر حساب مستخدم عادي ومدير Dashboard، ثم اختبر مستخدمًا من شركة أخرى للتأكد من العزل.

## 7. الملفات المعدلة

- `odoo20/el_dashboard_builder/static/src/xml/dashboard_templates.xml`
- `odoo20/el_dashboard_builder/controllers/controllers.py`
- `odoo20/el_dashboard_builder/tests/test_dashboard_builder.py`
