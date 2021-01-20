# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class SocialGroups(models.Model):
    _name = 'gogp.social_groups.type'
    _description = 'goGP social groups type'

    name = fields.Char("Name")
    code = fields.Char("Code")


class SocialGroups(models.Model):
    _name = 'gogp.social_groups'
    _description = 'goGP social groups'

    name = fields.Char("Social group name", translate=True)
    type = fields.Many2one("gogp.social_groups.type", string="Type", required=True)
    is_public_group = fields.Boolean("Is Public Group", default=False)
    description = fields.Text("Description")
    partner_ids = fields.Many2many('res.partner', 'social_group_partner_rel', 'social_group_id', 'partner_id', string="Partner")
    parent_id = fields.Many2one("gogp.social_groups", string="Parent")
    child_ids = fields.One2many('gogp.social_groups', 'parent_id', string="Child Groups")
    total_count = fields.Integer("Total Subscribers", compute="compute_total_count")
    child_total_count = fields.Integer("Child Subscribers", compute="compute_total_count")

    def action_subscriber_list(self):
        action = self.env.ref('contacts.action_contacts').read()[0]
        partner_ids = self.child_ids.mapped('partner_ids').ids
        action['domain'] = [('id', 'in', partner_ids)]
        return action

    def action_subscriber_list_total(self):
        action = self.env.ref('contacts.action_contacts').read()[0]
        partner_ids = self.child_ids.mapped('partner_ids').ids + self.partner_ids.ids
        action['domain'] = [('id', 'in', partner_ids)]
        return action

    @api.depends('partner_ids', 'child_ids')
    def compute_total_count(self):
        for record in self:
            partner_ids = record.child_ids.mapped('partner_ids').ids
            record.child_total_count = len(partner_ids)
            record.total_count = len(set(partner_ids + record.partner_ids.ids))




class SocialGroupsCodes(models.Model):
    _name = 'gogp.social_groups.codes'
    _description = 'goGP codes for social groups'

    name = fields.Char("Social group code name")