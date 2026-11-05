# Button Access Control

- **المسار والإصدار:** `odoo19/el_button_access_control` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Control button visibility per user group — show/hide buttons in any view without editing XML

## الصلاحيات والحماية المكتشفة

### ACL

- access_el_button_access_rule_user: model=model_el_button_access_rule, group=group_button_access_user, read/write/create/delete=1/0/0/0
- access_el_button_access_rule_manager: model=model_el_button_access_rule, group=group_button_access_manager, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_button_access_user`, `group_button_access_manager`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/button_access_rule.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.