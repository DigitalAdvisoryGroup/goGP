# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import UserError



class RaceFields(models.Model):
    _name = 'gogp.racefields'
    _inherit = "website.published.mixin"
    _description = 'goGP race fields'

    name = fields.Char("Racefield name")
    sort_order = fields.Float("Sort Order")
    event_id = fields.Many2one("event.event", string="Event")
    description = fields.Text("Description")
    image_128 = fields.Binary("Logo")
    gp_event_ids = fields.One2many('gogp.my.event','racefield_id',string='Gp Events')

    def _compute_website_url(self):
        super(RaceFields, self)._compute_website_url()
        for race in self:
            if race.id:
                race.website_url = "/racefields/participants/%s" % slug(race)




class RaceFieldsCodes(models.Model):
    _name = 'gogp.racefield.codes'
    _description = 'goGP codes for racefields'

    name = fields.Char("Racefield code name")
    