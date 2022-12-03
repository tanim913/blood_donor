import re
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError ,Warning

class PlacesCanVisit(models.Model):
    _name = "visitable.place"
    _description = "Places Can visit"
    _rec_name = 'name'

    name = fields.Char(string = "Visitable Places")

    places_ids = fields.Many2many('blood.donor', 'blood_donor_visitable_place_rel',string="Places")
