# eBook Serial Delivery

- **المسار والإصدار:** `odoo19/ebook_serial_delivery` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Deliver eBook licenses using standard Inventory Serial Numbers (stock.lot) — no custom "activation code" model.

## الحقول ونقاط الإعداد الموجودة في المصدر

- لا توجد عناصر معلنة في ملفات الموديول.

### إجراءات الإعداد

- `tests/test_serial_mail_template.py::test_template_chosen_in_settings_is_sent`
- `tests/test_serial_mail_template.py::test_empty_setting_falls_back_to_default`
- `models/res_config_settings.py::action_open_ebook_serial_mail_template`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
