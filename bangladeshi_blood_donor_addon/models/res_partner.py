import re
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError ,Warning

class ResPartner(models.Model):
    _inherit = 'res.partner'

    blood_group = fields.Char(string="Blood group")

    @api.model
    def create(self, values):
        if not values.get('blood_group'): 
            raise UserError("Blood group field is Empty!")
        res = super(ResPartner, self).create(values)
        return res