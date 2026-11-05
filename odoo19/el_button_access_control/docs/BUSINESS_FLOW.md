# Button Access Control

- **المسار والإصدار:** `odoo19/el_button_access_control` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Control button visibility per user group — show/hide buttons in any view without editing XML

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Button Access Control
- المستخدم يبدأ من قائمة: Rules
- المستخدم يبدأ من قائمة: Configuration
- المستخدم يبدأ من قائمة: User Groups
- النموذج/الامتداد المعني: ElButtonAccessRule: model _name
- النموذج/الامتداد المعني: Base: model _inherit
- العملية البرمجية المتاحة: `setUpClass` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `_create_rule` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `_get_view_arch` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_01_create_rule` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_02_rule_requires_groups` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_03_unique_constraint` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_04_whitelist_injects_groups` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_05_whitelist_multiple_groups` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_06_blacklist_mode` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_07_view_type_all` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_08_view_type_list` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_09_view_type_kanban` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_10_archive_rule` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_11_inactive_rule_not_applied` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_12_multiple_rules_same_model` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_13_rule_sequence_ordering` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `setUpClass` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_20_fields_view_get_does_not_crash` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_21_rule_creation_clears_cache` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `test_22_rule_deletion` في `tests/test_button_access.py`
- العملية البرمجية المتاحة: `_selection_button_name` في `models/button_access_rule.py`
- العملية البرمجية المتاحة: `_onchange_model_view` في `models/button_access_rule.py`
- العملية البرمجية المتاحة: `_onchange_button_name` في `models/button_access_rule.py`
- العملية البرمجية المتاحة: `action_scan_buttons` في `models/button_access_rule.py`
- العملية البرمجية المتاحة: `_scan_model_buttons` في `models/button_access_rule.py`
- العملية البرمجية المتاحة: `rpc_get_available_buttons` في `models/button_access_rule.py`
- العملية البرمجية المتاحة: `create` في `models/button_access_rule.py`
- العملية البرمجية المتاحة: `write` في `models/button_access_rule.py`
- العملية البرمجية المتاحة: `unlink` في `models/button_access_rule.py`
- العملية البرمجية المتاحة: `_lookup_button_string` في `models/button_access_rule.py`
- العملية البرمجية المتاحة: `action_test_rule` في `models/button_access_rule.py`
- العملية البرمجية المتاحة: `_el_apply_button_access_rules` في `models/base.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
