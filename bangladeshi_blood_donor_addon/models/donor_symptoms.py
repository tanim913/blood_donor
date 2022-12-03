import re
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError ,Warning

class DonorSymptoms(models.Model):
    _name = "donor.symptoms"
    _description = "Donor Symptoms"
    _rec_name = 'name'

    name = fields.Char(string = "Donor Symptoms")

    symptom_ids = fields.Many2many('blood.donor', 'blood_donor_donor_symptoms_rel',string="Places")
