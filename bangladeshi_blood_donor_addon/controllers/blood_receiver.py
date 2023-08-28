from odoo import http
from odoo.http import request


class BloodReceiverController(http.Controller):

    @http.route('/blood_receiver_page', type='http', auth="public", website=True)
    def blood_receiver_page(self, **kwargs):
        blood_receivers = request.env['blood.receiver'].sudo().search([])
        return http.request.render('bangladeshi_blood_donor_addon.blood_receiver_page_template', {
            'blood_receivers': blood_receivers,
        })
