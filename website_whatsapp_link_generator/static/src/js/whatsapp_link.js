odoo.define('website_whatsapp_link_generator.whatsapp_link', function (require) {
    "use strict";

    const publicWidget = require('web.public.widget');

    publicWidget.registry.WhatsappLinkGenerator = publicWidget.Widget.extend({
        selector: '.container',

        start: function () {
            this.phoneInput = this.$('#wa_phone');
            this.messageInput = this.$('#wa_message');
            this.linkInput = this.$('#wa_link');
            this.copyButton = this.$('#wa_copy');

            this.phoneInput.on('input', this._updateLink.bind(this));
            this.messageInput.on('input', this._updateLink.bind(this));
            this.copyButton.on('click', this._copyLink.bind(this));

            this._updateLink();

            return this._super.apply(this, arguments);
        },

        _updateLink: function () {
            const phoneRaw = this.phoneInput.val() || '';
            const messageRaw = this.messageInput.val() || '';
            const phone = phoneRaw.replace(/\D/g, '');
            const baseUrl = 'https://wa.me/';

            if (!phone) {
                this.linkInput.val('');
                return;
            }

            let url = baseUrl + phone;

            if (messageRaw) {
                const encodedMessage = encodeURIComponent(messageRaw);
                url += '?text=' + encodedMessage;
            }

            this.linkInput.val(url);
        },

        _copyLink: function () {
            const value = this.linkInput.val();
            if (!value) {
                return;
            }
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(value);
            } else {
                this.linkInput[0].select();
                document.execCommand('copy');
            }
        },
    });

    return publicWidget.registry.WhatsappLinkGenerator;
});