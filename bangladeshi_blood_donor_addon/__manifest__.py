# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bangladeshi Blood Donor Module',
    'version': '1.0',
    'category': 'Tools',
    'sequence': 2,
    'author': 'Tanim Aziz',
    'summary': 'Blood Donor information',
    'description': "Blood Donor information",
    'website': '',
    'depends': [
        'base_setup',
    ],
    'data': [
        # 'security/hr_security.xml',
        'security/ir.model.access.csv',
        'views/blood_group_views.xml',
        'views/blood_donor_views.xml',
        'views/donor_district_views.xml',
        'views/visitable_place_views.xml',
        'views/res_partner.xml',
        'views/donor_symptoms_views.xml',
        'report/bangladeshi_blood_donor_addon_reports.xml',
        'report/blood_donor_information_report.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
}
