import re
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError ,Warning


class BloodDonor(models.Model):
    _name = "blood.donor"
    _description = "Blood Donor Details"
    _rec_name = 'name'


    donor_id = fields.Char(string="Donor Id")
    
    first_name = fields.Char(string="Donor first Name")
    last_name = fields.Char(string="Donor last Name")
    name = fields.Char(string="Donor Name")
    contact_no = fields.Char(string="Contact Number")
    age = fields.Integer(string="Age")
    marital_status = fields.Char(string="Marital Status")
    donor_pic = fields.Image(string="Donor's Picture", max_width=150, max_height=150)
    date_of_birth = fields.Date(string="Date of Birth")
    last_donated = fields.Date(string="Last Donated")
    today = fields.Date.today()
    bmi = fields.Float(string= "Body Mass Index")
    height = fields.Float(string= "Height(cm)")
    weight = fields.Float(string= "Weight(cm)")
    age = fields.Integer(string="Age")
    contact_no = fields.Char(string="Contact Number")
    rh_factor = fields.Selection(
        string="RH factor",
        selection= [
            ('positive','Positive'),
            ('negative','Negative')
            
        ]
    )
    gender = fields.Selection(
        string="Gender",
        selection= [
            ('male','Male'),
            ('female','Female'),
            ('other','Other')
        ]
    )
    
    occupation = fields.Char(string="Occupation")
    email_address = fields.Char(string="Email Address")

    blood_group_id  = fields.Many2one('donor.blood.group', string='Blood Group')
    donor_district_id = fields.Many2one('donor.district', string='District')

    visitable_places_ids = fields.Many2many('visitable.place', string="Places Can Travel")
    donor_symptoms_ids = fields.Many2many('donor.symptoms', string="Donor Symptoms")
    symptom_since = fields.Date(string="Symptom Since")
    symptom_hours = fields.Float(string="Symptom for (hours)")

    def calculate_bmi(self,h,w):
        height_in_meter = h/100
        body_mass_index = w/(height_in_meter * height_in_meter)
        return body_mass_index

    def calculate_age(self,date_of_birth):
        calculated_age = (datetime.today().date() - datetime.strptime(str(date_of_birth), '%Y-%m-%d').date()) // timedelta(days=365)
        return calculated_age

    def check_eligibility(self):
        donation_delay = relativedelta.relativedelta(datetime.today(),datetime.strptime(str(self.last_donated),'%Y-%m-%d'))
        difference = donation_delay.months + (donation_delay.years*12)

        body_mass_index = self.calculate_bmi(self.height, self.weight)
        age = self.calculate_age(self.date_of_birth)

        if difference >=4 and body_mass_index > 18.5 and age >=18 and age <= 65:
            raise UserError("Eligible for donating blood.")
        else:
            raise UserError("Not Eligible for donating blood.")

    
    @api.onchange('height','weight')
    def onchange_calculate_bmi(self):
        if self.height and self.weight:
            body_mass_index = self.calculate_bmi(self.height, self.weight)
            self.bmi = body_mass_index

    @api.onchange('date_of_birth')
    def onchange_date_of_birth(self):
        if self and self.date_of_birth:
            self.age = self.calculate_age(self.date_of_birth)



    
    
    