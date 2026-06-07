# دليل موديولات Odoo في المستودع

هذا الملف يجمع الموديولات الموجودة في المستودع ويصنفها حسب إصدار Odoo: **18** و **19**. يحتوي كل جدول على الاسم التقني للموديول، اسمه الظاهر، ووصف مختصر لما يقوم به.

## Odoo 18

| الموديول | الاسم الظاهر | ماذا يفعل؟ |
|---|---|---|
| `account_invoice_fixed_discount` | Account Fixed Discount | يضيف إمكانية تطبيق خصم بمبلغ ثابت على فواتير العملاء أو الموردين بدل الاعتماد على الخصم النسبي فقط. |
| `archer_meta_lead_ads` | Meta Lead Ads | يربط إعلانات Meta Lead Ads مع CRM لاستيراد بيانات العملاء المحتملين وتحويلها إلى Leads داخل أودو. |
| `bi_global_custom_fields` | All in one add custom fields - Global Custom Fields | يتيح إنشاء حقول مخصصة ديناميكية وربطها بالنماذج والواجهات بدون تعديل مباشر في الكود. |
| `bi_health_care_center_management` | Health Care Center Management | نظام لإدارة مركز رعاية صحية يشمل الحجوزات، المرضى/العملاء، الخدمات، الفواتير، الموقع، المخزون، والحضور. |
| `bi_so_product_quantity_limit` | Sale Order Product Quantity Limit | يضع حدودًا دنيا أو قصوى لكميات المنتجات في أوامر البيع لمنع بيع كميات غير مسموح بها. |
| `bi_sport_center_management` | Sport Center Management | نظام لإدارة مركز أو نادٍ رياضي يشمل الاستفسارات، التسجيلات، الحجوزات، المدربين، الأنشطة، والفواتير. |
| `ie_restrict_qty` | Ie Restrict Qty | يضيف قيودًا على الكميات في عمليات البيع والمخزون وفق إعدادات محددة داخل النظام. |
| `inventory_report_generator` | Inventory All In One Report Generator | منشئ تقارير مخزون ديناميكي لاستخراج وتحليل بيانات المخزون بطرق متعددة. |
| `investment_club` | Investment Clubs Management | نظام لإدارة نوادي الاستثمار والحسابات المرتبطة بها مع متابعة العوائد والعقود والتحليلات. |
| `invoice_stock_move` | Stock Picking From Invoice | ينشئ عمليات استلام أو تسليم مخزني مرتبطة مباشرة بفواتير العملاء أو الموردين. |
| `meno` | meno | موديول إعدادات/تخصيص داخلي متعلق بإصدار Odoo 18. |
| `pdf_print_preview` | Pdf Print Preview | يفتح تقارير PDF في المتصفح للمعاينة والطباعة مباشرة بدل تنزيلها تلقائيًا. |
| `pos_cashier_handover` | POS Cashier Handover Report | يطبع تقرير تسليم خزينة الكاشير عند إغلاق جلسة نقطة البيع. |
| `pos_get_weight_button` | POS Get Weight Button | يضيف زرًا في نقطة البيع لجلب الوزن من الميزان وربطه بسطر المنتج. |
| `pos_receipt_price_before_discount` | POS Receipt: Price Before Discount | يعرض سعر المنتج قبل الخصم في إيصال نقطة البيع عند وجود خصم على السطر. |
| `pos_refund_restriction` | POS Refund Restriction | يقيد عمليات المرتجعات في نقطة البيع لتكون متاحة للمسؤولين فقط. |
| `pos_restrict` | POS User Restrict | يحدد صلاحيات مستخدمي نقطة البيع ويقيد الوصول إلى الجلسات والأوامر حسب المستخدم. |
| `prt_report_attachment_preview` | Open PDF Reports and PDF Attachments in Browser | يفتح تقارير ومرفقات PDF في تبويب المتصفح بدل تنزيلها مباشرة. |
| `sale_contract_auto` | Sale Contract Auto | ينشئ العقود تلقائيًا من أوامر البيع مع ربطها بالفواتير والبوابة والمراسلات. |
| `sale_kitchen_receipt` | Kitchen Receipt from Quotation | يطبع إيصال مطبخ من عرض السعر/أمر البيع لاستخدامه في تجهيز الطلبات. |
| `sale_order_automation` | Sale Order Automation | يشغل سير عمل البيع تلقائيًا مثل تأكيد أمر البيع، إنشاء الفاتورة، اعتمادها، وتنفيذ التسليم. |
| `sale_order_contract` | Sale Order Contract | ينشئ عقدًا مرتبطًا بأمر البيع تلقائيًا لتوثيق شروط الصفقة. |
| `sale_order_contract_terms` | Sales Order Contract Terms (AR/EN) - 4 Pages | يضيف تقرير عقد مستقل لأمر البيع بشروط ثنائية اللغة عربي/إنجليزي على أربع صفحات. |
| `sale_stock_restrict` | Sale Stock Restrict | يمنع أو يحذر من بيع المنتجات غير المتوفرة في المخزون حسب قواعد البيع والمخزون. |
| `sales_credit_limit` | Customer Credit Limit with Due Amount Warning | يدير حد الائتمان للعميل مع تحذير أو منع البيع عند تجاوز المبالغ المستحقة. |
| `stock_move_invoice` | Invoice From Stock Picking | ينشئ فواتير من عمليات المخزون/الشحن لتسهيل الربط بين التسليم والفوترة. |
| `stock_split_transfer` | Stock Split Transfer | يدعم التحويلات الداخلية على خطوتين مع التحكم في المواقع الظاهرة لكل مستخدم. |
| `transfer_wizard` | trade_paints_wizard | معالج لتسهيل إنشاء أو تنفيذ التحويلات المرتبطة بالمبيعات والمشتريات والمخزون. |
| `whatsapp_mail_messaging` | Odoo Whatsapp Connector | يربط أودو بواتساب لإرسال الرسائل من مستندات مثل المبيعات والفواتير والموقع. |
| `wm_purchase_global_discount` | Purchase Order Global Discount | يضيف خصمًا عامًا على أمر الشراء مشابهًا لخصم أوامر البيع في أودو. |

## Odoo 19

| الموديول | الاسم الظاهر | ماذا يفعل؟ |
|---|---|---|
| `WPS` | WPS | موديول مرتبط بنظام الرواتب ويعتمد على Payroll لإدارة أو تجهيز بيانات WPS. |
| `account_invoice_fixed_discount` | Account Fixed Discount | يضيف إمكانية تطبيق خصم بمبلغ ثابت على فواتير العملاء أو الموردين. |
| `advanced_accounting_reports` | Advanced Accounting Reports | يوفر تقارير محاسبية متقدمة مثل الأستاذ العام وميزان المراجعة مع الأبعاد التحليلية والعملات المتعددة. |
| `auto_project_stages` | Project Task Visit Forms | يضيف تبويبات وحقول تفصيلية لزيارات الموقع وزيارات الشركات داخل مهام المشاريع. |
| `bi_employee_travel_managment` | HR Employee Travel Expense in Odoo | يدير طلبات سفر الموظفين ومصاريف السفر والسلف والتعويضات المرتبطة بالموارد البشرية والمشاريع. |
| `bi_so_product_quantity_limit` | Sale Order Product Quantity Limit | يضع حدودًا دنيا أو قصوى لكميات المنتجات في أوامر البيع. |
| `crm_project_linker` | CRM Project Linker | ينشئ مشاريع من فرص CRM ويربطها بالفرص وأوامر البيع لتسهيل المتابعة. |
| `inventory_report_generator` | Inventory All In One Report Generator | منشئ تقارير مخزون ديناميكي لاستخراج وتحليل بيانات المخزون. |
| `invoice_stock_move` | Stock Picking From Invoice | ينشئ عمليات استلام أو تسليم مخزني من فواتير العملاء أو الموردين. |
| `invoice_tracking` | Invoice Tracking | يضيف تتبعًا للفواتير وربطًا بالمراسلات والمشتريات لمتابعة حالة الفاتورة. |
| `meno` | meno | موديول إعدادات/تخصيص داخلي متعلق بإصدار Odoo 19. |
| `pos_daily_sequence` | POS Daily Sequence | يعيد ترقيم أوامر نقطة البيع يوميًا تلقائيًا لتسهيل تنظيم الإيصالات والجلسات. |
| `pos_get_weight_button` | POS Get Weight Button | يضيف زرًا في نقطة البيع لجلب الوزن من الميزان وربطه بسطر المنتج. |
| `rm_hr_attendance_sheet` | HR Attendance Sheet and Policies | يدير كشوف الحضور وسياسات التأخير والغياب والعمل الإضافي والربط مع الرواتب. |
| `saudi_tax_invoice` | Saudi Tax Invoice | يضيف تقرير فاتورة ضريبية بنمط سعودي مع زر إجراء للطباعة أو العرض. |
| `stock_intercompany_transfer` | Inter Company Stock Transfer | ينشئ أوامر استلام/تسليم مقابلة بين الشركات عند تنفيذ تحويلات مخزنية بينية. |
| `test_AI_finance` | AI Finance V1 | موديول مالي ذكي يوفر وظائف مثل المساعد المالي الافتراضي ومعالجة OCR للفواتير أو المستندات. |
| `whatsapp_mail_messaging` | Odoo Whatsapp Connector | يربط أودو بواتساب لإرسال الرسائل من مستندات مثل المبيعات والفواتير والموقع. |
| `wm_purchase_global_discount` | Purchase Order Global Discount | يضيف خصمًا عامًا على أمر الشراء مشابهًا لخصم أوامر البيع. |
| `zk_attendance_integration_v19` | TechScope / ZK Attendance Integration | يربط أجهزة حضور ZK مع أودو لجلب سجلات الحضور وربطها بالموظفين والحضور. |
