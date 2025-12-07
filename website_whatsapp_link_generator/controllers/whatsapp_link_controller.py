from odoo import http
from odoo.http import request


class WhatsappLinkController(http.Controller):

    @http.route('/whatsapp-link-generator', type='http', auth='public', website=True)
    def whatsapp_link_generator(self, **kwargs):
        return request.render('website_whatsapp_link_generator.whatsapp_link_page', {})