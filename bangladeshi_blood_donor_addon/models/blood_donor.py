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
    donation_delay_days = fields.Char(string="Donated (Days Ago)")
    today = fields.Date.today()
    bmi = fields.Float(string= "Body Mass Index")
    height = fields.Float(string= "Height(cm)")
    weight = fields.Float(string= "Weight(Kg)")
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

    def calculate_hours_difference(self, symptom_since):
        symptoms_delay = relativedelta.relativedelta(datetime.today(),datetime.strptime(str(self.symptom_since),'%Y-%m-%d'))
        difference = symptoms_delay.hours + (symptoms_delay.days*24)
        return difference 
    
    
    

    @api.onchange('height','weight')
    def onchange_calculate_bmi(self):
        if self.height and self.weight:
            body_mass_index = self.calculate_bmi(self.height, self.weight)
            self.bmi = body_mass_index

    @api.onchange('date_of_birth')
    def onchange_date_of_birth(self):
        if self and self.date_of_birth:
            self.age = self.calculate_age(self.date_of_birth)

    @api.onchange('symptom_since')
    def onchange_symptom_since(self):
        if self and self.symptom_since:
            self.symptom_hours = self.calculate_hours_difference(self.symptom_since)
    
    @api.onchange('last_donated')
    def onchange_last_donated(self):
        if self and self.last_donated:
            d1=datetime.strptime(str(self.today),'%Y-%m-%d') 
            d2=datetime.strptime(str(self.last_donated),'%Y-%m-%d')
            d3=d1-d2
            self.donation_delay_days=str(d3.days)


    @api.model
    def create(self, vals):

        if vals.get("first_name") and vals.get("last_name"):
            vals['name'] = str(vals.get("first_name") +" "+ vals.get("last_name"))
        elif vals.get("first_name") and not vals.get("last_name"):
            vals['name'] = str(vals.get("first_name"))
        elif vals.get("last_name") and not vals.get("first_name"):
            vals['name'] = str(vals.get("last_name"))
        else:
            raise ValidationError("Please provide First Name or Last Name or Both.")
        phone_number = vals['contact_no']
        if len(phone_number) < 11 or len(phone_number) > 11:
            raise ValidationError("Invalid Contact Number")
        if phone_number[:3] != '+88' and len(phone_number) == 11:
            phone_number = "+88" + phone_number
            vals['contact_no'] = phone_number
        if len(phone_number) == 14 and phone_number[:3] != '+88':
            raise ValidationError("Invalid Contact Number")
        result = super(BloodDonor, self).create(vals)

        return result
    
    def write(self, vals):
        if 'contact_no' in vals:
            if len(vals['contact_no'])>14 or len(vals['contact_no'])<11:
                raise ValidationError("Wrong Phone number!! : please insert correct phone number.")
            elif len(vals['contact_no'])==11:
                if vals['contact_no'][0:3]!='+88':
                    vals['contact_no']='+88'+vals['contact_no']
                else:
                    raise ValidationError("Wrong Phone number!! : please insert correct phone number.")
            elif len(vals['contact_no'])==14:
                if vals['contact_no'][0:3]!='+88':
                    raise ValidationError("Wrong Phone number!! : please insert correct phone number.")
            else:
                raise ValidationError("Wrong Phone number!! : please insert correct phone number.")

        if "first_name" in vals or "last_name" in vals:
           
            if vals.get("first_name") and vals.get("last_name"):
                vals['name'] = vals.get("first_name") +" "+ vals.get("last_name")
            elif vals.get("first_name") and not vals.get("last_name"):
                vals['name'] = vals.get("first_name")+" "+self.last_name
            elif vals.get("last_name") and not vals.get("first_name"):
                vals['name'] = self.first_name+" "+vals.get("last_name")


        print(vals)
        result = super(BloodDonor,self).write(vals)
        return result