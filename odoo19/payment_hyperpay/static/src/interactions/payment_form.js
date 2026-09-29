import { _t } from '@web/core/l10n/translation';
import { rpc } from '@web/core/network/rpc';
import { patch } from '@web/core/utils/patch';

import { PaymentForm } from '@payment/interactions/payment_form';

const getGeneratedPageURL = ({ html, css, js }) => {
    const source = `
        <html>
            <head>
                ${css}
                ${js}
            </head>
            <body>
                <script>
                    var wpwlOptions = {
                        onReady: function () {
                            var shopOrigin = $('input[name="shopOrigin"]');
                            var origin = parent.window.location.origin;
                            var parent_iframe = $('#hyperpay_iframe', window.parent.document);
                            parent_iframe.css({"width": "100%", "height": "21em", "border": "none", "display": ""});
                            $('.hyperpay_loader', window.parent.document).remove();
                            $('#hyperpay_close', window.parent.document).on('click', function () {
                                parent.window.location.reload(true);
                            });
                            if (shopOrigin.length !== 0 && shopOrigin.val() === 'null') {
                                shopOrigin.val(origin);
                            }
                        },
                        applePay: {
                            displayName: "ENSAN",
                            total: { label: "ENSAN" },
                            supportedNetworks: ["mada"]
                        }
                    };
                    $(document).ready(function () {
                        setTimeout(function () {
                            var parent_frame = window.parent.$("#hyperpay_iframe");
                            if (parent_frame.css('display') === 'none') {
                                $('.hyperpay_loader', window.parent.document).remove();
                                parent_frame.css({"display": "block", "width": "100%", "height": "21em", "border": "none"});
                                $('#hyperpay_close', window.parent.document).on('click', function () {
                                    parent.window.location.reload();
                                });
                            }
                        }, 3000);
                    });
                </script>
                ${html || ''}
            </body>
        </html>
    `;
    const blob = new Blob([source], { type: 'text/html' });
    return URL.createObjectURL(blob);
};

patch(PaymentForm.prototype, {

    _processRedirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        if (providerCode === 'hyperpay') {
            this._processHyperpayFlow(processingValues);
            return;
        }
        super._processRedirectFlow(...arguments);
    },

    async _processHyperpayFlow(processingValues) {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = processingValues.redirect_form_html;
        const txId = wrapper.querySelector('#hyperpay_tx')?.value;
        if (!txId) {
            this._displayErrorDialog(_t("Payment processing failed"), _t("Missing HyperPay transaction."));
            this._enableButton();
            return;
        }

        this._initHyperpayBlockUI(_t("Loading..."));
        try {
            const result = await this.waitFor(rpc('/payment/hyperpay/checkout/create', { txId }));
            if (!result?.checkoutId) {
                const message = result?.error_message || _t("Could not create HyperPay checkout.");
                this._displayErrorDialog(_t("Payment processing failed"), message);
                this._enableButton();
                return;
            }
            this._openHyperpayModal(result, processingValues.redirect_form_html);
        } catch (error) {
            this._displayErrorDialog(_t("Payment processing failed"), error.message || _t("Unknown error"));
            this._enableButton();
        }
    },

    _openHyperpayModal(result, redirectFormHtml) {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = redirectFormHtml;
        const modalElement = wrapper.querySelector('.payment_hyper_modal');
        if (!modalElement) {
            this._displayErrorDialog(_t("Payment processing failed"), _t("Missing HyperPay modal template."));
            this._enableButton();
            return;
        }

        document.body.appendChild(modalElement);
        const modalBody = modalElement.querySelector('#hyperpay-modal-body');
        const styleCss = `<link rel="stylesheet" href="${result.base_url}/payment_hyperpay/static/src/css/hyperpay_style.css" />`;
        const entityParam = result.entityId ? `&entityId=${encodeURIComponent(result.entityId)}` : '';
        const script = `<script async src="${result.domain}/v1/paymentWidgets.js?checkoutId=${result.checkoutId}${entityParam}"></script>`;
        const jsScript = '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>';
        const shopperResultUrlTag = `<form action="${result.base_url}/payment/hyperpay/result?acq=${result.acq}" class="paymentWidgets" data-brands="${result.data_brands}"></form>`;
        const iframe = document.createElement('iframe');
        iframe.id = 'hyperpay_iframe';
        iframe.style.display = 'none';
        iframe.src = getGeneratedPageURL({
            html: script + shopperResultUrlTag,
            css: styleCss,
            js: jsScript,
        });
        modalBody.appendChild(iframe);

        const closeButton = modalElement.querySelector('#hyperpay_close');
        if (closeButton) {
            closeButton.addEventListener('click', () => window.location.reload());
        }

        if (window.bootstrap?.Modal) {
            const modal = window.bootstrap.Modal.getOrCreateInstance(modalElement, {
                backdrop: 'static',
                keyboard: false,
            });
            modal.show();
        } else {
            modalElement.classList.add('show');
            modalElement.style.display = 'block';
        }
    },

    _initHyperpayBlockUI(message) {
        const submitButton = document.querySelector('button[name="o_payment_submit_button"]');
        if (submitButton) {
            submitButton.setAttribute('disabled', 'disabled');
        }
        if (!document.querySelector('.hyperpay_loader_overlay')) {
            const overlay = document.createElement('div');
            overlay.className = 'hyperpay_loader_overlay';
            overlay.innerHTML = `<div class="text-center p-4 text-white"><span>${message}</span></div>`;
            overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:1999;';
            document.body.appendChild(overlay);
        }
    },

});
