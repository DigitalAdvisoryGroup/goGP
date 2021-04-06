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
    event_ticket_id = fields.Many2one("event.event.ticket", related="event_registration_id.event_ticket_id",string="Ticket")
    state = fields.Selection(related="event_registration_id.state", string="Registration State")
    vehicle_id = fields.Many2one("gogp.vehicles", string="Vehicle")
    racefield_id = fields.Many2one("gogp.racefields", string="Racefield")
    startnumber = fields.Char("StartNumber")
    pitid = fields.Char("Box ID")
    nomination_id = fields.Char("Nomination ID")



class MyProfile(models.Model):
    _name = 'gogp.my.profile'
    _description = 'goGP profile extensions'

    name = fields.Char("myProfile name")
    