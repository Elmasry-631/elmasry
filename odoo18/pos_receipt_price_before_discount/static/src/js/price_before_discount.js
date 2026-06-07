///** @odoo-module **/
//
//import { patch } from "@web/core/utils/patch";
//import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
//
//patch(Orderline.prototype, {
//    setup() {
//        super.setup?.();
//
//        const pos = this.env.services.pos;
//        const line = this.props.line;
//        if (!line || !line.productName) return;
//
//        // ابحث عن المنتج بالاسم
//        const products = pos.data.records["product.product"];
//        if (!products) return;
//
//        let foundProduct = null;
//        for (const p of products.values()) {
//            if (p.display_name === line.productName || p.name === line.productName) {
//                foundProduct = p;
//                break;
//            }
//        }
//
//        if (!foundProduct) return;
//
//        const lp = foundProduct.lst_price ?? foundProduct.list_price;
//        line.lst_price = lp;
//        const fmt =
//            this.env.utils?.formatCurrency ||
//            this.env.services?.pos?.format_currency ||
//            this.env.services?.pos?.formatCurrency;
//
//        line.lst_price_fmt = fmt ? fmt(lp || 0) : String(lp || 0);
//
//        const soldPrice = parseFloat(
//            line.unitPrice?.replace(/[^\d.]/g, "") || 0
//        );
//        line.show_lst_price = lp > soldPrice;
//    },
//});

/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";

patch(Orderline.prototype, {
    // يحوّل "265.50 LE" إلى 265.5 (يدعم فاصلة كمان)
    _toFloat(priceStr) {
        if (!priceStr) return 0;

        // نشيل أي نص (عملة، Units، إلخ)
        let s = String(priceStr).replace(/[^\d.,]/g, "");

        // لو فيه , و . مع بعض → , آلاف
        if (s.includes(",") && s.includes(".")) {
            s = s.replace(/,/g, "");
        }
        // لو فيه , فقط → عشرية
        else if (s.includes(",")) {
            s = s.replace(",", ".");
        }

        const n = parseFloat(s);
        return Number.isFinite(n) ? n : 0;
    },

    // نحاول نطلع سعر الوحدة المباع (دايمًا per unit)
    _getSoldUnitPrice(line) {
        // لو unitPrice موجود (الأفضل)
        if (line?.unitPrice) return this._toFloat(line.unitPrice);

        // fallback: price / qty لو unitPrice مش موجود
        const total = this._toFloat(line?.price);
        const qty = this._toFloat(line?.qty) || 1;
        return total / qty;
    },

    // نجيب المنتج من pos cache عن طريق الاسم (نفس اللي اشتغل معك)
    _findProductByLineName(line) {
        const pos = this.env.services.pos;
        const products = pos?.data?.records?.["product.product"];
        if (!products || !line?.productName) return null;

        for (const p of products.values()) {
            if (p.display_name === line.productName || p.name === line.productName) {
                return p;
            }
        }
        return null;
    },

    // نرجّع lst_price كرقم
    getLstPrice(line) {
        const p = this._findProductByLineName(line);
        if (!p) return 0;
        return p.lst_price ?? p.list_price ?? 0;
    },

    // نرجّع lst_price formatted
    getLstPriceFmt(line) {
        const lp = this.getLstPrice(line);
        const fmt =
            this.env.utils?.formatCurrency ||
            this.env.services?.pos?.format_currency ||
            this.env.services?.pos?.formatCurrency;

        return fmt ? fmt(lp || 0) : String(lp || 0);
    },

    // ✅ الشرط اللي تريده: يظهر فقط لو lst_price > sold unit price
    shouldShowLstPrice(line) {
        const lp = this.getLstPrice(line);
        const sold = this._getSoldUnitPrice(line);
        return lp > sold;
    }
});
