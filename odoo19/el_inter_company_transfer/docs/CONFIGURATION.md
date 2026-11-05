# Inter Company Transfer

- **المسار والإصدار:** `odoo19/el_inter_company_transfer` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automate inter-company stock, sale, purchase, and accounting documents

## الحقول ونقاط الإعداد الموجودة في المصدر

- `inter_company_transfer_id (Many2one)`
- `inter_company_sale_order_id (Many2one)`
- `inter_company_warehouse_id (Many2one)`
- `inter_company_transfer_id (Many2one)`
- `inter_company_transfer_id (Many2one)`
- `source_company_id (Many2one)`
- `dest_company_id (Many2one)`
- `from_warehouse_id (Many2one)`
- `to_warehouse_id (Many2one)`
- `config_id (Many2one)`
- `company_id (Many2one)`
- `company_id (Many2one)`
- `inter_company_transfer_id (Many2one)`
- `inter_company_purchase_order_id (Many2one)`
- `source_company_id (Many2one)`
- `dest_company_id (Many2one)`
- `source_company_id (Many2one)`
- `dest_company_id (Many2one)`
- `from_warehouse_id (Many2one)`
- `to_warehouse_id (Many2one)`
- `company_id (Many2one)`
- `company_id (Many2one)`

### إجراءات الإعداد

- `models/stock_inter_company_transfer.py::_get_config`
- `models/inter_company_config.py::_compute_display_name`
- `models/inter_company_config.py::_check_company_warehouses`
- `models/inter_company_config.py::_find_for_sale`
- `models/inter_company_config.py::_find_for_purchase`
- `models/inter_company_config.py::_company_from_partner`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
