# Balance Confirmation

- **المسار والإصدار:** `odoo19/partner_balance_confirmation` — Odoo 19
- **إصدار الحزمة:** `19.0.3.6.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Customer Balance Confirmation (Imdad / Namo templates)

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: ResPartner: model _inherit
- النموذج/الامتداد المعني: BalanceConfirmationWizard: model _name
- العملية البرمجية المتاحة: `action_open_balance_confirmation` في `models/res_partner.py`
- العملية البرمجية المتاحة: `_compute_balance` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_build_report_data` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `action_print_pdf` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `action_print_word` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `action_send_email` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_get_template_path` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_generate_docx` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_fill_template_safe` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_replace_placeholders_in_xml` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_find_libreoffice` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_path_to_file_uri` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_run_libreoffice_conversion` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_ensure_arabic_fonts_installed` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_is_sakkal_majalla_installed` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_is_font_installed` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_get_font_install_dir` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_install_fonts_from_module` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_ensure_sakkal_majalla_alias` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_refresh_font_cache` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_generate_pdf_from_word` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_try_convert_with_msword` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_build_fallback_reason` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_build_libreoffice_diagnostic` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_generate_pdf_qweb_fallback` في `wizard/balance_confirmation_wizard.py`
- العملية البرمجية المتاحة: `_set_pdf_metadata` في `wizard/balance_confirmation_wizard.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
