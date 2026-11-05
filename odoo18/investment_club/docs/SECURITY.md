# Investment Clubs Management

- **المسار والإصدار:** `odoo18/investment_club` — Odoo 18
- **إصدار الحزمة:** `18.0.12.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Complete investment management system with Unified Return System

## الصلاحيات والحماية المكتشفة

### ACL

- access_investment_club: model=model_investment_club, group=group_investment_access, read/write/create/delete=1/1/1/1
- access_investment_project: model=model_investment_project, group=group_investment_access, read/write/create/delete=1/1/1/1
- access_investment_membership: model=model_investment_membership, group=group_investment_access, read/write/create/delete=1/1/1/1
- access_membership_renewal: model=model_membership_renewal, group=group_investment_access, read/write/create/delete=1/1/1/1
- access_investment_subscription: model=model_investment_subscription, group=group_investment_access, read/write/create/delete=1/1/1/1
- access_actual_return: model=model_investment_actual_return, group=group_investment_access, read/write/create/delete=1/1/1/1
- access_membership_terminate_wizard: model=model_membership_terminate_wizard, group=group_investment_access, read/write/create/delete=1/1/1/1
- access_subscription_terminate_wizard: model=model_subscription_terminate_wizard, group=group_investment_access, read/write/create/delete=1/1/1/1
- access_investor_death_wizard: model=model_investor_death_wizard, group=group_investment_access, read/write/create/delete=1/1/1/1
- access_investment_club_user: model=model_investment_club, group=group_investment_user, read/write/create/delete=1/0/0/0
- access_investment_club_manager: model=model_investment_club, group=group_investment_manager, read/write/create/delete=1/1/1/1
- access_investment_project_user: model=model_investment_project, group=group_investment_user, read/write/create/delete=1/0/0/0
- access_investment_project_manager: model=model_investment_project, group=group_investment_manager, read/write/create/delete=1/1/1/1
- access_investment_membership_user: model=model_investment_membership, group=group_investment_user, read/write/create/delete=1/1/1/0
- access_investment_membership_manager: model=model_investment_membership, group=group_investment_manager, read/write/create/delete=1/1/1/1
- access_membership_renewal_user: model=model_membership_renewal, group=group_investment_user, read/write/create/delete=1/1/1/0
- access_membership_renewal_manager: model=model_membership_renewal, group=group_investment_manager, read/write/create/delete=1/1/1/1
- access_investment_subscription_user: model=model_investment_subscription, group=group_investment_user, read/write/create/delete=1/1/1/0
- access_investment_subscription_manager: model=model_investment_subscription, group=group_investment_manager, read/write/create/delete=1/1/1/1
- access_actual_return_user: model=model_investment_actual_return, group=group_investment_user, read/write/create/delete=1/1/1/0
- access_actual_return_manager: model=model_investment_actual_return, group=group_investment_manager, read/write/create/delete=1/1/1/1
- access_membership_terminate_wizard_user: model=model_membership_terminate_wizard, group=group_investment_user, read/write/create/delete=1/1/1/0
- access_membership_terminate_wizard_manager: model=model_membership_terminate_wizard, group=group_investment_manager, read/write/create/delete=1/1/1/1
- access_subscription_terminate_wizard_user: model=model_subscription_terminate_wizard, group=group_investment_user, read/write/create/delete=1/1/1/0
- access_subscription_terminate_wizard_manager: model=model_subscription_terminate_wizard, group=group_investment_manager, read/write/create/delete=1/1/1/1
- access_investor_death_wizard_user: model=model_investor_death_wizard, group=group_investment_user, read/write/create/delete=1/1/1/0
- access_investor_death_wizard_manager: model=model_investor_death_wizard, group=group_investment_manager, read/write/create/delete=1/1/1/1
- access_terminate_reason: model=model_terminate_reason, group=group_investment_access, read/write/create/delete=1/1/1/1
- access_terminate_reason_user: model=model_terminate_reason, group=group_investment_user, read/write/create/delete=1/0/0/0
- access_terminate_reason_manager: model=model_terminate_reason, group=group_investment_manager, read/write/create/delete=1/1/1/1
- access_investment_dashboard: model=model_investment_dashboard, group=group_investment_access, read/write/create/delete=1/1/1/1
- access_investment_dashboard_user: model=model_investment_dashboard, group=group_investment_user, read/write/create/delete=1/0/0/0
- access_investment_dashboard_manager: model=model_investment_dashboard, group=group_investment_manager, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_investment_user`, `group_investment_access`, `group_investment_manager`
- قواعد السجلات: `investment_project_access_rule`, `investment_subscription_access_rule`, `investment_membership_access_rule`, `actual_return_access_rule`, `investment_project_user_rule`, `investment_project_manager_rule`, `investment_subscription_user_rule`, `investment_subscription_manager_rule`, `investment_membership_user_rule`, `investment_membership_manager_rule`, `actual_return_user_rule`, `actual_return_manager_rule`

### واجهات HTTP ورفع الصلاحيات

- '/investment/dashboard/stats' (auth=user)

مواضع `sudo()` المرصودة:

- `models/investment_actual_return_inherit.py`
- `models/investment_subscription.py`
- `models/membership.py`
- `models/investment_project_inherit.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.