# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError



class MyEvent(models.Model):
    _name = 'gogp.my.event'
    _description = 'goGP participants view'

    name = fields.Char("myEvent name")
    attendee_id = fields.Many2one("res.partner",string="Attendee ID")
    event_id = fields.Many2one("event.event", string="Event ID")
    event_registration_id = fields.Many2one("event.registration", string="Registration")
    state = fields.Selection(related="event_registration_id.state", string="Registration State")
    vehicle_id = fields.Many2one("gogp.vehicles", string="Vehicle")



class MyProfile(models.Model):
    _name = 'gogp.my.profile'
    _description = 'goGP profile extensions'

    name = fields.Char("myProfile name")
    