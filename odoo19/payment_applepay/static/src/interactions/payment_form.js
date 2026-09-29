import { patch } from '@web/core/utils/patch';

import { PaymentForm } from '@payment/interactions/payment_form';

patch(PaymentForm.prototype, {

    /**
     * Apple Pay uses a redirect form that posts to an intermediate OPPWA page.
     *
     * @override method from @payment/interactions/payment_form
     */
    _processRedirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        if (providerCode === 'applepay') {
            const div = document.createElement('div');
            div.innerHTML = processingValues.redirect_form_html;
            const redirectForm = div.querySelector('form');
            if (!redirectForm) {
                return super._processRedirectFlow(...arguments);
            }
            redirectForm.setAttribute('id', 'o_payment_redirect_form');
            redirectForm.setAttribute('target', '_top');
            document.body.appendChild(redirectForm);
            redirectForm.submit();
            return;
        }
        super._processRedirectFlow(...arguments);
    },

});
