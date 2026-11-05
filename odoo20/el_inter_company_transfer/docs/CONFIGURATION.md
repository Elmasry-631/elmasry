# Inter Company Internal Transfer

- **المسار والإصدار:** `odoo20/el_inter_company_transfer` — Odoo 20
- **إصدار الحزمة:** `20.0.1.0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Request stock transfers between warehouses of different companies

## الحقول ونقاط الإعداد الموجودة في المصدر

- `company_id (Many2one)`
- `source_warehouse_id (Many2one)`
- `dest_company_id (Many2one)`
- `dest_warehouse_id (Many2one)`
- `company_id (Many2one)`

### إجراءات الإعداد

- لا توجد عناصر معلنة في ملفات الموديول.

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
