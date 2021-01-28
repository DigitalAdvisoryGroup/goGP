# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class PartnerSex(models.Model):
    _name = "partner.sex.type"
    _description = "Sex Type"

    name = fields.Char("Name", translate=True)


class PartnerShirtSize(models.Model):
    _name = "partner.shirt.size"
    _description = "Shirt Size"

    name = fields.Char("Name", translate=True)



class ResPartner(models.Model):
    _inherit = 'res.partner'

    vehicle_lines = fields.One2many("gogp.vehicles", "driver_id", "Vehicles")
    event_lines = fields.One2many("gogp.my.event", "attendee_id", "Events")
    partner_sex_id = fields.Many2one("partner.sex.type", "Sex")
    partner_shirt_size_id = fields.Many2one("partner.shirt.size", "Shirt Size")
    birthdate = fields.Date(string="Birthdate")
    social_group_ids = fields.Many2many('gogp.social_groups', 'social_group_partner_rel', 'partner_id', 'social_group_id', string="Social Group")
