
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class DonorDistrict(models.Model):
    _name = "donor.district"
    _description = "Donor District"
    _rec_name = 'name'

    name = fields.Char(string = "District")

    district_ids = fields.One2many('blood.donor', 'donor_district_id', string="District")
    