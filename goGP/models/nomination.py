# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError



class Nomination(models.Model):
    _name = 'gogp.nomination'
    _description = 'goGP nomination'

    name = fields.Char("Nomination name")
    tech_approval_date = fields.Datetime("Vehicle approval date")
    vehicle_id = fields.Many2one("gogp.vehicles","Nominated vehicle")
    event_id = fields.Many2one("event.event","Nominated for event")
    driver_id = fields.Many2one("res.partner","Nominated driver")
