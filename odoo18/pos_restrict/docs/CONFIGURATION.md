# POS User Restrict

- **المسار والإصدار:** `odoo18/pos_restrict` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Restricts User access to pos and orders.

## الحقول ونقاط الإعداد الموجودة في المصدر

- لا توجد عناصر معلنة في ملفات الموديول.

### إجراءات الإعداد

- `models/pos_config.py::_compute_users_allowed`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
