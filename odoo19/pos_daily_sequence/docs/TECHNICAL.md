# POS Daily Sequence

- **المسار والإصدار:** `odoo19/pos_daily_sequence` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automatically reset POS order numbering every day

## المكونات المكتشفة

- Python: 6 file(s)
- XML: 3 file(s)
- JavaScript/TypeScript: 1 file(s)

### نماذج وامتدادات Odoo

- PosConfig: model _inherit
- PosSession: model _inherit
- PosOrder: model _inherit

### الملفات المصدرية ذات الصلة

- `views/pos_config_views.xml`
- `models/pos_config.py`
- `models/__init__.py`
- `models/pos_session.py`
- `models/pos_order.py`
- `security/ir.model.access.csv`
- `static/src/app/models/pos_order.js`

### حقول معلنة

- `daily_sequence_id (Many2one)`
- `use_daily_sequence (Boolean)`
- `daily_sequence_prefix (Char)`
- `daily_sequence_reset_period (Selection)`
- `daily_sequence_padding (Integer)`
- `daily_sequence_id (Many2one)`
- `daily_order_number (Char)`

### XML IDs

- `views/pos_config_views.xml::pos_config_view_form_inherit_daily_sequence`
- `views/pos_config_views.xml::daily_order_sequence`
- `views/pos_config_views.xml::pos_order_view_tree_inherit_daily_sequence`
- `views/pos_config_views.xml::pos_order_view_form_inherit_daily_sequence`
- `views/pos_config_views.xml::pos_order_view_search_inherit_daily_sequence`
- `data/ir_sequence_data.xml::sequence_pos_daily_order`
- `static/src/app/screens/receipt_screen/receipt/receipt_header.xml::template`