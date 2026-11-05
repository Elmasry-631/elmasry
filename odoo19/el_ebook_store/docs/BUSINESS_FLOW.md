# E-Book Store

- **المسار والإصدار:** `odoo19/el_ebook_store` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Sell e-books with unique access codes — online reader + download

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: E-Book Store
- المستخدم يبدأ من قائمة: Access Codes
- المستخدم يبدأ من قائمة: Customer Libraries
- المستخدم يبدأ من قائمة: Access Logs
- النموذج/الامتداد المعني: EbookCode: model _name
- النموذج/الامتداد المعني: EbookAccessLog: model _name
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- النموذج/الامتداد المعني: EbookLibrary: model _name
- النموذج/الامتداد المعني: ProductTemplate: model _inherit
- النموذج/الامتداد المعني: GenerateCodesWizard: model _name
- العملية البرمجية المتاحة: `test_02_generate_random_codes` في `tests/test_ebook_store.py`
- العملية البرمجية المتاحة: `test_03_generate_manual_codes` في `tests/test_ebook_store.py`
- العملية البرمجية المتاحة: `test_10_access_log_created` في `tests/test_ebook_store.py`
- العملية البرمجية المتاحة: `_generate_random_code` في `models/ebook_code.py`
- العملية البرمجية المتاحة: `generate_codes` في `models/ebook_code.py`
- العملية البرمجية المتاحة: `action_assign` في `models/ebook_code.py`
- العملية البرمجية المتاحة: `action_use` في `models/ebook_code.py`
- العملية البرمجية المتاحة: `action_assign_and_expire` في `models/ebook_code.py`
- العملية البرمجية المتاحة: `action_reset` في `models/ebook_code.py`
- العملية البرمجية المتاحة: `action_expire` في `models/ebook_code.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/sale_order.py`
- العملية البرمجية المتاحة: `_compute_code_stats` في `models/product_template.py`
- العملية البرمجية المتاحة: `action_generate` في `wizard/generate_codes_wizard.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
