# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError



class RaceFields(models.Model):
    _name = 'gogp.racefields'
    _description = 'goGP race fields'

    name = fields.Char("Racefield name")
    sort_order = fields.Float("Sort Order")
    event_id = fields.Many2one("event.event", string="Event")
    description = fields.Text("Description")
    image_128 = fields.Binary("Logo")



class RaceFieldsCodes(models.Model):
    _name = 'gogp.racefield.codes'
    _description = 'goGP codes for racefields'

    name = fields.Char("Racefield code name")
    