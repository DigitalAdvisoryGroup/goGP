# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vehicle_lines = fields.One2many("gogp.vehicles", "driver_id", "Vehicles")
    event_lines = fields.One2many("gogp.my.event", "attendee_id", "Events")
    social_group_ids = fields.Many2many('gogp.social_groups', 'social_group_partner_rel', 'partner_id', 'social_group_id', string="Social Group")
