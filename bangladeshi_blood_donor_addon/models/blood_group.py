
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class BlooddGroup(models.Model):
    _name = "donor.blood.group"
    _description = "Donor Blood Group"
    _rec_name = 'name'

    name = fields.Char(string = "Blood Group")

    donor_ids = fields.One2many('blood.donor', 'blood_group_id', string="Donors")
    