# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError



class MyEvent(models.Model):
    _name = 'gogp.my.event'
    _description = 'goGP participants view'
    _order = 'sequence'

    sequence = fields.Integer(help='Used to order My event in the kanban view', default=1)
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
    nomination_id = fields.Many2one("gogp.nomination","Nomination ID")

    #related fields for kanban
    horsepower = fields.Integer(related="vehicle_id.horsepower", string="Horsepower", store=True)
    cm3 = fields.Integer(related="vehicle_id.cm3",string="Cubic centimetres", store=True)
    model_year = fields.Char(related="vehicle_id.model_year",string="Model Year", store=True)


    def action_create_nomination(self):
        for rec in self:
            if not rec.nomination_id:
                nomination_vals = {
                    "tech_approval_date" : False,
                    "vehicle_id": rec.vehicle_id and rec.vehicle_id.id or False,
                    "event_id" : rec.event_id and rec.event_id.id or False,
                    "driver_id": rec.attendee_id and rec.attendee_id.id or False
                }
                nomination_id = self.env['gogp.nomination'].create(nomination_vals)
                rec.nomination_id = nomination_id.id





class MyProfile(models.Model):
    _name = 'gogp.my.profile'
    _description = 'goGP profile extensions'

    name = fields.Char("myProfile name")
    