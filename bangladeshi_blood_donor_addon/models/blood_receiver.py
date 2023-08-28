from odoo import models, fields, api, _


class BloodReceiver(models.Model):
    _name = "blood.receiver"

    blood_donor_id = fields.Many2one('blood.donor', string='Blood Donor', required=True)
